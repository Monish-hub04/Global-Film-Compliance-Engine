import os
import re
import requests
from flask import Flask, render_template, request, jsonify
from src.file_parser import process_uploaded_file
from src.nlp_engine import extract_compliance_entities
from src.rating_rules import calculate_ratings

app = Flask(__name__)

OMDB_API_KEY = "77b3410f"

def extract_movie_title(filename):
    name = filename.rsplit('.', 1)[0]
    name = re.sub(r'[\._\-\[\]\(\)]+', ' ', name)
    junk = (r'\b(720p|1080p|2160p|4k|bluray|blu ray|webrip|web dl|hdtv|hdrip|dvdrip|'
            r'x264|x265|hevc|aac|ac3|dts|dd5|hd|uhd|srt|sub|subtitle|script|'
            r'english|hindi|tamil|dubbed|proper|extended|remastered|'
            r'yify|yts|rarbg|eztv|publichd|fgt|ubs|co|en|gang)\b')
    name = re.sub(junk, ' ', name, flags=re.IGNORECASE)
    name = re.sub(r'\b(19|20)\d{2}\b', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return ' '.join(name.split()[:4]).title()

def fetch_movie_data(title):
    words = title.split()
    for length in range(len(words), 0, -1):
        attempt = ' '.join(words[:length])
        try:
            url = (f"http://www.omdbapi.com/?t={requests.utils.quote(attempt)}"
                   f"&apikey={OMDB_API_KEY}&type=movie")
            resp = requests.get(url, timeout=5)
            data = resp.json()
            if data.get("Response") == "True" and data.get("Poster") not in (None, "N/A"):
                return data
        except Exception:
            pass
    return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/how-it-works", methods=["GET"])
def how_it_works():
    return render_template("how-it-works.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    try:
        guessed_title = extract_movie_title(file.filename)
        movie_data = fetch_movie_data(guessed_title)
        
        poster_url = movie_data.get("Poster") if movie_data else None
        
        # Read the file content
        file_content = file.read()
        
        text = process_uploaded_file(file.filename, file_content)
        doc, entity_counts, highlights = extract_compliance_entities(text)
        ratings = calculate_ratings(entity_counts)
        
        return jsonify({
            "success": True,
            "filename": file.filename,
            "guessed_title": guessed_title,
            "movie_data": movie_data,
            "poster_url": poster_url,
            "entity_counts": entity_counts,
            "ratings": ratings,
            "highlights": highlights
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)