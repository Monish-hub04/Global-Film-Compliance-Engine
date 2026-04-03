from src.file_parser import parse_txt
from src.nlp_engine import extract_compliance_entities
from src.rating_rules import calculate_ratings

with open("sample_mature.txt", "r") as f:
    text = parse_txt(f.read())
    
doc, counts, highlights = extract_compliance_entities(text)
print("Entities:", counts)
print("Ratings:", calculate_ratings(counts))
