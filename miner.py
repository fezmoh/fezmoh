import hashlib
import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.mine(4)

    def calculate_hash(self):
        content = (
            str(self.index) +
            str(self.data) +
            str(self.previous_hash) +
            str(self.timestamp) +
            str(self.nonce)
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        print("Mining block " + str(self.index) + "...")
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                print("Block mined! Hash: " + self.hash[:20] + "...")
                return self.hash
            self.nonce += 1

if __name__ == "__main__":
    print("\n=== FZM MINING TEST ===\n")
    start = time.time()
    b1 = Block(1, "Alice sends 100 FZM to Bob", "0000genesis")
    b2 = Block(2, "Bob sends 50 FZM to Alice", b1.hash)
    b3 = Block(3, "Alice sends 25 FZM to Ken", b2.hash)
    end = time.time()
    print("\n=== RESULTS ===")
    print("Blocks mined : 3")
    print("Time taken   : " + str(round(end - start, 2)) + " seconds")
    print("Security     : 4 zeros required per block")
    print("\nMining system working!")
