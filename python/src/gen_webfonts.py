import requests
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
from fontTools.ttLib.woff2 import compress
import re
import json
import os

def download_ttf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded TTF file: {filename}")
    else:
        raise Exception(f"Failed to download the file: {url}")

def parse_unicode_ranges(unicode_ranges):
    codepoints = set()
    for range_str in unicode_ranges:
        # Remove "U+"
        range_str = range_str.replace("U+", "").upper()
        
        # Get range of codepoints
        match = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+)', range_str)
        if match:
            start, end = match.groups()
            start, end = int(start, 16), int(end, 16)
            codepoints.update(range(start, end + 1))
        else:
            # Single codepoint
            codepoints.add(int(range_str, 16))
    return codepoints

def convert_ttf_to_woff2(ttf_filename, woff2_filename, unicode_ranges):
    font = TTFont(ttf_filename)

    options = Options()
    codepoints = parse_unicode_ranges(unicode_ranges)

    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=codepoints)
    subsetter.subset(font)

    font.flavor='woff2'

    directory = os.path.dirname(woff2_filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    font.save(woff2_filename)
    
    print(f"Converted to WOFF2 file: {woff2_filename}")

def generate_webfont(fontname, filename, spec, unicode_ranges):
    weights = ["regular", "700"]
    # Loop through weights
    for weight in weights:
        if not weight in spec["files"]:
            continue
        ttf_url = spec["files"][weight]
        ttf_filename = f"fonts/{filename}-{weight}.ttf"
        # Download TTF file
        download_ttf(ttf_url, ttf_filename)

        # Loop unicode ranges with index
        for i, unicode_range in enumerate(unicode_ranges):
            woff2_filename = f"dist/{filename}/{spec["version"]}/{filename}-{weight}-{i}.woff2"
            convert_ttf_to_woff2(ttf_filename, woff2_filename, unicode_range)

def get_spec(fontname, webfonts_spec):
    for spec in webfonts_spec["items"]:
        if spec["family"] == fontname:
            return spec
    return None

if __name__ == "__main__":
    with open("config/webfonts.json", "r") as f:
        webfonts = json.load(f)

    with open("config/webfonts_spec.json", "r") as f:
        webfonts_spec = json.load(f)

    with open("config/ranges.json", "r") as f:
        unicode_ranges = json.load(f)
    
    for filename, fontname in webfonts.items():
        print(f"Generating webfont: {fontname}")
        spec = get_spec(fontname, webfonts_spec)
        if spec:
            generate_webfont(fontname, filename,  spec, unicode_ranges)
        else:
            print(f"Spec not found for {fontname}")
            abort()
