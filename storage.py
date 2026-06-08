import json
import os
from models import Team, Pilot, GrandPrix

DATA_FILE = "data.json"

_DEFAULTS = {"teams": [], "pilots": [], "grandprix": []}

#Читання
def load():
    if not os.path.exists(DATA_FILE):
        return dict(_DEFAULTS)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


#Запис
def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


#Yfcnegybq ID від вже записаного
def _next_id(items):
    return max((i["id"] for i in items), default=0) + 1


#Команди
def add_team(name, country):
    data = load()
    team = {"id": _next_id(data["teams"]), "name": name, "country": country}
    data["teams"].append(team)
    save(data)


def list_teams():
    return [Team(**t) for t in load()["teams"]]


def edit_team(team_id, name, country):
    data = load()
    for t in data["teams"]:
        if t["id"] == team_id:
            t["name"] = name
            t["country"] = country
            break
    save(data)


#Пілоти
def add_pilot(name, country, team):
    data = load()
    pilot = {
        "id": _next_id(data["pilots"]),
        "name": name,
        "country": country,
        "team": team,
    }
    data["pilots"].append(pilot)
    save(data)


def list_pilots():
    return [Pilot(**p) for p in load()["pilots"]]


def edit_pilot(pilot_id, name, country, team):
    data = load()
    for p in data["pilots"]:
        if p["id"] == pilot_id:
            p["name"] = name
            p["country"] = country
            p["team"] = team
            break
    save(data)


#Гран-прі
def add_grandprix(name, circuit, date, winner=""):
    data = load()
    gp = {
        "id": _next_id(data["grandprix"]),
        "name": name,
        "circuit": circuit,
        "date": date,
        "winner": winner,
    }
    data["grandprix"].append(gp)
    save(data)


def list_grandprix():
    return [GrandPrix(**g) for g in load()["grandprix"]]


def edit_grandprix(gp_id, name, circuit, date, winner):
    data = load()
    for g in data["grandprix"]:
        if g["id"] == gp_id:
            g["name"] = name
            g["circuit"] = circuit
            g["date"] = date
            g["winner"] = winner
            break
    save(data)
