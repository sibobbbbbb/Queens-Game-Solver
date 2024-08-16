import tkinter as tk
from tkinter import filedialog, messagebox
from solver import QueensGameSolver
import random

class QueensGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Queens Game Solver")
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        
        self.open_button = tk.Button(self.frame, text="Open Input File", command=self.open_file)
        self.open_button.pack(pady=5)
        
        self.algorithm_var = tk.StringVar(value="backtracking")
        tk.Label(self.frame, text="Select Algorithm:").pack(pady=5)
        tk.Radiobutton(self.frame, text="Backtracking", variable=self.algorithm_var, value="backtracking").pack(anchor=tk.W)
        tk.Radiobutton(self.frame, text="Simulated Annealing", variable=self.algorithm_var, value="simulated_annealing").pack(anchor=tk.W)
        
        self.board_frame = tk.Frame(self.frame)
        self.board_frame.pack(pady=5)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            solver = QueensGameSolver(file_path)
            algorithm = self.algorithm_var.get()
            solution = solver.get_solution(algorithm)
            if solution:
                self.display_solution(solution, solver.board, solver.color_regions)
            else:
                messagebox.showerror("Error", "No solution found")
    
    def display_solution(self, solution, board, color_regions):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        colors = {}
        for region in color_regions:
            colors[region] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        
        for i in range(len(solution)):
            for j in range(len(solution[i])):
                color = colors.get(board[i][j], '#FFFFFF')
                label = tk.Label(self.board_frame, text=solution[i][j], width=4, height=2, 
                                 bg=color, relief="solid", font=("Helvetica", 16, "bold"))
                label.grid(row=i, column=j, padx=2, pady=2)

def create_gui():
    root = tk.Tk()
    app = QueensGameGUI(root)
    root.mainloop()
