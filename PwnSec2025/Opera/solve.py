
from chall import *

# ================ first REQ (encrypt flag) ===========================

N = 4916080727098179914441241519095552553856565700728450075108170059002990957939138896547105292967739166027945377243402934097595656728822101653101831279139531
enc_flag = bytes.fromhex("7522d4be9b90773ef12ac08c421cc5f530fca2fb770627b78b4bf6eb65cafd42160110520ec65a7f47710cf7656915e4ee1e13d2ed38d83d7207504acb66a968")
flaglen = len(enc_flag)

# ================ second REQ (encrypt empty string) ===========================
second_res = bytes.fromhex("d52700e2d5afba119e8b1ef7a43f3b80ce64e020c33c29add39fe92d6aa2edd4")

# ================ third REQ (encrypt empty string) ===========================
third_res = bytes.fromhex("0b60eac0d73cdb29385180dd650321c8bdb94ae5bdf9c5855f993575d5929c5c")

# ================ forth REQ (encrypt "A") ===========================

A_enc = bytes.fromhex("58f94332a306f99f84e95766814dd46f0931a2bcd3251f6bcf22ce3268fb3400")

# ================ SOLVE AJMI ===========================
def recover_lcg_states(stream):
    m = 1 << 64
    xs = [int.from_bytes(stream[i:i+8], "big") for i in range(0, len(stream), 8)]
    x1, x2, x3 = xs[0], xs[1], xs[2]
    d1 = (x2 - x1) % m
    d2 = (x3 - x2) % m
    a = (d2 * pow(d1, -1, m)) % m
    c = (x2 - a*x1) % m
    return a, c, m

a, c, m = recover_lcg_states(second_res)
a, c, m = recover_lcg_states(third_res)
# the first output is comfirmed to identical to the second

ainv = pow(a, -1, m)
def prev(x):
    return (ainv * (x - c)) % m

def next(x): 
    x=(a*x+c)%m
    return x

xs3 = [int.from_bytes(third_res[i:i+8], "big") for i in range(0, len(third_res), 8)]
xs2 = [int.from_bytes(second_res[i:i+8], "big") for i in range(0, len(second_res), 8)]

print("doing good ? ", xs2[-1] == prev(xs3[0]))

xs1 = [prev(x) for x in xs2]

def complete_stream_prev(xs, l):
    need = (l - len(xs)) // len(xs[0].to_bytes(8,"big"))
    for _ in range(need):
        xs.insert(0, prev(xs[0]))
    
def complete_stream_next(xs, l):
    need = (l - len(xs)) // len(xs[0].to_bytes(8,"big"))
    for _ in range(need):
        xs.append(next(xs[-1]))
    
complete_stream_prev(xs1, len(enc_flag))

def xs_to_bytes(xs, n):
    out=b""
    i=0
    while len(out)<n:
        out+=xs[i].to_bytes(8,"big")
        i = i+1
    return out

C0 = (xor(xs_to_bytes(xs1, flaglen), enc_flag))
print(C0.hex())

from Crypto.Util.number import *

xs4 = [next(xs3[-1])]
complete_stream_next(xs4, len(A_enc))
A = (xor(xs_to_bytes(xs4[-len(A_enc):], len(A_enc)), A_enc))
print(A)
s="A"
m=s.encode()
e = 0x10001
B = pow(bytes_to_long(m), e, N)
import math
p = (math.gcd(B-bytes_to_long(A), N))

print(p)
print("are we good ? ", N%p==0 and p != 1)

q=N//p
# ========== Decrypt FLAG ============

print(long_to_bytes(pow(bytes_to_long(C0), pow(e, -1, (p-1)*(q-1)), N)))

# ========== OUTPUT ============
# doing good ?  True
# 2c1a38c828a55d5f9e630a8f940a1385e15aec1252ac3fca89c1ad84a7372906e06ee4a7a3ca46062f6c7038d2df5a5c7d647aa2fe0015685c0eac70430144a4
# b'O{\x04\x9c?\xf1.^\xf4g\xf6\xde\x08\xf7\xde\xff\x18\xb4\x0c^\xd6\x9f\xa7\xb6\xaa\xb8/\x1aYnud'
# 61737447455151085190911017044968419618689478567149066920180466069341485265367
# are we good ?  True
# b'flag{abc87ec0bc4741ab}'