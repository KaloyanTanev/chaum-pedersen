import secrets
import sys

import gensafeprime

def start(x):
    # PROVER REGISTRATION
    p = gensafeprime.generate(1024) # send to verifier
    q = (p-1)//2
    g = 81 # public
    h = 121 # public
    y1 = pow(g, x, p) # send to verifier
    y2 = pow(h, x, p) # send to verifier

    # PROVER LOGIN ROUND 1
    k = secrets.randbelow(sys.maxsize - 1)
    r1 = pow(g, k, p) # send to verifier
    r2 = pow(h, k, p) # send to verifier

    # VERIFIER LOGIN ROUND 1
    c = secrets.randbelow(sys.maxsize - 1) # send to prover

    # PROVER LOGIN ROUND 2
    s = (k - (c*x)) % q # send to verifier

    # VERIFIER LOGIN ROUND 2
    r1_comp = (pow(g, s, p) * pow(y1, c, p)) % p
    if(r1_comp != r1):
        return False
    r2_comp = (pow(h, s, p) * pow(y2, c, p)) % p
    if(r2_comp != r2):
        return False
    return True

if __name__ == "__main__":
    sercret = 35
    res = start(sercret)
    print(res)
