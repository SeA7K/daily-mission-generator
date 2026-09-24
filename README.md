# Daily Mission Generator ⚡

RPG-style daily mission tracker mit XP und Streak-System.

## Features

- 3 tägliche Missionen (Easy / Medium / Hard)
- XP System mit Level-Aufstieg
- Streak-Tracking
- Verlauf der letzten 20 Missionen
- Automatischer Tageswechsel

## Start

```bash
python daily_mission_generator.py
```

## Setup

Benötigt Python 3.10 oder neuer. Beim ersten Start wird `mission_save.json`
neben dem Skript angelegt. Die Datei enthält den persönlichen Spielstand und
wird nicht mit Git eingecheckt.

## Missionen
- Easy → 10 XP
- Medium → 25 XP
- Hard → 50 XP

## Level
- Level 1: 0–99 XP
- Level 2: 100–299 XP
- Level 3: 300–599 XP
- Level 4: 600+ XP
