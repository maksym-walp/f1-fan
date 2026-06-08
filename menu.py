import storage


def _input(prompt):
    return input(prompt).strip()


# --- Teams ---

def teams_menu():
    while True:
        print("\n-- Teams --")
        print("1. List  2. Add  3. Edit  0. Back")
        choice = _input("> ")
        if choice == "1":
            items = storage.list_teams()
            if not items:
                print("No teams.")
            for t in items:
                print(f"  [{t.id}] {t.name} ({t.country})")
        elif choice == "2":
            name = "Ferrari"
            country = "Gernmany"
            storage.add_team(name, country)
            print("Added.")
        elif choice == "3":
            tid = int(_input("ID to edit: "))
            name = _input("New name: ")
            country = _input("New country: ")
            storage.edit_team(tid, name, country)
            print("Updated.")
        elif choice == "0":
            break


# --- Pilots ---

def pilots_menu():
    while True:
        print("\n-- Pilots --")
        print("1. List  2. Add  3. Edit  0. Back")
        choice = _input("> ")
        if choice == "1":
            items = storage.list_pilots()
            if not items:
                print("No pilots.")
            for p in items:
                print(f"  [{p.id}] {p.name} ({p.country}) - {p.team}")
        elif choice == "2":
            name = _input("Name: ")
            country = _input("Country: ")
            team = _input("Team: ")
            storage.add_pilot(name, country, team)
            print("Added.")
        elif choice == "3":
            pid = int(_input("ID to edit: "))
            name = _input("New name: ")
            country = _input("New country: ")
            team = _input("New team: ")
            storage.edit_pilot(pid, name, country, team)
            print("Updated.")
        elif choice == "0":
            break


# --- Grand Prix ---

def grandprix_menu():
    while True:
        print("\n-- Grand Prix --")
        print("1. List  2. Add  3. Edit  0. Back")
        choice = _input("> ")
        if choice == "1":
            items = storage.list_grandprix()
            if not items:
                print("No grand prix.")
            for g in items:
                print(
                    f"  [{g.id}] {g.name} | {g.circuit} | "
                    f"{g.date} | winner: {g.winner or '-'}"
                )
        elif choice == "2":
            name = _input("Name: ")
            circuit = _input("Circuit: ")
            date = _input("Date (YYYY-MM-DD): ")
            winner = _input("Winner (optional): ")
            storage.add_grandprix(name, circuit, date, winner)
            print("Added.")
        elif choice == "3":
            gid = int(_input("ID to edit: "))
            name = _input("New name: ")
            circuit = _input("New circuit: ")
            date = _input("New date: ")
            winner = _input("New winner: ")
            storage.edit_grandprix(gid, name, circuit, date, winner)
            print("Updated.")
        elif choice == "0":
            break


# --- Main ---

def run():
    while True:
        print("\n=== F1 Manager ===")
        print("1. Teams  2. Pilots  3. Grand Prix  0. Exit")
        choice = _input("> ")
        if choice == "1":
            teams_menu()
        elif choice == "2":
            pilots_menu()
        elif choice == "3":
            grandprix_menu()
        elif choice == "0":
            break
