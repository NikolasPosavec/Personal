import tkinter as tk
from tkinter import ttk

class College:
    def __init__(self, name, size, cs_rank, campus_rating):
        self.name = name
        self.size = size
        self.cs_rank = cs_rank
        self.campus_rating = campus_rating  # Now 1=best, 10=worst

    def score(self, weights, stat_ranges):
        def normalize(val, min_val, max_val):
            return (val - min_val) / (max_val - min_val) if max_val != min_val else 0

        # All metrics now follow: smaller is better (1=best, 10=worst)
        size_score = 1 - normalize(self.size, *stat_ranges['size'])
        cs_score = 1 - normalize(self.cs_rank, *stat_ranges['cs_rank'])
        campus_score = 1 - normalize(self.campus_rating, *stat_ranges['campus'])

        # Apply weights and ensure total is out of 3 points
        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0
            
        weighted_sum = (
            weights['size'] * size_score +
            weights['cs'] * cs_score +
            weights['campus'] * campus_score
        )
        
        # Normalize to 3-point scale
        return (weighted_sum / total_weight) * 3

# Updated schools with campus ratings now on 1-10 scale (1=best, 10=worst)
colleges = [
    College("Clemson", 21000, 80, 4),  # Previously 7 → now 4 (better)
    College("UGA", 31000, 80, 4),      # Previously 7 → now 4
    College("University of South Carolina", 27000, 110, 4),  # 7→4
    College("Case Western Reserve", 5500, 71, 5),  # 6→5
    College("Fairfield", 4400, 200, 5),  # 6→5
    College("Miami University (Oxford)", 17000, 200, 4),  # 7→4
    College("NC State", 26000, 51, 5),  # 6→5
    College("Penn State", 47000, 39, 5),  # 6→5
    College("Ohio State", 46000, 35, 4),  # 7→4
    College("University of Delaware", 18500, 71, 6),  # 5→6 (worse)
    College("UMD", 30000, 16, 3),  # 8→3 (much better)
    College("Villanova", 7000, 150, 1),  # 10→1 (best possible)
    College("Virginia Tech", 29000, 35, 1),  # 10→1 (best possible)
    College("Pitt", 19000, 51, 4)  # 7→4
]

def get_stat_ranges(colleges):
    return {
        'size': (min(c.size for c in colleges), max(c.size for c in colleges)),
        'cs_rank': (min(c.cs_rank for c in colleges), max(c.cs_rank for c in colleges)),
        'campus': (min(c.campus_rating for c in colleges), max(c.campus_rating for c in colleges)),
    }

def rank_colleges():
    weights = {
        'size': float(size_weight.get()),
        'cs': float(cs_weight.get()),
        'campus': float(campus_weight.get())
    }
    stat_ranges = get_stat_ranges(colleges)
    ranked = sorted(colleges, key=lambda c: c.score(weights, stat_ranges), reverse=True)
    result_box.delete(0, tk.END)
    for i, college in enumerate(ranked, 1):
        result_box.insert(tk.END, f"{i}. {college.name} (Score: {college.score(weights, stat_ranges):.2f}/3.00)")

# GUI Setup
root = tk.Tk()
root.title("College Ranker")

tk.Label(root, text="Weight for Size (smaller = better):").grid(row=0, column=0)
size_weight = ttk.Entry(root)
size_weight.insert(0, "1")
size_weight.grid(row=0, column=1)

tk.Label(root, text="Weight for CS Ranking (smaller = better):").grid(row=1, column=0)
cs_weight = ttk.Entry(root)
cs_weight.insert(0, "1")
cs_weight.grid(row=1, column=1)

tk.Label(root, text="Weight for Campus Rating (1=best, 10=worst):").grid(row=2, column=0)
campus_weight = ttk.Entry(root)
campus_weight.insert(0, "1")
campus_weight.grid(row=2, column=1)

rank_button = ttk.Button(root, text="Rank Colleges", command=rank_colleges)
rank_button.grid(row=3, column=0, columnspan=2, pady=10)

result_box = tk.Listbox(root, width=60, height=15)
result_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()