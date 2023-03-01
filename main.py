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

img = Image.open('greenpass2.jpeg').convert("L")
scanner = zbar.Scanner()
result = scanner.scan(img)
i = result.pop()
print(i)
info = i.data
info = info[4:]
print(info)
decoded = base45.b45decode(info)
print(decoded)
decompressed = zlib.decompress(decoded)
print(decompressed)
cose = CoseMessage.decode(decompressed)
print(cose)
sign = cose.__getattribute__("signature")
payload = cose.payload
decodedSign = base64.b64encode(sign)
print(sign)
"""
kid = cose.phdr[KID]
decodedKid = base64.b64encode(kid)
print(decodedKid)
"""
print(cose.payload)
print(tuple(cose.payload))
print(json.dumps(cbor2.loads(cose.payload), indent=2))
json_to_change =\
{
  "4": 1699747200,
  "6": 1639993894,
  "1": "IT",
  "-260": {
    "1": {
      "v": [
        {
          "dn": 3,
          "ma": "ORG-100030215",
          "vp": "1119349007",
          "dt": "2021-12-19",
          "co": "IT",
          "ci": "01ITDC3747AE32E140D6ACCE060850B9A9C3#6",
          "mp": "EU/1/20/1528",
          "is": "Ministero della Salute",
          "sd": 3,
          "tg": "840539006"
        }
      ],
      "nam": {
        "fnt": "MORANTE",
        "fn": "MORANTE",
        "gnt": "MARIANNA",
        "gn": "MARIANNA"
      },
      "ver": "1.3.0",
      "dob": "1966-09-18"
    }
  }
}

"""
json_to_change = json.dumps(json_to_change, indent=2)
json_str = json.loads(json_to_change)
json_changed = cbor2.dumps(json_str)
print(json_changed)
print(tuple(json_changed))
json_byte = b'\xa4\x04'
#json_changed = json_byte + json_changed[3:]
print(json_changed)
"""
json_changed = b'\xa4\x04\x1aeP\x15\x80\x06\x1aa\xc0R&\x01bIT9\x01\x03\xa1\x01\xa4av\x81\xaabdn\x03bmamORG-100030215bvpj1119349007bdtj2021-12-19bcobITbcix&01ITDC3747AE32E140D6ACCE060850B9A9C3#6bmplEU/1/20/1528bisvMinistero della Salutebsd\x03btgi840539006cnam\xa4cfntgMORANTEbfngMORANTEcgnthMARIANNAbgnhMARIANNAcvere1.3.0cdobj1999-06-21'
cose.__setattr__("payload", json_changed)
cose_encoded = cose.encode(sign=False)
b = b'X@'
cose_encoded = cose_encoded + b + sign
cose_encoded = (b'\xd2\x84M') + cose_encoded[3:]
print(cose_encoded)
compressed = zlib.compress(cose_encoded)
compressed = compressed[:-4] + (b'\xcb\xa5v\xd8')
print(compressed)
encoded = base45.b45encode(compressed)
print(encoded)
strct = b'HC1:'
output = strct + encoded
print(output)

qr = qrcode.QRCode(
  version=15,
  box_size=9,
  border=1
)

qr.add_data(output)
qimg = Image.Image.
qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
qr_pos = (0, 12)

img.convert('RGB')
img.paste(qr_img, qr_pos)
img.save("mygreen.jpeg")

