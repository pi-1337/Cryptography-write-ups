# RSA Challenge Writeup — Exploiting the \( m^{p+q} \) Leak

The chal is an RSA chal, it's a fun chal, here is the problem:

---

## What we are given

- Public key \((e, N)\)
- Ciphertext of the flag: \(ct_1 = m^e \bmod N\)
- An additional leak: \(ct_2 = m^{p+q} \bmod N\)

In this chal, the primes \(p, q\) are super large, so factoring \(N\) is impractical.

---

## Typical RSA Chal Approach

Usually, the goal is to factor the modulus \(N\) somehow, then decrypt the message.

But in this chal specifically, the general approach doesn't seem to work.  
My approach was to try to recover the message directly.

---

## Step 1: Understanding the leak \(m^{p+q} \bmod N\)

Recall Euler's totient function:

\[
\varphi(N) = (p-1)(q-1) = pq + 1 - (p+q) = N + 1 - (p+q)
\]

What even is \(\varphi(N)\)?  
It's called Euler's totient of \(N\), equal to the product of its prime factors minus 1.

**Example:**  
Let \(p_1, p_2, \dots, p_n\) be the prime factors of \(N\). Then:

\[
\varphi(N) = \prod_{i=1}^n (p_i - 1)
\]

A well-known property is:

\[
a^{\varphi(N)} \equiv 1 \pmod{N}
\]

Fermat's Little Theorem is a special case when \(N\) is prime:  
If \(N\) is prime, then \(\varphi(N) = N - 1\), so

\[
a^{N-1} \equiv 1 \pmod{N}
\]

---

## Step 2: Using \(\varphi(N)\)

Since 

\[
a^{\varphi(N)} \equiv 1 \pmod{N}
\]

then

\[
a^{\varphi(N) + 1} \equiv a \pmod{N}
\]

This means if we raise the plaintext \(m\) to the power \(\varphi(N) + 1\), we get \(m\) back.

We have:

\[
\varphi(N) = N + 1 - (p + q)
\]

and since we already have \(m^{p+q} \bmod N\), maybe we can use this.

---

## Step 3: Combining the leak with known values

If only we could compute

\[
m^{N+1} \bmod N
\]

then

\[
m^{\varphi(N)+1} = m^{N+1 - (p+q) + 1} = m^{N+1} \cdot m^{-(p+q)} \bmod N
\]

and since we have \(m^{p+q} \bmod N\) as \(ct_2\), we can invert that and multiply.

Unfortunately, computing \(m^{N+1} \bmod N\) directly isn't feasible since we don't know \(m\).

---

## Step 4: Approximating \(m^{N+1} \bmod N\) via \(ct_1\)

Given

\[
ct_1 = m^e \bmod N
\]

and knowing

\[
N = \alpha e + \beta, \quad \beta < e
\]

Define

\[
\gamma = e - \beta - 1
\]

Thus,

\[
e = \gamma + \beta + 1
\]

Raising \(ct_1\) to the power \(\alpha + 1\):

\[
(ct_1)^{\alpha + 1} = m^{e(\alpha + 1)} = m^{e\alpha + e} \bmod N
\]

Multiply this by the inverse of \(ct_2 = m^{p+q}\):

\[
m_\gamma = m^{e\alpha + e} \cdot m^{-(p+q)} = m^{e\alpha + e - (p+q)} \bmod N
\]

Substitute \(e = \gamma + \beta + 1\) and \(N = \alpha e + \beta\):

\[
m_\gamma = m^{N + \gamma + 1 - (p+q)} = m^{\varphi(N) + \gamma} = m^{\varphi(N)} \cdot m^\gamma \equiv m^\gamma \pmod{N}
\]

Since

\[
m^{\varphi(N)} \equiv 1 \pmod{N}
\]

we get:

\[
m_\gamma \equiv m^\gamma \pmod{N}
\]

---

## Step 5: Recovering \(m\) using Bézout's lemma

We have:

\[
\begin{cases}
ct_1 = m^e \pmod{N} \\
m_\gamma = m^\gamma \pmod{N}
\end{cases}
\]

By Bézout's lemma, since \(e\) is prime and \(\gamma < e\), \(\gcd(e, \gamma) = 1\).

There exist integers \(x, y\) such that:

\[
ex + \gamma y = 1
\]

Then:

\[
m = (ct_1)^x \cdot (m_\gamma)^y \pmod{N}
\]

because

\[
m^{ex + \gamma y} = m^1 = m
\]

---

## Complete code

```python
from Crypto.Util.number import *

e = 65537

N = 13172635138210286640933237746072073728198869440440273861514688422430115450596963502627269613634657978751692320585777768877613321668778514462972611542147278205792418292362109100597755668571861738781190210255903465162483813897653948305531342676537057130369323555420200545974179860718822410192595079238246216026529376260568656408216009127973127738250617629330070723654601189310430802429585919291621479622419163092371272056180409609142738265178224163465585013019636286435078812898907472859171136422659050412212315590509027225331104292443193693974638004592849794819591007103879538185323581422819852185166422985403024630123

ct1 = 8499526321488266762028127474977263983474334713646962923180757984708039537289636737028409522654349845032612940144246996001396064450188534247830979105036627472087587636695469693411422088223080856169980341928057477564688506588678465277896123712776169270866525885072607021419929184184301722442524104467963680432737243478200661224741027413690099507128782156810842444314483076587935222998920241102484844741597333281611874849648935849985954902264102662618041817365284648356127737145896858259709819593359264714426125676691235985164360773645489923563993927995838346085066937602961724919392025887999986486672200850129835569774

ct2 = 2263178005282615069738169250508811825030372342139636879043114251227029802177975391784856426659871916802959302578620910469427367218786299839311310420522660987052055310279591316813828952756984548230575321772825193775083404279028090110850848262192595930920326368607665856808251531130234210906413358662814500632504899088517752958423466186872534450108628371006268110210630017230741670440780982809417986017372337888735465439382827207990030719121834402226087906249993820193417658352914727984318783025375497623944699995700474418221251293446038111913247755996471673024017921092527032486774115935601292346440934530921157935322

alpha = N // e
beta = N % e
gamma = e - beta - 1

print(f"{alpha = }")
print(f"{beta = }")
print(f"{gamma = }")

m_to_gamma = (pow(ct1, alpha + 1, N) * pow(ct2, -1, N)) % N

def extended_gcd(a, b):
    """
    Returns (gcd, x, y) such that:
       a * x + b * y = gcd(a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return (gcd, x, y)

gcd, x, y = extended_gcd(e, gamma)
flag_to_gcd = (pow(ct1, x, N) * pow(m_to_gamma, y, N)) % N
print("here is the flag to the power of ", gcd, ":", long_to_bytes(flag_to_gcd))
