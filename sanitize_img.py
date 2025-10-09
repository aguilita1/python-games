from PIL import Image

img = Image.open("orca-425x250.png")
img = img.convert("RGBA")  # Force standard RGBA
img.save("orca-clean.png", optimize=True)