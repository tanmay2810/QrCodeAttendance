import pyqrcode
from pyqrcode import QRCode
import png

def qrCodeGenrator(urlPath):
    # String which represents the QR code
    print('fun '+urlPath)
    s = urlPath

    # Generate QR code
    url = pyqrcode.create(s)

    # Create and save the svg file naming "myqr.svg"
    url.svg("static/myqr.svg", scale=8)

    # Create and save the png file naming "myqr.png"
    url.png('static/myqr.png', scale=6)