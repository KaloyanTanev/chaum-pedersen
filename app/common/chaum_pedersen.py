from hashlib import sha256
import os
import secrets
import gensafeprime
import sys

def calcualte_id(y1, y2, p):
    conc = f'{y1} {y2} {p}'
    id = sha256(conc.encode()).hexdigest()
    return id

def get_g():
    return int(os.getenv('CHAUM_PEDERSEN_G', "4"))

def get_h():
    return int(os.getenv('CHAUM_PEDERSEN_H', "9"))

def random_number():
    return secrets.randbelow(sys.maxsize - 1)

def generate_safe_prime():
    return gensafeprime.generate(1024)
