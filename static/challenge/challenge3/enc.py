from secret import FLAG
key = 0xC8763
def complex_function(n:int):
    return key * (((n * 0x323) % 0x229) | ((n << 5) ^ 0x34) & (0x8f * key) >> 5)

Cipher = []
for ch in FLAG:
    Cipher.append(complex_function(ch))

print(f"Cipher = {Cipher}")