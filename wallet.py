from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
import hashlib
import base64

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

    def show(self):
        print("\n================================")
        print("   FEZMOH WALLET CREATED!")
        print("================================")
        print("Name    : " + self.name)
        print("Address : " + self.address)
        print("Balance : " + str(self.balance) + " FZM")
        print("================================")

if __name__ == "__main__":
    print("Creating wallets...")
    alice = Wallet("Alice")
    bob = Wallet("Bob")
    alice.show()
    bob.show()
    print("\nTesting signature...")
    msg = "Send 100 FZM to Bob"
    sig = alice.sign(msg)
    print("Valid: " + str(alice.verify(msg, sig)))
    print("Tampered: " + str(alice.verify("Send 999 FZM", sig)))
    print("\nWallet system working!")
