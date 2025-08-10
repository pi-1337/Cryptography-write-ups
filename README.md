RSA Challenge Write-Up
Challenge Description

We are given an RSA challenge where the public key (e, N) and the ciphertext of the flag ct1 are provided. The primes p and q are super large, so factoring N directly isn't feasible. However, we're also given an additional interesting value: ct2 = m^(p+q) mod N.
Approach
Understanding the Problem

In standard RSA challenges, the goal is to factor the modulus N and then decrypt the message. However, in this challenge, the solution involves leveraging the additional information ct2 = m^(p+q) mod N to recover the message directly.
Key Observations

    Euler's Totient Function φ(N):

        For RSA, N = p * q, so:
        text

φ(N) = (p-1)*(q-1) = p*q + 1 - (p+q) = N + 1 - (p+q)

Euler's theorem tells us that for any integer a coprime with N:
text

a^φ(N) ≡ 1 mod N

This implies:
text

    a^(φ(N) + 1) ≡ a mod N

Leaking m^(p+q) mod N:

    Given ct2 = m^(p+q) mod N, we can use it to recover φ(N):
    text

        φ(N) = N + 1 - (p+q)

        Thus, if we can compute m^(φ(N) + 1) mod N, we can recover m.

Mathematical Manipulation

    Expressing φ(N) + 1:

        From φ(N) = N + 1 - (p+q), we have:
        text

    φ(N) + 1 = N + 2 - (p+q)

    However, directly computing m^(N+1) mod N is not straightforward since we don't know m.

Alternative Approach:

    We have ct1 = m^e mod N and ct2 = m^(p+q) mod N.

    Let’s express N in terms of e:
    text

    N = α * e + β, where β = N % e

    Define γ = e - β - 1.

    Then, e = γ + β + 1.

Computing m^γ mod N:

    Raise ct1 to (α + 1)
