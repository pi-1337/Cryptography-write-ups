# RSA Challenge Writeup — Exploiting `m^(p+q)` Leak

## 📜 Challenge Summary

We are given:

- **Public key:** `(e, N)`
- **Ciphertext:**  
  `ct1 = m^e mod N`
- **Leak:**  
  `ct2 = m^(p+q) mod N`

Here:

- `p` and `q` are **super large primes**, so factoring `N` is not feasible.
- The challenge is **not** to factor `N`, but to exploit the leak to recover `m`.

---

## 🔍 Usual RSA Recap

In RSA:

φ(N) = (p-1) * (q-1)

By Euler's theorem:

a^φ(N) ≡ 1 (mod N)

Fermat's Little Theorem is a special case when `N` is prime:

a^(N-1) ≡ 1 (mod N)


For RSA, if we had `φ(N)`:

a^(φ(N) + 1) ≡ a (mod N)


---

## 🧠 Key Insight

We can write:

φ(N) = (p-1)(q-1)
= pq + 1 - (p + q)
= N + 1 - (p + q)


Since `ct2` leaks `m^(p+q) mod N`, we essentially know `(p+q)` hidden inside `φ(N)`.

If we could compute:

m^(φ(N) + 1) mod N

we’d get back `m`.

---

## ❌ Why the Direct Approach Fails

We **don’t** have `m`, so we can’t directly compute `m^(N+1)` to cancel terms.  
We need to work indirectly.

---

## ✅ Alternate Approach

We have:
- `ct1 = m^e mod N`
- `ct2 = m^(p+q) mod N`
- `e`, `N` public

### Step 1 — Express `N` in terms of `e`

N = α * e + β, 0 ≤ β < e
γ = e - β - 1


### Step 2 — Construct `m_to_γ`
Raise `ct1` to `(α + 1)` and multiply by `ct2` inverse:

m_to_γ = (ct1^(α+1) * ct2^(-1)) mod N

This simplifies to:

m^(φ(N) + γ) ≡ m^γ (mod N)

because:
- `φ(N) = N + 1 - (p+q)`
- `m^φ(N) ≡ 1 (mod N)`

So:

m_to_γ = m^γ mod N


---

## 🧩 Step 3 — Recover `m` Using Bézout's Lemma

We now have:

ct1 = m^e mod N
m_to_γ = m^γ mod N


Bézout’s Lemma:  
If `gcd(a, b) = 1`, there exist integers `x, y` such that:

ax + by = 1


Here:
- `a = e`
- `b = γ`
- `e` is prime, `γ < e` → `gcd(e, γ) = 1`

Then:

m = (ct1^x * m_to_γ^y) mod N

Because:

(ct1^x * m_to_γ^y) ≡ m^(ex + γy) ≡ m^1 (mod N)


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

m_to_gamma = (pow(ct1, alpha + 1, N) * pow(ct2, -1, N)) % N

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return (gcd, x, y)

gcd, x, y = extended_gcd(e, gamma)
flag_to_gcd = (pow(ct1, x, N) * pow(m_to_gamma, y, N)) % N
print(long_to_bytes(flag_to_gcd))

