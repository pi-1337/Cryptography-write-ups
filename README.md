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
