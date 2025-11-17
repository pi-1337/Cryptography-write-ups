
class ZKP:
    def __init__(self):
        self.p = getPrime(256)
        self.q = getPrime(256) 
        self.g = 2
        self.w = b2l(FLAG) 
        self.y = pow(self.g, self.w, self.p)
    def prover(self):
            r = randbelow(1 << 200)
            a = pow(self.g, r, self.p)
            e = randbelow(1 << 256)
            z = (r + self.w * e) % self.q
            proof = {"a": a, "e": e, "z": z}
            return proof
    def __str__(self):
        return f"ZKP PUBLIC PARAMETERS:\np = {self.p}\nq = {self.q}\ng = {self.g}\ny = {self.y}"

user = ZKP()

menu = """
[1] Prover
[2] Exit
"""
def main():
    ctr = 0
    print(user)
    print(f'hint: {b2l(FLAG).bit_length()}...you\'re welcome :)')

    while True:
        print(menu)
        choice = input("Select an option > ")
        if choice == '1':
            if ctr >= 6:
                print("You have reached the maximum number of proofs.")
                continue
            
            print("Prover selected.")
            print(f'Here is your proof: {user.prover()}')
            ctr += 1

        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
