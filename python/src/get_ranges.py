import os
import re
import json
import requests

def download_file(url, filename):
    # Download the file with user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download the file: {url}")

def extract_unicode_ranges(file_path):
    unicode_ranges = []

    with open(file_path, 'r') as file:
        content = file.read()

        # Collect all unicode-range values
        matches = re.findall(r'unicode-range:\s*([^;]+);', content)

        for match in matches:
            # Split multiple ranges
            ranges = [item.strip() for item in match.split(',')]
            unicode_ranges.append(ranges)

    return unicode_ranges

def save_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    spec_file_path = 'config/webfonts_spec.json'
    input_file_path = 'config/notosansjp.css'
    output_file_path = 'config/ranges.json'

    # Get API key from environment variable
    API_KEY = os.environ.get('GOOGLE_FONTS_API_KEY')
    spec_url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={API_KEY}"

    # Download the spec file
    download_file(spec_url, spec_file_path)

    # Download CSS file
    css_url = 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP'
    download_file(css_url, input_file_path)

    # Extract unicode ranges
    unicode_ranges = extract_unicode_ranges(input_file_path)
    save_to_json(unicode_ranges, output_file_path)

    print(f"Unicode ranges have been saved to {output_file_path}")
