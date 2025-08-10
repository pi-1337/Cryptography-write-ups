# RSA Challenge Writeup — Exploiting the \( m^{p+q} \) Leak

A fun RSA challenge where factoring is impossible but **math saves the day**.

---

## 📜 Challenge Summary

We are given:

- **Public key:** (e, N)  
- **Ciphertext of flag:** ct₁ = mᵉ mod N  
- **A mysterious leak:** ct₂ = m^{p+q} mod N  

Here:

- p, q are very large primes, so factoring N is infeasible.  
- The leak ct₂ allows a shortcut without factoring.

---

## 🧠 Step 1 — Understanding the Leak

Recall Euler's totient function:

```math
\varphi(N) = (p-1)(q-1) = pq + 1 - (p + q) = N + 1 - (p+q)

For any a coprime with N:
aφ(N)≡1(modN)
aφ(N)≡1(modN)

This generalizes Fermat's Little Theorem:
aN−1≡1(modN)(if N is prime)
aN−1≡1(modN)(if N is prime)
🧩 Step 2 — Using the Leak and φ(N)φ(N)

From the property above:
aφ(N)+1≡a(modN)
aφ(N)+1≡a(modN)

So if we raise the plaintext m to φ(N)+1φ(N)+1, we recover m.

Since:
φ(N)=N+1−(p+q)
φ(N)=N+1−(p+q)

and we have mp+qmp+q mod N, the idea is to combine it cleverly with mN+1mN+1 mod N.
⚙ Step 3 — Express N in terms of e

Write:
N=αe+β,β<e
N=αe+β,β<e

Define:
γ=e−β−1
γ=e−β−1

Thus:
e=γ+β+1
e=γ+β+1
🛠 Step 4 — Isolating mγmγ

Raise ct₁ to the power α+1α+1:
me(α+1)=meα+e
me(α+1)=meα+e

Multiply by the inverse of ct₂:
mγ=meα+e−(p+q)
mγ​=meα+e−(p+q)

Substitute e=γ+β+1e=γ+β+1 and N=αe+βN=αe+β:
mγ=mN+γ+1−(p+q)=mφ(N)+γ=mφ(N)⋅mγ≡mγ(modN)
mγ​=mN+γ+1−(p+q)=mφ(N)+γ=mφ(N)⋅mγ≡mγ(modN)

Since mφ(N)≡1(modN)mφ(N)≡1(modN).
📐 Step 5 — Recovering m via Bézout's Lemma

We have:
{ct1=me(modN)mγ=mγ(modN)
{ct1​=me(modN)mγ​=mγ(modN)​

By Bézout's lemma, there exist integers x, y such that:
ex+γy=gcd⁡(e,γ)
ex+γy=gcd(e,γ)

Since e is prime and γ<eγ<e, gcd⁡(e,γ)=1gcd(e,γ)=1.

Thus:
m=(ct1x⋅mγy)(modN)
m=(ct1x​⋅mγy​)(modN)

Because:
mex+γy=m1=m
mex+γy=m1=m
