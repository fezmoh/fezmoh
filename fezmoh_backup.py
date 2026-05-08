from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
import hashlib
import base64
import time
import os

class Wallet:
    def __init__(self, name):
        self.name = name
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()
        self.address = self._generate_address()
        self.balance = 0

    def _generate_address(self):
        pub_bytes = self.public_key.public_bytes(
            serialization.Encoding.X962,
            serialization.PublicFormat.UncompressedPoint
        )
        sha = hashlib.sha256(pub_bytes).digest()
        ripe = hashlib.new('ripemd160', sha).digest()
        return "FZM" + base64.b32encode(ripe).decode()[:15]

    def sign(self, data):
        signature = self.private_key.sign(
            data.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature).decode()

    def verify(self, data, signature):
        try:
            sig_bytes = base64.b64decode(signature)
            self.public_key.verify(
                sig_bytes,
                data.encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False

class Block:
    def __init__(self, index, sender, receiver, amount, previous_hash):
        self.index = index
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.mine(4)

    def calculate_hash(self):
        content = (
            str(self.index) +
            str(self.sender) +
            str(self.receiver) +
            str(self.amount) +
            str(self.previous_hash) +
            str(self.timestamp) +
            str(self.nonce)
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                return self.hash
            self.nonce += 1

class FZMCoin:
    def __init__(self):
        self.chain = []
        self.wallets = {}
        self.total_supply = 21000000
        self.circulating = 0
        self._create_genesis()

    def _create_genesis(self):
        print("Starting FEZMOH COIN...")
        genesis = Block(0, "FZM_SYSTEM", "FZM_SYSTEM", 0, "0")
        self.chain.append(genesis)
        print("Genesis block created!")

    def create_wallet(self, name):
        if name in self.wallets:
            print("Wallet already exists!")
            return
        w = Wallet(name)
        self.wallets[name] = w
        print("\n================================")
        print("   FZM WALLET CREATED!")
        print("================================")
        print("Name    : " + name)
        print("Address : " + w.address)
        print("Balance : 0 FZM")
        print("================================")

    def mint(self, name, amount):
        if name not in self.wallets:
            print("Wallet not found!")
            return
        if self.circulating + amount > self.total_supply:
            print("Exceeds total supply!")
            return
        self.wallets[name].balance += amount
        self.circulating += amount
        block = Block(
            len(self.chain),
            "FZM_SYSTEM",
            name,
            amount,
            self.chain[-1].hash
        )
        self.chain.append(block)
        print("\nMinted " + str(amount) + " FZM to " + name)

    def send(self, sender, receiver, amount):
        if sender not in self.wallets:
            print("Sender not found!")
            return
        if receiver not in self.wallets:
            print("Receiver not found!")
            return
        if self.wallets[sender].balance < amount:
            print("Not enough FZM!")
            return
        fee = round(amount * 0.01, 2)
        actual = amount - fee
        self.wallets[sender].balance -= amount
        self.wallets[receiver].balance += actual
        msg = sender + " sends " + str(amount) + " FZM to " + receiver
        sig = self.wallets[sender].sign(msg)
        if not self.wallets[sender].verify(msg, sig):
            print("Invalid signature! Transaction rejected!")
            return
        block = Block(
            len(self.chain),
            sender,
            receiver,
            actual,
            self.chain[-1].hash
        )
        self.chain.append(block)
        print("\n================================")
        print("   FZM SENT!")
        print("================================")
        print("From    : " + sender)
        print("To      : " + receiver)
        print("Amount  : " + str(actual) + " FZM")
        print("Fee     : " + str(fee) + " FZM")
        print("Block   : #" + str(block.index))
        print("================================")

    def balance(self, name):
        if name not in self.wallets:
            print("Wallet not found!")
            return
        print("\n================================")
        print("Name    : " + name)
        print("Address : " + self.wallets[name].address)
        print("Balance : " + str(self.wallets[name].balance) + " FZM")
        print("================================")

    def info(self):
        print("\n================================")
        print("   FEZMOH COIN (FZM) INFO")
        print("================================")
        print("Total Supply  : 21,000,000 FZM")
        print("Circulating   : " + str(self.circulating) + " FZM")
        print("Total Blocks  : " + str(len(self.chain)))
        print("Total Wallets : " + str(len(self.wallets)))
        print("================================")

def main():
    os.system("clear")
    print("\n================================")
    print("   FEZMOH COIN (FZM)")
    print("   Built in Kenya 2026")
    print("================================\n")
    fzm = FZMCoin()

    while True:
        print("\n================================")
        print("        FZM MENU")
        print("================================")
        print("1. Create Wallet")
        print("2. Mint FZM")
        print("3. Send FZM")
        print("4. Check Balance")
        print("5. Coin Info")
        print("6. Exit")
        print("================================")
        choice = input("Choice: ")

        if choice == "1":
            name = input("Wallet name: ")
            fzm.create_wallet(name)
        elif choice == "2":
            name = input("Wallet name: ")
            amt = int(input("Amount: "))
            fzm.mint(name, amt)
        elif choice == "3":
            s = input("From: ")
            r = input("To: ")
            amt = float(input("Amount: "))
            fzm.send(s, r, amt)
        elif choice == "4":
            name = input("Wallet name: ")
            fzm.balance(name)
        elif choice == "5":
            fzm.info()
        elif choice == "6":
            print("\nThank you for using FEZMOH COIN!")
            print("Built in Kenya 2026\n")
            break

if __name__ == "__main__":
    main()
