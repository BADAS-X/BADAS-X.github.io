import os
import base64

keyfile = os.path.join(os.getcwd(), "secret.txt")
if not os.path.exists(keyfile):
    with open(keyfile,"wb") as f:
        f.write(os.urandom(24))
#    with open(keyfile, 'r') as f:
#        SECRET_KEY = f.read()
