import time
import random

class ForexFZM:
    def __init__(self):
        # FZM exchange rates against major forex pairs
        self.rates = {
            "FZM/USD": 0.0050,
            "FZM/KES": 0.65,
            "FZM/EUR": 0.0046,
            "FZM/GBP": 0.0039,
            "FZM/BTC": 0.000000085,
        }
        self.history = []
        self.orders = []

    def get_rates(self):
        print("\n================================")
        print("   FZM LIVE FOREX RATES")
        print("================================")
        print("Time: " + time.strftime('%Y-%m-%d %H:%M:%S'))
        print("--------------------------------")
        for pair, rate in self.rates.items():
            print(pair + " : " + str(rate))
        print("================================")

    def simulate_market(self):
        print("\nSimulating market movement...")
        for pair in self.rates:
            change = random.uniform(-0.0002, 0.0002)
            self.rates[pair] = round(self.rates[pair] + change, 8)
            if self.rates[pair] < 0.0001:
                self.rates[pair] = 0.0001
        print("Market updated!")

    def buy_fzm(self, wallet, currency, amount, wallets):
        if wallet not in wallets:
            print("Wallet not found!")
            return
        if currency not in ["USD", "KES", "EUR", "GBP"]:
            print("Currency not supported!")
            return
        pair = "FZM/" + currency
        rate = self.rates[pair]
        fzm_amount = round(amount / rate, 2)
        wallets[wallet].balance += fzm_amount
        order = {
            "type": "BUY",
            "wallet": wallet,
            "paid": str(amount) + " " + currency,
            "received": str(fzm_amount) + " FZM",
            "rate": rate,
            "time": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.orders.append(order)
        self.history.append(order)
        print("\n================================")
        print("   FZM PURCHASED!")
        print("================================")
        print("Wallet   : " + wallet)
        print("Paid     : " + str(amount) + " " + currency)
        print("Received : " + str(fzm_amount) + " FZM")
        print("Rate     : " + str(rate))
        print("================================")

    def sell_fzm(self, wallet, currency, fzm_amount, wallets):
        if wallet not in wallets:
            print("Wallet not found!")
            return
        if wallets[wallet].balance < fzm_amount:
            print("Not enough FZM!")
            return
        pair = "FZM/" + currency
        rate = self.rates[pair]
        currency_amount = round(fzm_amount * rate, 4)
        wallets[wallet].balance -= fzm_amount
        order = {
            "type": "SELL",
            "wallet": wallet,
            "sold": str(fzm_amount) + " FZM",
            "received": str(currency_amount) + " " + currency,
            "rate": rate,
            "time": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.orders.append(order)
        self.history.append(order)
        print("\n================================")
        print("   FZM SOLD!")
        print("================================")
        print("Wallet   : " + wallet)
        print("Sold     : " + str(fzm_amount) + " FZM")
        print("Received : " + str(currency_amount) + " " + currency)
        print("Rate     : " + str(rate))
        print("================================")

    def order_history(self):
        if not self.history:
            print("\nNo orders yet!")
            return
        print("\n================================")
        print("   FZM ORDER HISTORY")
        print("================================")
        for order in self.history:
            print("\nType : " + order["type"])
            print("Time : " + order["time"])
            if order["type"] == "BUY":
                print("Paid : " + order["paid"])
                print("Got  : " + order["received"])
            else:
                print("Sold : " + order["sold"])
                print("Got  : " + order["received"])
        print("================================")

    def market_depth(self):
        print("\n================================")
        print("   FZM MARKET DEPTH")
        print("================================")
        print("Pair        Buy       Sell")
        print("--------------------------------")
        for pair, rate in self.rates.items():
            buy = round(rate * 0.999, 8)
            sell = round(rate * 1.001, 8)
            print(pair + "  " + str(buy) + "  " + str(sell))
        print("================================")

class Wallet:
    def __init__(self, name):
        self.name = name
        self.balance = 0

if __name__ == "__main__":
    print("\n================================")
    print("   FZM FOREX TRADING")
    print("   Kenya 2026")
    print("================================")

    forex = ForexFZM()
    wallets = {
        "FEZMOH": Wallet("FEZMOH"),
        "TRADER1": Wallet("TRADER1")
    }
    wallets["FEZMOH"].balance = 1000000

    while True:
        print("\n================================")
        print("      FZM FOREX MENU")
        print("================================")
        print("1. Live Rates")
        print("2. Buy FZM")
        print("3. Sell FZM")
        print("4. Order History")
        print("5. Market Depth")
        print("6. Simulate Market")
        print("7. Check Balance")
        print("8. Exit")
        print("================================")
        choice = input("Choice: ")

        if choice == "1":
            forex.get_rates()
        elif choice == "2":
            w = input("Wallet name: ")
            c = input("Currency (USD/KES/EUR/GBP): ")
            a = float(input("Amount to spend: "))
            forex.buy_fzm(w, c, a, wallets)
        elif choice == "3":
            w = input("Wallet name: ")
            c = input("Currency to receive (USD/KES/EUR/GBP): ")
            a = float(input("FZM amount to sell: "))
            forex.sell_fzm(w, c, a, wallets)
        elif choice == "4":
            forex.order_history()
        elif choice == "5":
            forex.market_depth()
        elif choice == "6":
            forex.simulate_market()
            forex.get_rates()
        elif choice == "7":
            w = input("Wallet name: ")
            if w in wallets:
                print("\nBalance: " + str(wallets[w].balance) + " FZM")
            else:
                print("Wallet not found!")
        elif choice == "8":
            print("\nFZM Forex closing...")
            break
