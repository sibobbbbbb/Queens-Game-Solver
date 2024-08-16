import math
import random

class QueensGameSolver:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dimensions, self.num_colors, self.board, self.color_regions = self.read_input_file(file_path)
        self.solution = [['.' for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])]
    
    def read_input_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        dimensions = list(map(int, lines[0].split()))
        num_colors = int(lines[1].strip())
        board = [line.strip().split() for line in lines[2:]]

        color_regions = {}
        for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                if board[i][j] not in color_regions:
                    color_regions[board[i][j]] = []
                color_regions[board[i][j]].append((i, j))
        
        return dimensions, num_colors, board, color_regions
    
    def is_valid(self, row, col):
        for i in range(self.dimensions[0]):
            if self.solution[row][i] == 'Q' or self.solution[i][col] == 'Q':
                return False
        
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                if (i + j == row + col or i - j == row - col) and self.solution[i][j] == 'Q':
                    return False
        
        for color in self.color_regions:
            if (row, col) in self.color_regions[color]:
                for r, c in self.color_regions[color]:
                    if self.solution[r][c] == 'Q':
                        return False
        
        return True
    
    def solve_backtracking(self, color_idx=0):
        if color_idx >= len(self.color_regions):
            return True
        
        color = list(self.color_regions.keys())[color_idx]
        for row, col in self.color_regions[color]:
            if self.is_valid(row, col):
                self.solution[row][col] = 'Q'
                if self.solve_backtracking(color_idx + 1):
                    return True
                self.solution[row][col] = '.'
        
        return False
    
    def solve_simulated_annealing(self, initial_temp=1000, cooling_rate=0.99, max_iterations=10000):
        # Initialize a random solution
        self.solution = [['.' for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])]
        for region in self.color_regions.values():
            r, c = random.choice(region)
            self.solution[r][c] = 'Q'
        
        current_cost = self.calculate_cost()
        T = initial_temp
        
        for _ in range(max_iterations):
            if current_cost == 0:
                return True
            
            # Select a random region and move the queen within that region
            region = random.choice(list(self.color_regions.values()))
            current_pos = [(r, c) for r, c in region if self.solution[r][c] == 'Q'][0]
            new_pos = random.choice([pos for pos in region if pos != current_pos])
            
            # Apply the move
            self.solution[current_pos[0]][current_pos[1]] = '.'
            self.solution[new_pos[0]][new_pos[1]] = 'Q'
            new_cost = self.calculate_cost()
            
            # Accept or reject the new solution
            delta_cost = new_cost - current_cost
            if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / T):
                current_cost = new_cost
            else:
                # Revert the move
                self.solution[new_pos[0]][new_pos[1]] = '.'
                self.solution[current_pos[0]][current_pos[1]] = 'Q'
            
            # Cool down the temperature
            T *= cooling_rate
        
        return current_cost == 0
    
    def calculate_cost(self):
        """Calculate the number of conflicting queens."""
        conflicts = 0
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                if self.solution[i][j] == 'Q':
                    conflicts += sum(self.solution[i][k] == 'Q' for k in range(self.dimensions[1]) if k != j)
                    conflicts += sum(self.solution[k][j] == 'Q' for k in range(self.dimensions[0]) if k != i)
                    conflicts += sum(self.solution[i + k][j + k] == 'Q' for k in range(1, min(self.dimensions[0] - i, self.dimensions[1] - j)))
                    conflicts += sum(self.solution[i - k][j - k] == 'Q' for k in range(1, min(i + 1, j + 1)))
                    conflicts += sum(self.solution[i + k][j - k] == 'Q' for k in range(1, min(self.dimensions[0] - i, j + 1)))
                    conflicts += sum(self.solution[i - k][j + k] == 'Q' for k in range(1, min(i + 1, self.dimensions[1] - j)))
        return conflicts

    def get_solution(self, algorithm='backtracking'):
        if algorithm == 'backtracking':
            if self.solve_backtracking():
                return self.solution
            else:
                return None
        elif algorithm == 'simulated_annealing':
            if self.solve_simulated_annealing():
                return self.solution
            else:
                return None