# 🩸 VAMP ODDS - Ultimate Betting Game
import json
import random
import time


class Fighter:
    def __init__(self, name, race, power, agility, durability, fatigue, injury, hex):
        self.name = name.strip()
        self.race = race.strip()
        self.power = power
        self.agility = agility
        self.durability = durability
        self.fatigue = fatigue
        self.injury = injury
        self.hex = hex.strip()
        self.battles_fought = 0

    def __str__(self):
        return f"{self.name} is a {self.race}"

    def battle_score(self):
        base = self.power * 0.5 + self.agility * 0.3 + self.durability * 0.2
        fatigue_factor = 1 - self.fatigue / 100
        injury_factor = 1 - self.injury / 120
        score = round(base * fatigue_factor * injury_factor, 2)
        if score < base * 0.85:
            print(f"⚠️ HEX ACTIVATED for {self.name}: {self.hex}")
        return score

    def apply_fatigue_and_injury(self):
        fatigue = random.randint(5, 20)
        injury = random.randint(3, 10)
        self.fatigue = min(100, self.fatigue + fatigue)
        self.injury = min(100, self.injury + injury)
        self.battles_fought += 1
        if self.battles_fought >= 2:
            self.fatigue = max(0, self.fatigue - random.randint(10, 25))
            self.battles_fought = 0

    def status(self):
        return (
            f"{self.name} ({self.race})\n"
            f"Power: {self.power} | Agility: {self.agility} | Durability: {self.durability}\n"
            f"Fatigue: {self.fatigue}/100 | Injury: {self.injury}/100\n"
            f"Hex: {self.hex}\n"
            f"Battle Score: {self.battle_score()}"
        )


class Wallet:
    def __init__(self, balance):
        self.balance = balance

    def bet(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return amount
        else:
            print("Not enough blood coins. Top up.")
            return 0

    def win(self, amount):
        self.balance += amount

    def __str__(self):
        return f"💰 Balance: R{self.balance:.2f}"


def load_fighters(path):
    with open(path, 'r') as f:
        return [Fighter(**data) for data in json.load(f)]

def calculate_odds(f1, f2):
    s1, s2 = f1.battle_score(), f2.battle_score()
    if s1 > s2:
        return {f1.name: round((s2 / s1) * 1.25, 2), f2.name: round((s1 / s2) * 0.75, 2)}
    else:
        return {f1.name: round((s2 / s1) * 0.75, 2), f2.name: round((s1 / s2) * 1.25, 2)}

def simulate_battle(f1, f2):
    time.sleep(1)
    print("\n⚔️ The fight begins...")
    for i in range(3):
        print(".", end='', flush=True)
        time.sleep(0.5)
    print("\n")
    s1, s2 = f1.battle_score(), f2.battle_score()
    winner = f1 if s1 > s2 else f2
    print(f"👑 Winner: {winner.name}\n")
    f1.apply_fatigue_and_injury()
    f2.apply_fatigue_and_injury()
    return winner.name

def quick_bet(wallet, all_fighters):
    print("\n🩸 QUICK BET 🩸")
    for f in all_fighters:
        print(f" - {f.name}")
    f1 = input("Choose fighter 1: ").strip()
    f2 = input("Choose fighter 2: ").strip()
    fighter1 = next((f for f in all_fighters if f.name.lower() == f1.lower()), None)
    fighter2 = next((f for f in all_fighters if f.name.lower() == f2.lower()), None)
    if not fighter1 or not fighter2:
        print("Invalid fighters.")
        return
    odds = calculate_odds(fighter1, fighter2)
    print(f"\n{fighter1.name} odds: {odds[fighter1.name]}x")
    print(f"{fighter2.name} odds: {odds[fighter2.name]}x")
    choice = input("Who do you bet on? ").strip()
    amount = float(input("Bet amount: R"))
    placed = wallet.bet(amount)
    if placed == 0:
        return
    winner = simulate_battle(fighter1, fighter2)
    if choice.lower() == winner.lower():
        winnings = round(placed * odds[winner], 2)
        wallet.win(winnings)
        print(f"🤑 You won R{winnings:.2f}")
    else:
        print("💀 You lost the bet.")
    print(wallet)

def multibet(wallet, all_fighters):
    print("\n🔮 MULTIBET MODE")
    matches = []
    for _ in range(6):
        f1, f2 = random.sample(all_fighters, 2)
        matches.append((f1, f2))
    for i, (f1, f2) in enumerate(matches):
        print(f"[{i+1}] {f1.name} vs {f2.name}")
    chosen = input("Enter match numbers to bet on (comma separated): ").split(',')
    for i in chosen:
        idx = int(i.strip()) - 1
        if 0 <= idx < len(matches):
            f1, f2 = matches[idx]
            print(f"\nMatch: {f1.name} vs {f2.name}")
            odds = calculate_odds(f1, f2)
            print(f"{f1.name} odds: {odds[f1.name]}x | {f2.name} odds: {odds[f2.name]}x")
            pick = input("Your pick: ").strip()
            amount = float(input("Bet amount: R"))
            placed = wallet.bet(amount)
            if placed == 0:
                continue
            winner = simulate_battle(f1, f2)
            if pick.lower() == winner.lower():
                winnings = round(placed * odds[winner], 2)
                wallet.win(winnings)
                print(f"✅ WON: R{winnings:.2f}")
            else:
                loss = placed * 3
                print(f"❌ LOST: R{loss:.2f} (3x penalty)")
    print(wallet)


def main():
    vamp_path = "vamps.json"
    boogie_path = "boogies.json"
    vamp_fighters = load_fighters(vamp_path)
    boogie_fighters = load_fighters(boogie_path)
    all_fighters = vamp_fighters + boogie_fighters
    wallet = Wallet(100)
    print("\n🧛 Welcome to BLOODS ODDS")
    while True:
        mode = input("\nChoose your bet mode (quick / multi): ").strip().lower()
        if mode == "quick":
            quick_bet(wallet, all_fighters)
        elif mode == "multi":
            multibet(wallet, all_fighters)
        else:
            print("Invalid mode.")
            continue
        again = input("\nWanna keep betting? (yes/no): ").strip().lower()
        if again != "yes":
            break
    print("\n🧃 Farewell, creature of chance.")

if __name__ == "__main__":
    main()