import json
from scipy.optimize import linprog

def solve_game(outcomeMatrix):
    if len(outcomeMatrix) == 0 or len(outcomeMatrix[0]) == 0:
        raise ValueError("Outcome matrix is not the right size.")

    rows = len(outcomeMatrix)
    cols = len(outcomeMatrix[0])

    # Variables: [v, p1, p2, ..., p_cols]
    # Objective: minimize v
    c = [1] + [0] * cols

    # Equality: sum(p_j) = 1
    A_eq = [[0] + [1] * cols]
    b_eq = [1]

    # Inequalities: sum_j a_ij * p_j - v <= 0   (for each player choice i)
    A_ub = []
    b_ub = []
    for i in range(rows):
        row = [-1]  # coefficient for v
        row.extend(outcomeMatrix[i])  # coefficients for probabilities
        A_ub.append(row)
        b_ub.append(0)

    # Bounds: v free, p_j >= 0
    bounds = [(None, None)] + [(0, None)] * cols

    result = linprog(
        c, A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq,
        bounds=bounds, method="highs"
    )

    data = {}
    if result.success:
        data["value"] = result.x[0]
        data["probabilities"] = result.x[1:].tolist()
        data["success"] = True
    else:
        data["success"] = False

    with open("results.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Load matrix passed from user input file
    with open("matrix.json", "r") as f:
        matrix = json.load(f)
    solve_game(matrix)
