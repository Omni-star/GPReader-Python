import base64
import qrcode
import json
import base45
import zlib
import cbor2
import zbar
from cose.headers import KID
from cose.messages import CoseMessage
from PIL import Image
from qrcode import QRCode

img = Image.open('img_1.png').convert("L")
scanner = zbar.Scanner()
result = scanner.scan(img)
i = result.pop()
#print(i)
info = i.data
info = info[4:]
#print(info)
decoded = base45.b45decode(info)
#print(decoded)
decompressed = zlib.decompress(decoded)
#print(decompressed)
cose = CoseMessage.decode(decompressed)
#print(cose)


print(json.dumps(cbor2.loads(cose.payload), indent=2))
