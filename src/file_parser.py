import os
import pysrt

def parse_txt(file_content):
    """
    Parses a standard text file or raw text string.
    Returns the string as is.
    """
    if isinstance(file_content, bytes):
        return file_content.decode('utf-8', errors='ignore')
    return str(file_content)

def parse_srt(file_content):
    """
    Parses an SRT file content, extracting only the text without timestamps.
    """
    # Write to a temporary file since pysrt expects a file path
    temp_path = "temp_sub.srt"
    try:
        with open(temp_path, "wb") as f:
            if isinstance(file_content, str):
                f.write(file_content.encode('utf-8'))
            else:
                f.write(file_content)
                
        subs = pysrt.open(temp_path, encoding='utf-8')
        text = " ".join([sub.text for sub in subs])
        
        # Clean up tags like <i>, </i>, etc.
        import re
        text = re.sub(r'<[^>]+>', '', text)
        
        return text
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def process_uploaded_file(filename, file_content):
    if filename.endswith('.srt'):
        return parse_srt(file_content)
    else:
        return parse_txt(file_content)
