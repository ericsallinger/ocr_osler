try:
    from PIL import Image
except ImportError:
    import Image
import pandas as pd
import pytesseract

scannedText = open("scannedText.tsv", "w+")
scannedText.write(pytesseract.image_to_data(Image.open('Scanned_documents/Picture_003.jpg')))

