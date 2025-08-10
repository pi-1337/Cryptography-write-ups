# RSA Challenge Writeup — Exploiting \( m^{p+q} \) Leak

> *A fun RSA challenge where factoring is impossible but math saves the day.*

---

## 📜 Challenge Summary

We are given:

- Public key: \((e, N)\)
- Ciphertext:
  \[
  \text{ct}_1 = m^e \bmod N
  \]
- A **mysterious leak**:
  \[
  \text{ct}_2 = m^{p+q} \bmod N
  \]

Here:

- \(p\) and \(q\) are *huge* primes — **factoring \(N\)** is not feasible.
- Our goal: **Recover \(m\) (the flag)** without factoring.

---

## 🧠 Initial Thoughts

Normally, an RSA solve path is:

1. Factor \(N = p \cdot q\)
2. Compute \(\varphi(N) = (p-1)(q-1)\)
3. Get \(d = e^{-1} \bmod \varphi(N)\)
4. Compute \(m = \text{ct}_1^d \bmod N\)

But here, factoring is off the table.  
Instead, we’re given:
\[
\text{ct}_2 = m^{p+q} \bmod N
\]
which is **unusual**.

---

## 📐 Key Insight

We know:
\[
\varphi(N) = (p-1)(q-1) = pq - p - q + 1
\]
Replacing \(pq\) with \(N\):
\[
\varphi(N) = N + 1 - (p+q)
\]

Euler's theorem says:
\[
a^{\varphi(N)} \equiv 1 \pmod N
\]

Special case: if \(N\) is prime, \(\varphi(N) = N - 1\) (Fermat's Little Theorem).

From Euler’s theorem:
\[
a^{\varphi(N) + 1} \equiv a \pmod N
\]
So, **if we could raise \(m\) to \(\varphi(N) + 1\)**, we’d get \(m\) back.

---

## 🔍 Relating to the Leak

We have:
- \(\text{ct}_1 = m^e \bmod N\)
- \(\text{ct}_2 = m^{p+q} \bmod N\)

And:
\[
\varphi(N) = N + 1 - (p+q)
\]

If we somehow got \(m^{N+1} \bmod N\),  
we could multiply it by \(m^{-(p+q)}\) (the inverse of \(\text{ct}_2\)) to get:
\[
m^{\varphi(N) + 1} \equiv m \pmod N
\]

Problem: We don’t know \(m^{N+1} \bmod N\) directly.

---

## ⚡ Trick: Approximating \(m^{N+1}\)

Let:
\[
N = \alpha e + \beta, \quad \beta < e
\]

Define:
\[
\gamma = e - \beta - 1
\]

Then:
\[
e = \gamma + \beta + 1
\]

Raise \(\text{ct}_1\) to \(\alpha + 1\):
\[
\text{ct}_1^{\alpha+1} = m^{e(\alpha+1)}
\]

Multiply by \(\text{ct}_2^{-1}\):
\[
m_{\gamma} = m^{e(\alpha+1) - (p+q)}
\]

Substitute \(e = \gamma + \beta + 1\) and \(N = \alpha e + \beta\):
\[
m_{\gamma} = m^{\varphi(N) + \gamma} \equiv m^\gamma \pmod N
\]
(Because \(m^{\varphi(N)} \equiv 1 \pmod N\))

---

Now we have:
\[
\text{ct}_1 = m^e \bmod N
\]
\[
m_{\gamma} = m^\gamma \bmod N
\]

---

## 📏 Recovering \(m\) — Bézout's Lemma

Bézout's Lemma says:
\[
\exists \ x, y \ \text{s.t.} \ e x + \gamma y = \gcd(e, \gamma)
\]

Since \(e\) is prime and \(\gamma < e\), we have:
\[
\gcd(e, \gamma) = 1
\]

Thus:
\[
m = \left( \text{ct}_1^x \cdot m_{\gamma}^y \right) \bmod N
\]
Because:
\[
(\text{ct}_1^x \cdot m_{\gamma}^y) \bmod N
= m^{ex + \gamma y} \bmod N
= m^1 \bmod N
\]

---

## 💻 Exploit Code

```python
from Crypto.Util.number import *

e = 65537
N = 13172635138210286640933237746072073728198869440440273861514688422430115450596963502627269613634657978751692320585777768877613321668778514462972611542147278205792418292362109100597755668571861738781190210255903465162483813897653948305531342676537057130369323555420200545974179860718822410192595079238246216026529376260568656408216009127973127738250617629330070723654601189310430802429585919291621479622419163092371272056180409609142738265178224163465585013019636286435078812898907472859171136422659050412212315590509027225331104292443193693974638004592849794819591007103879538185323581422819852185166422985403024630123
ct1 = 8499526321488266762028127474977263983474334713646962923180757984708039537289636737028409522654349845032612940144246996001396064450188534247830979105036627472087587636695469693411422088223080856169980341928057477564688506588678465277896123712776169270866525885072607021419929184184301722442524104467963680432737243478200661224741027413690099507128782156810842444314483076587935222998920241102484844741597333281611874849648935849985954902264102662618041817365284648356127737145896858259709819593359264714426125676691235985164360773645489923563993927995838346085066937602961724919392025887999986486672200850129835569774
ct2 = 2263178005282615069738169250508811825030372342139636879043114251227029802177975391784856426659871916802959302578620910469427367218786299839311310420522660987052055310279591316813828952756984548230575321772825193775083404279028090110850848262192595930920326368607665856808251531130234210906413358662814500632504899088517752958423466186872534450108628371006268110210630017230741670440780982809417986017372337888735465439382827207990030719121834402226087906249993820193417658352914727984318783025375497623944699995700474418221251293446038111913247755996471673024017921092527032486774115935601292346440934530921157935322

alpha = N // e
beta = N % e
gamma = e - beta - 1

# m^gamma
m_to_gamma = (pow(ct1, alpha + 1, N) * pow(ct2, -1, N)) % N

# Extended GCD
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x1, y1 = extended_gcd(b % a, a)
        return (g, y1 - (b // a) * x1, x1)

g, x, y = extended_gcd(e, gamma)

# Recover m
m = (pow(ct1, x, N) * pow(m_to_gamma, y, N)) % N
print(long_to_bytes(m))
