import json
import os
from .connecting import obj

def load_tokens_auth():
    xsrf = os.getenv('xsrf')
    hhtoken = os.getenv('hhtoken')
    
    if xsrf and hhtoken:
        obj.xsrf = xsrf
        obj.hhtoken = hhtoken
    else:
        print("Tokens not found in environment variables.")
