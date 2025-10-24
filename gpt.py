import subprocess, pytesseract, re, json, os
from PIL import Image

input_path = "competing.jpeg"
clean_path = "cleaned_sharp_inverted.png"
output_json = "ocr_results.json"

# Step 1: Gentle cleanup and invert (no hard thresholding)
subprocess.run([
    "magick", input_path,
    "-scale", "260%",
    "-colorspace", "Gray",
    "-normalize",
    "-level", "72%,100%,2.0",         # Lower the black cutoff to brighten background
    "-blur", "0x1.0",                  # Very slight blur to smooth edges
    "-contrast-stretch", "3.8%",
    "-negate",
    "-sharpen", "0x1",                 # Sharpen text edges
    "-bordercolor", "white",
    "-border", "40x40",
    clean_path
], check=True)



# Step 2: OCR
config = r"--psm 6 -c tessedit_char_whitelist=0123456789.<: "
text = pytesseract.image_to_string(Image.open(clean_path), config=config)
print(text)
# Step 3: Extract only left/right numeric pairs
matches = re.findall(r"([<]?\s*\d+(?:\.\d+)?)\s*[:\s]+1\s*(\d+)", text)
results = [{"left": left.strip().replace(" ", ""), "right": right.strip()} for left, right in matches]

# Step 4: Save and print
with open(output_json, "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
