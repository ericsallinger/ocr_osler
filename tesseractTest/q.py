try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
print(pytesseract.get_tesseract_version())
