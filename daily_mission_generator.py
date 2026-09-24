import json
import random
from datetime import date, timedelta
from pathlib import Path

# ==============================
# Daily Mission Generator
# Sel Edition - Python Version
# ==============================

SAVE_FILE = Path(__file__).resolve().with_name("mission_save.json")

MISSIONS = {
    "easy": [
        {"name": "10 Min aufräumen", "xp": 10, "category": "Reset"},
        {"name": "Fenster öffnen + frische Luft", "xp": 10, "category": "Reset"},
        {"name": "Kurze Dusche + frische Kleidung", "xp": 10, "category": "Reset"},
        {"name": "10 Min spazieren", "xp": 10, "category": "Körper"},
        {"name": "1 Kabel ordentlich verlegen", "xp": 10, "category": "Setup"},
        {"name": "Bett machen", "xp": 10, "category": "Ordnung"},
    ],
    "medium": [
        {"name": "25 Min Bash / Python lernen", "xp": 25, "category": "Lernen"},
        {"name": "1 Schublade komplett organisieren", "xp": 25, "category": "Ordnung"},
        {"name": "Journal 10 Min ehrlich schreiben", "xp": 25, "category": "Journal"},
        {"name": "Rücken / Becken Mobility 20 Min", "xp": 25, "category": "Körper"},
        {"name": "Werkbank 30 Min sortieren", "xp": 25, "category": "Werkstatt"},
    ],
    "hard": [
        {"name": "2 Std nur 1 Projekt, kein Wechsel", "xp": 50, "category": "Fokus"},
        {"name": "Digital Detox 3 Std", "xp": 50, "category": "Ruhe"},
        {"name": "Zimmer komplett reinigen", "xp": 50, "category": "Reset"},
        {"name": "iPhone Reparatur Block", "xp": 50, "category": "Repair"},
        {"name": "Mini-Dokumentation für Notion schreiben", "xp": 50, "category": "Doku"},
    ],
}


def default_data():
    return {
        "xp": 0,
        "streak": 0,
        "last_day": "",
        "today_missions": {},
        "done": [],
        "history": [],
    }


def load_data():
    if SAVE_FILE.exists():
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_data()


def save_data(data):
    temporary_file = SAVE_FILE.with_suffix(SAVE_FILE.suffix + ".tmp")
    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    temporary_file.replace(SAVE_FILE)


def get_level(xp):
    if xp < 100:
        return 1
    if xp < 300:
        return 2
    if xp < 600:
        return 3
    return 4


def next_level_xp(xp):
    if xp < 100:
        return 100
    if xp < 300:
        return 300
    if xp < 600:
        return 600
    return 1000


def generate_daily_missions():
    return {
        "easy": random.choice(MISSIONS["easy"]),
        "medium": random.choice(MISSIONS["medium"]),
        "hard": random.choice(MISSIONS["hard"]),
    }


def check_new_day(data, today=None):
    today = today or date.today()
    today_string = today.isoformat()

    if data.get("last_day") != today_string:
        last_day = data.get("last_day", "")
        if last_day:
            try:
                previous_day = date.fromisoformat(last_day)
            except ValueError:
                data["streak"] = 0
            else:
                if previous_day == today - timedelta(days=1) and data.get("done"):
                    data["streak"] = data.get("streak", 0) + 1
                else:
                    data["streak"] = 0
        else:
            data["streak"] = 0

        data["last_day"] = today_string
        data["today_missions"] = generate_daily_missions()
        data["done"] = []
        save_data(data)


def show_status(data):
    xp = data["xp"]
    level = get_level(xp)
    next_xp = next_level_xp(xp)

    print("\n==============================")
    print(" DAILY MISSION GENERATOR ⚡")
    print("==============================")
    print(f"Level: {level}")
    print(f"XP: {xp} / {next_xp}")
    print(f"Streak: {data['streak']} Tage")
    print("==============================\n")


def show_missions(data):
    print("Heutige Missionen:\n")

    for index, key in enumerate(["easy", "medium", "hard"], start=1):
        mission = data["today_missions"][key]
        status = "✅" if key in data["done"] else "⬜"
        print(f"{index}. {status} {key.upper()} - {mission['name']}")
        print(f"   Kategorie: {mission['category']} | XP: {mission['xp']}\n")


def complete_mission(data):
    mapping = {"1": "easy", "2": "medium", "3": "hard"}
    choice = input("Welche Mission abschließen? 1/2/3: ").strip()

    if choice not in mapping:
        print("Ungültige Auswahl.")
        return

    key = mapping[choice]

    if key in data["done"]:
        print("Diese Mission ist schon erledigt.")
        return

    mission = data["today_missions"][key]
    data["xp"] += mission["xp"]
    data["done"].append(key)

    data["history"].insert(0, {
        "date": str(date.today()),
        "name": mission["name"],
        "xp": mission["xp"],
        "category": mission["category"],
    })

    data["history"] = data["history"][:20]
    save_data(data)

    print(f"Mission erledigt: {mission['name']} +{mission['xp']} XP")


def show_history(data):
    print("\nLetzte Missionen:\n")

    if not data["history"]:
        print("Noch keine Mission abgeschlossen.")
        return

    for item in data["history"][:10]:
        print(f"{item['date']} | {item['name']} | +{item['xp']} XP | {item['category']}")


def reset_all():
    confirm = input("Wirklich alles zurücksetzen? ja/nein: ").strip().lower()

    if confirm == "ja":
        save_data(default_data())
        print("Alles wurde zurückgesetzt.")
    else:
        print("Reset abgebrochen.")


def main():
    data = load_data()
    check_new_day(data)

    while True:
        show_status(data)
        show_missions(data)

        print("Menü:")
        print("1 = Mission abschließen")
        print("2 = Verlauf anzeigen")
        print("3 = Alles zurücksetzen")
        print("0 = Beenden")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            complete_mission(data)
        elif choice == "2":
            show_history(data)
        elif choice == "3":
            reset_all()
            data = load_data()
            check_new_day(data)
        elif choice == "0":
            print("Bis zur nächsten Mission. ⚡")
            break
        else:
            print("Ungültige Eingabe.")


if __name__ == "__main__":
    main()
