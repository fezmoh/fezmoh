import socket
import threading
import json
import time

class FZMNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.blockchain = []

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print("\n================================")
        print("   FZM NODE STARTED!")
        print("================================")
        print("Your IP  : 192.168.8.145")
        print("Port     : " + str(self.port))
        print("Waiting for peers...")
        print("================================\n")
        while True:
            try:
                client, address = server.accept()
                print("Peer connected: " + str(address))
                thread = threading.Thread(
                    target=self.handle_peer,
                    args=(client, address)
                )
                thread.start()
            except:
                break

    def handle_peer(self, client, address):
        try:
            while True:
                data = client.recv(4096).decode()
                if not data:
                    break
                message = json.loads(data)
                self.process_message(message, client)
        except:
            pass
        finally:
            client.close()
            print("Peer disconnected: " + str(address))

    def process_message(self, message, client):
        if message["type"] == "HELLO":
            print("Message: " + message["data"])
            response = json.dumps({
                "type": "HELLO",
                "data": "FZM Node Kenya 2026 - Connected!"
            })
            client.send(response.encode())
        elif message["type"] == "NEW_BLOCK":
            print("New block from peer!")
            self.blockchain.append(message["data"])

    def connect_to_peer(self, peer_host, peer_port):
        try:
            peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer.connect((peer_host, peer_port))
            self.peers.append(peer)
            print("Connected to: " + peer_host)
            message = json.dumps({
                "type": "HELLO",
                "data": "FZM Node connecting from Kenya!"
            })
            peer.send(message.encode())
            response = peer.recv(4096).decode()
            data = json.loads(response)
            print("Response: " + data["data"])
            return peer
        except Exception as e:
            print("Error: " + str(e))
            return None

if __name__ == "__main__":
    print("\n================================")
    print("   FZM NETWORK NODE")
    print("   Kenya 2026")
    print("================================\n")
    print("1. Start node (server)")
    print("2. Connect to node (peer)")
    choice = input("\nChoice: ")
    if choice == "1":
        node = FZMNode("0.0.0.0", 5000)
        node.start()
    elif choice == "2":
        host = input("Enter IP to connect to: ")
        node = FZMNode("0.0.0.0", 5001)
        thread = threading.Thread(target=node.start)
        thread.daemon = True
        thread.start()
        time.sleep(1)
        node.connect_to_peer(host, 5000)
        input("\nPress Enter to disconnect...")
