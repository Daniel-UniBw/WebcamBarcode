import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Load the image
path = "testimage.jpeg"
image = cv2.imread(path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to the image
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Find barcodes
barcodes = decode(thresh)

for barcode in barcodes:
    barcode_data = barcode.data.decode("utf-8")
    print("Barcode:", barcode_data)
