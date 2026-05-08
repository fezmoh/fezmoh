import hashlib
import time

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

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis()

    def create_genesis(self):
        print("Creating FZM Genesis Block...")
        genesis = Block(0, "FZM_SYSTEM", "FZM_SYSTEM", 0, "0")
        self.chain.append(genesis)
        print("Genesis block created!")

    def add_transaction(self, sender, receiver, amount):
        print("Processing transaction...")
        block = Block(
            len(self.chain),
            sender,
            receiver,
            amount,
            self.chain[-1].hash
        )
        self.chain.append(block)
        print("Transaction confirmed in block " + str(block.index))
        return block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.previous_hash != previous.hash:
                return False
        return True

    def show_chain(self):
        print("\n=== FZM BLOCKCHAIN ===")
        for block in self.chain:
            print("\nBlock #" + str(block.index))
            print("From    : " + str(block.sender))
            print("To      : " + str(block.receiver))
            print("Amount  : " + str(block.amount) + " FZM")
            print("Hash    : " + block.hash[:25] + "...")

if __name__ == "__main__":
    print("\n=== FZM BLOCKCHAIN TEST ===\n")
    fzm = Blockchain()
    print("\nAdding transactions...")
    fzm.add_transaction("Alice", "Bob", 100)
    fzm.add_transaction("Bob", "Ken", 50)
    fzm.add_transaction("Ken", "Alice", 25)
    fzm.show_chain()
    print("\nBlockchain valid: " + str(fzm.is_valid()))
    print("\nBlockchain system working!")
