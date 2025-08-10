RSA Challenge Solution
Challenge Overview

We are given:

    Public key: $(e, N)$

    Ciphertext: $c_1 \equiv m^{e} \pmod{N}$

    Additional value: $c_2 \equiv m^{p+q} \pmod{N}$

Where:

    $N = pq$ (standard RSA modulus)

    $p,q$ are large primes

    $m$ is the plaintext message (flag)

Key Mathematical Relationships
Euler's Totient Function

For RSA modulus $N = pq$:
ϕ(N)=(p−1)(q−1)=N+1−(p+q)ϕ(N)=(p−1)(q−1)=N+1−(p+q)

From Euler's theorem:
mϕ(N)≡1(modN)  ⟹  mϕ(N)+1≡m(modN)mϕ(N)≡1(modN)⟹mϕ(N)+1≡m(modN)
Solution Approach
Step 1: Express $\phi(N)$ using $c_2$

We can write:
ϕ(N)=N+1−(p+q)ϕ(N)=N+1−(p+q)

Thus to recover $m$, we'd want to compute:
mϕ(N)+1=mN+1−(p+q)+1=mN+2−(p+q)mϕ(N)+1=mN+1−(p+q)+1=mN+2−(p+q)

But we have $c_2 \equiv m^{p+q} \pmod{N}$, so:
mN+2⋅c2−1≡mN+2−(p+q)(modN)mN+2⋅c2−1​≡mN+2−(p+q)(modN)
Step 2: Compute $m^{N+1}$ using the public key

Given $c_1 \equiv m^e \pmod{N}$, we can express $N$ as:
N=αe+βwhere 0≤β<eN=αe+βwhere 0≤β<e

Define $\gamma = e - \beta - 1$, then:
e=γ+β+1e=γ+β+1

Compute:
mγ≡c1α+1⋅c2−1(modN)mγ≡c1α+1​⋅c2−1​(modN)
Step 3: Combine using Extended Euclidean Algorithm

We now have:

    $c_1 \equiv m^e \pmod{N}$

    $m^\gamma \pmod{N}$

Since $e$ is prime and $\gamma < e$, $\gcd(e, \gamma) = 1$. Using the Extended Euclidean Algorithm, find integers $x,y$ such that:
ex+γy=1ex+γy=1

Then recover $m$ as:
m≡c1x⋅(mγ)y(modN)m≡c1x​⋅(mγ)y(modN)
Python Implementation
python

from Crypto.Util.number import *

# Given values
e = 65537
N = 131...0123  # (full value omitted for brevity)
c1 = 849...9774  # m^e mod N
c2 = 226...5322  # m^{p+q} mod N

# Step 1: Compute alpha, beta, gamma
alpha = N // e
beta = N % e
gamma = e - beta - 1

# Step 2: Compute m^gamma
m_gamma = pow(c1, alpha+1, N) * pow(c2, -1, N) % N

# Step 3: Apply Extended Euclidean Algorithm
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x1, y1 = extended_gcd(b % a, a)
        return (g, y1 - (b // a) * x1, x1)

gcd, x, y = extended_gcd(e, gamma)
assert gcd == 1  # Since e is prime and γ < e

# Recover the flag
flag = pow(c1, x, N) * pow(m_gamma, y, N) % N
print(long_to_bytes(flag))

Explanation

This solution cleverly combines:

    The leaked $m^{p+q} \bmod N$ to access $\phi(N)$ relationship

    The public key encryption $m^e \bmod N$

    Bezout's identity to combine exponents

The approach avoids factorization of N entirely, instead using the extra information to construct a system of congruences that can be solved for the original message.
