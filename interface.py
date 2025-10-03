import json
import subprocess

def get_matrix():
    rows = int(input("How many choices does the PLAYER have? "))
    cols = int(input("How many choices does the AI have? "))

    matrix = []
    print("\nEnter the payoff values row by row (PLAYER vs AI):")
    for i in range(rows):
        row = []
        for j in range(cols):
            val = float(input(f"Payoff for Player choosing {i}, AI choosing {j}: "))
            row.append(val)
        matrix.append(row)
    return matrix

def save_matrix(matrix):
    with open("matrix.json", "w") as f:
        json.dump(matrix, f)

def load_results():
    with open("results.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    matrix = get_matrix()
    save_matrix(matrix)

    subprocess.run(["python", "solver.py"])

    results = load_results()

    print("\n=== Game Results ===")
    if results["success"]:
        print(f"Game value (expected payoff to the player): {results['value']:.4f}")
        print("AI's optimal strategy (probabilities for each choice):")
        for i, p in enumerate(results["probabilities"]):
            print(f"  Choice {i}: {p:.4f}")
    else:
        print("No solution found.")
