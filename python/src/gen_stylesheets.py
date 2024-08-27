import json

def generate_font_faces(fontname, fontweight, url, unicode_range):
    fontweight = "400" if fontweight == "regular" else "700"
    unicode_range = ", ".join(unicode_range)
    font_face_template = f"""
@font-face {{
  font-family: '{fontname}';
  font-style: normal;
  font-weight: {fontweight};
  font-display: swap;
  src: url({url}) format('woff2');
  unicode-range: {unicode_range};
}}
"""
    return font_face_template

def generate_stylesheet(fontname, filename, spec, unicode_ranges):
    with open(f"dist/{filename}.css", 'w', encoding='utf-8') as file:
        weights = ["regular", "700"]
        # Loop through weights
        for weight in weights:
            if not weight in spec["files"]:
                continue
            ttf_url = spec["files"][weight]
            
            # Loop unicode ranges with index
            for i, unicode_range in enumerate(unicode_ranges):
                woff2_url = f"/webfonts/{filename}/{spec["version"]}/{filename}-{weight}-{i}.woff2"
                file.write(generate_font_faces(fontname, weight, woff2_url, unicode_range))
                file.write("\n")

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
        print(f"Generating stylesheet: {fontname}")
        spec = get_spec(fontname, webfonts_spec)
        if spec:
            generate_stylesheet(fontname, filename,  spec, unicode_ranges)
        else:
            print(f"Spec not found for {fontname}")
            abort()
