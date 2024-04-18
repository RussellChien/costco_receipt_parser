import pytesseract
from PIL import Image

# Path to tesseract executable
# On Windows, you might need to set the path to the tesseract.exe file directly
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load an image
image_path = r'data\test.jpg'
image = Image.open(image_path)

# Use Tesseract to do OCR on the image
text = pytesseract.image_to_string(image)

# Print the text
print(text)
