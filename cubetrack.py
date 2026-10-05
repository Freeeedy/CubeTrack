import json
import os
import time
from datetime import datetime

FILE = "solves.json"


def load_solves():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)


def save_solve(solve_time, clean):
    solves = load_solves()

    solves.append({
        "time": solve_time,
        "clean": clean,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(FILE, "w") as f:
        json.dump(solves, f, indent=4)


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{minutes:02d}:{seconds:05.2f}"


def average(solves):
    if not solves:
        return 0

    return sum(s["time"] for s in solves) / len(solves)


def display_session(session):
    all_solves = load_solves()

    if not all_solves:
        return

    best = min(s["time"] for s in all_solves)
    clean_solves = [s for s in all_solves if s["clean"]]
    best_clean = min((s["time"] for s in clean_solves), default=0)

    print("BEST")
    print(format_time(best))

    print("BEST CLEAN")
    print(format_time(best_clean))

    print()

    print("SESSION")
    print("────────────────────")

    start_number = len(all_solves) - len(session) + 1

    for i, solve in enumerate(session, start_number):
        mark = "✓" if solve["clean"] else "✗"
        print(f"#{i} {format_time(solve['time'])} {mark}")


    print("SESSION AVG")
    print(format_time(average(session)))

    print("OVERALL AVG")
    print(format_time(average(all_solves)))


solves = load_solves()
session = []

while True:
    print("\nPress Enter to start...")
    input()

    start_time = time.perf_counter()

    print("Solving...")
    input()

    solve_time = time.perf_counter() - start_time

    clean_input = input(
        f"\nSolve: {format_time(solve_time)}\n"
        "Clean solve? [Y/N]: "
    )

    clean = clean_input.lower() == "y"

    solve = {
        "time": solve_time,
        "clean": clean,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    session.append(solve)
    save_solve(solve_time, clean)

    print("\n")
    display_session(session)

    if input("\nPress Enter for another solve, or type Q to quit: ").lower() == "q":
        break