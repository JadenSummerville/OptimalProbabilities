# 🧮 Optimal Probabilities Solver

A Python tool to compute **optimal mixed strategies** for two-player zero-sum games using **linear programming**.  
It calculates the AI’s strategy that minimizes the player’s maximum guaranteed payoff.

---

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![SciPy](https://img.shields.io/badge/scipy-required-green)

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `interface.py` | Terminal interface: collects the payoff matrix from the user and runs the solver. |
| `solver.py` | Reads `matrix.json`, solves the linear program, writes `results.json`. |
| `matrix.json` | Input file containing the user-provided payoff matrix. |
| `results.json` | Output file containing the AI’s optimal strategy and game value. |

---

## ⚡ Quick Usage

1. Run the interface:  

```bash
python interface.py
```

Then:

1. Input the number of **player choices** and **AI choices**.  
2. Enter the payoff matrix values row by row.  
3. The program outputs:  
   - **Game value**: expected payoff to the player if AI plays optimally  
   - **AI's optimal strategy**: probability for each choice

## 🧮 How the Solver Works (Conceptual Explanation)

This solver computes the AI’s **optimal mixed strategy** in a two-player zero-sum game.  

### 1. Representing the Game

The game is represented as a **payoff matrix**:

- **Rows** correspond to the **player's choices**.  
- **Columns** correspond to the **AI's choices**.  
- Each cell contains the **player's gain** if that combination of choices is selected.  

For example, a 2x3 game:

| Player \ AI | AI Choice 0 | AI Choice 1 | AI Choice 2 |
|------------|------------|------------|------------|
| Player Choice 0 | 2 | 0 | -1 |
| Player Choice 1 | -1 | 0 | 1 |

This matrix shows all possible outcomes for each combination of choices.

---

### 2. AI Probabilities and Game Value

Instead of picking a single column, the AI uses a **probability distribution** over its choices:

- `p_j` — probability that the AI picks column `j`  
- Probabilities are non-negative and sum to 1  

We choose a **randomized strategy** because:

- We assume the player knows the AI’s probabilities.  
- If the AI always picked a single choice, the player could exploit it.  
- By randomizing, the AI ensures the player cannot gain more than the game value `v` regardless of their choice.  

The **game value**, `v`, is the expected payoff for the player if both sides play optimally.

---

### 3. Constraints

Each player choice imposes a constraint on `v`:

- For a given choice, the expected payoff is calculated using the AI probabilities.  
- Geometrically, each choice defines a **hyperplane** in the space of AI probabilities, where each point on the hyperplane represents the expected payoff for that choice at those probabilities.  
- Since the solver **minimizes `v`**, `v` cannot be lower than the expected payoff for the **best player choice** at the given probabilities.  
- There are no constraints forcing `v` above these hyperplane (choices) and we minimize `v` so it cannot be greater than the expected payoff for the **best player choice**.  
- As a result, `v` at any AI probability distribution is always **equal to the expected payoff of the player’s optimal choice**, and the solver adjusts probabilities to minimize this value.

---

### 4. Optimization Intuition

- Each player choice acts as a constraint, representing the expected payoff if that choice is taken.  
- The AI cannot adapt after the player chooses, so the player always selects the choice with the highest expected payoff.  
- The solver finds the **probabilities that minimize `v`** while respecting all constraints.  
- Geometrically, this corresponds to the **lowest point above all floors** formed by the constraints in probability space.

---

This approach guarantees:

1. AI probabilities are valid (non-negative and sum to 1).  
2. The player’s optimal choice is accounted for.  
3. The game value `v` is minimized given the player’s best responses.
