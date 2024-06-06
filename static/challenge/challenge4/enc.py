from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from secret import FLAG

FLAG = bytes_to_long(FLAG)
p = getPrime(1024)
q = getPrime(1024)
e = 5
N = p * q
C = pow(FLAG, e, N)
print(f"N = {N}")
print(f"C = {C}")