import os
import base64
import random
import string
import shutil

keyfile = os.path.join(os.getcwd(), "secret.txt")
if not os.path.exists(keyfile):
    s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
    print(s)
    with open(keyfile,"w") as f:
        f.write(s)
#    with open(keyfile, 'r') as f:
#        SECRET_KEY = f.read()
shutil.move("secret.txt","secret.key")