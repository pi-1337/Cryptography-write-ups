# RSA Challenge Writeup — Exploiting the \( m^{p+q} \) Leak

A fun RSA challenge where factoring is impossible but **math saves the day**.

---

## 📜 Challenge Summary

We are given:

- **Public key:** (e, N)  
- **Ciphertext of flag:**  

```math
ct_1 = m^{e} \bmod N
