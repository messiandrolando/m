import tkinter as tk
from tkinter import messagebox
import random

class CaroGame:
    def __init__(self, root):
        self.root = root
        self.language = tk.StringVar(value="vi")
        self.load_language_resources()
        
        # Game state
        self.current_player = "X"
        self.board = [["" for _ in range(5)] for _ in range(5)]
        self.vs_computer = tk.BooleanVar(value=False)
        self.difficulty = tk.StringVar(value="easy")
        
        # Score tracking
        self.scores = {
            "X": 0,
            "O": 0,
            "draw": 0
        }

        # GUI setup
        self.colors = {
            "background": "#ffffff",
            "cell": "#e0f7fa",
            "border": "#80deea",
            "win": "#2ecc71",
            "X_color": "#2980b9",
            "O_color": "#c0392b",
            "score_bg": "#ecf0f1"
        }
        
        self.initialize_ui()
        self.update_ui()

    def load_language_resources(self):
        self.lang = {
            "vi": {
                "title": "CỜ CARO ",
                "author": "Tác giả: Bùi Nguyên Anh Tuấn - học sinh FPT",
                "language": ":", 
                "mode": "Chế độ:",
                "pvp": "2 Người chơi",
                "pve": "Chơi với máy",
                "difficulty": "Độ khó:",
                "easy": "Dễ",
                "medium": "Trung bình",
                "hard": "Khó",
                "expert": "Chuyên gia",
                "status": "Lượt của {}",
                "help": "Trợ giúp",
                "restart": "Chơi lại",
                "quit": "Thoát",
                "win": "{} chiến thắng!",
                "draw": "Hòa!",
                "help_text": """Luật chơi Cờ Caro 5x5:
1. Hai người luân phiên đánh X và O
2. Thắng khi có 5 quân liên tiếp (ngang/dọc/chéo)
3. Độ khó máy:
   - Dễ: Đi ngẫu nhiên
   - Trung bình: 50% phòng thủ
   - Khó: Phòng thủ chủ động
   - Chuyên gia: Tấn công chiến lược
   - bấm nút màu đỏ để thoát thẳng game
   - bấm nút màu vàng để xem lịch sử trận đấu""",
                "score_title": "Lịch Sử Trận Đấu",
                "player_X": "Người chơi X:",
                "player_O": "Người chơi O:",
                "draws": "Số trận hòa:",
                "reset_scores": "Xóa điểm",
                "exit_confirm": "Bạn có chắc muốn thoát?",
                "exit_title": "Xác nhận thoát"
            },
            "en": {
                "title": "CARO CHESS",
                "author": "Author:bui Ngyen Anh Tuan - Student of FPT",
                "language": ":",
                "mode": "Mode:",
                "pvp": "2 Players",
                "pve": "vs Computer",
                "difficulty": "Difficulty:",
                "easy": "Easy",
                "medium": "Medium",
                "hard": "Hard",
                "expert": "Expert",
                "status": "{}'s turn",
                "help": "Help",
                "restart": "Restart",
                "quit": "Quit",
                "win": "{} wins!",
                "draw": "Draw!",
                "help_text": """Caro 5x5 Rules:
1. Players take turns placing X and O
2. Win by getting 5 in a row (any direction)
3. AI difficulty:
   - Easy: Random moves
   - Medium: 50% defense
   - Hard: Active defense
   - Expert: Strategic attacks
   - press red button to exit game
   - press yellow button to view match history""",
                "score_title": "Match History",
                "player_X": "Player X:",
                "player_O": "Player O:",
                "draws": "Draws:",
                "reset_scores": "Reset Scores",
                "exit_confirm": "Are you sure you want to quit?",
                "exit_title": "Exit Confirmation"
            }
        }

    def initialize_ui(self):
        # Language selection
        lang_frame = tk.Frame(self.root, bg=self.colors["background"])
        lang_frame.pack(pady=5)
        
        tk.Label(lang_frame, text=self.lang["vi"]["language"],
                bg=self.colors["background"]).pack(side=tk.LEFT)
        tk.Radiobutton(lang_frame, text="VI", variable=self.language, value="vi",
                      command=self.update_ui, bg=self.colors["background"]).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(lang_frame, text="EN", variable=self.language, value="en",
                      command=self.update_ui, bg=self.colors["background"]).pack(side=tk.LEFT, padx=5)

        # Title
        self.title_label = tk.Label(
            self.root,
            font=("Arial", 20, "bold"),
            fg="#2c3e50",
            bg=self.colors["background"]
        )
        self.title_label.pack(pady=10)

        # Author
        self.author_label = tk.Label(
            self.root,
            font=("Arial", 10),
            fg="#7f8c8d",
            bg=self.colors["background"]
        )
        self.author_label.pack(pady=2)

        # Game mode
        self.mode_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.mode_label = tk.Label(self.mode_frame, font=("Arial", 12), bg=self.colors["background"])
        self.pvp_btn = tk.Radiobutton(self.mode_frame, variable=self.vs_computer, value=False,
                                    command=self.reset_game, bg=self.colors["background"])
        self.pve_btn = tk.Radiobutton(self.mode_frame, variable=self.vs_computer, value=True,
                                    command=self.reset_game, bg=self.colors["background"])

        # Difficulty
        self.difficulty_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.difficulty_label = tk.Label(self.difficulty_frame, bg=self.colors["background"])
        self.easy_btn = tk.Radiobutton(self.difficulty_frame, variable=self.difficulty, value="easy", 
                                     bg=self.colors["background"])
        self.medium_btn = tk.Radiobutton(self.difficulty_frame, variable=self.difficulty, value="medium", 
                                       bg=self.colors["background"])
        self.hard_btn = tk.Radiobutton(self.difficulty_frame, variable=self.difficulty, value="hard", 
                                     bg=self.colors["background"])
        self.expert_btn = tk.Radiobutton(self.difficulty_frame, variable=self.difficulty, value="expert", 
                                       bg=self.colors["background"])

        # Game board
        board_frame = tk.Frame(self.root, bg=self.colors["border"])
        board_frame.pack(pady=10)

        self.cells = []
        for row in range(5):
            cell_row = []
            for col in range(5):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 20),
                    width=3,
                    height=1,
                    relief="flat",
                    bg=self.colors["cell"],
                    fg="white",
                    highlightbackground=self.colors["border"],
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2, ipadx=5, ipady=5)
                cell_row.append(btn)
            self.cells.append(cell_row)

        # Status
        self.status_label = tk.Label(
            self.root,
            font=("Arial", 14),
            fg=self.colors["X_color"],
            bg=self.colors["background"]
        )
        self.status_label.pack(pady=5)

        # Scoreboard
        self.score_frame = tk.Frame(self.root, bg=self.colors["score_bg"], padx=10, pady=5)
        self.score_frame.pack(pady=10, fill=tk.X)
        
        self.score_title = tk.Label(self.score_frame, font=("Arial", 12, "bold"), bg=self.colors["score_bg"])
        self.score_title.pack(anchor=tk.W)
        
        self.score_X_label = tk.Label(self.score_frame, bg=self.colors["score_bg"])
        self.score_X_label.pack(anchor=tk.W)
        
        self.score_O_label = tk.Label(self.score_frame, bg=self.colors["score_bg"])
        self.score_O_label.pack(anchor=tk.W)
        
        self.draw_label = tk.Label(self.score_frame, bg=self.colors["score_bg"])
        self.draw_label.pack(anchor=tk.W)

        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.colors["background"])
        control_frame.pack(pady=10)

        self.help_btn = tk.Button(
            control_frame,
            command=self.show_help,
            bg="#27ae60",
            fg="white"
        )
        self.help_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            control_frame,
            command=self.reset_game,
            bg="#3498db",
            fg="white"
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.reset_score_btn = tk.Button(
            control_frame,
            command=self.reset_scores,
            bg="#f39c12",
            fg="white"
        )
        self.reset_score_btn.pack(side=tk.LEFT, padx=5)

        self.quit_btn = tk.Button(
            control_frame,
            command=self.root.quit,
            bg="#e74c3c",
            fg="white"
        )
        self.quit_btn.pack(side=tk.LEFT, padx=5)

        self.root.configure(bg=self.colors["background"])

        self.quit_btn = tk.Button(
            control_frame,
            command=self.confirm_exit,
            bg="#e74c3c",
            fg="white"
        )
        
    def confirm_exit(self):
        lang = self.lang[self.language.get()]
        response = messagebox.askyesno(lang["exit_title"], lang["exit_confirm"])
        if response:
            self.root.quit()
            
    def update_ui(self):
        lang = self.lang[self.language.get()]
        self.root.title(lang["title"])
        self.title_label.config(text=lang["title"])
        self.author_label.config(text=lang["author"])
        
        # Update mode section
        self.mode_label.config(text=lang["mode"])
        self.pvp_btn.config(text=lang["pvp"])
        self.pve_btn.config(text=lang["pve"])
        self.mode_frame.pack(pady=5)
        self.mode_label.pack(side=tk.LEFT)
        self.pvp_btn.pack(side=tk.LEFT, padx=5)
        self.pve_btn.pack(side=tk.LEFT, padx=5)
        
        # Update difficulty section
        self.difficulty_label.config(text=lang["difficulty"])
        self.easy_btn.config(text=lang["easy"])
        self.medium_btn.config(text=lang["medium"])
        self.hard_btn.config(text=lang["hard"])
        self.expert_btn.config(text=lang["expert"])
        self.difficulty_frame.pack(pady=5)
        self.difficulty_label.pack(side=tk.LEFT)
        self.easy_btn.pack(side=tk.LEFT, padx=5)
        self.medium_btn.pack(side=tk.LEFT, padx=5)
        self.hard_btn.pack(side=tk.LEFT, padx=5)
        self.expert_btn.pack(side=tk.LEFT, padx=5)
        
        # Update status
        self.status_label.config(text=lang["status"].format(self.current_player))
        
        # Update control buttons
        self.help_btn.config(text=lang["help"])
        self.reset_btn.config(text=lang["restart"])
        self.reset_score_btn.config(text=lang["reset_scores"])
        self.quit_btn.config(text=lang["quit"])
        
        # Update scoreboard
        self.score_title.config(text=lang["score_title"])
        self.score_X_label.config(text=f"{lang['player_X']} {self.scores['X']}")
        self.score_O_label.config(text=f"{lang['player_O']} {self.scores['O']}")
        self.draw_label.config(text=f"{lang['draws']} {self.scores['draw']}")                                                        

    def make_move(self, row, col):
        if self.board[row][col] != "" or self.check_winner()[0]:
            return

        self.board[row][col] = self.current_player
        color = self.colors["X_color"] if self.current_player == "X" else self.colors["O_color"]
        self.cells[row][col].config(text=self.current_player, fg=color)

        winner, win_pos = self.check_winner()
        if winner:
            self.scores[winner] += 1
            self.highlight_win(win_pos)
            lang = self.lang[self.language.get()]
            messagebox.showinfo(lang["title"], lang["win"].format(winner))
            self.update_ui()
            return

        if self.check_draw():
            self.scores["draw"] += 1
            lang = self.lang[self.language.get()]
            messagebox.showinfo(lang["title"], lang["draw"])
            self.update_ui()
            return

        self.switch_player()
        
        if self.vs_computer.get() and self.current_player == "O":
            self.root.after(500, self.computer_move)

    def computer_move(self):
        difficulty = self.difficulty.get()
        
        if difficulty == "easy":
            move = self.random_move()
        elif difficulty == "medium":
            move = (self.find_winning_move("O") 
                    or (random.random() < 0.5 and self.find_winning_move("X")) 
                    or self.random_move())
        elif difficulty == "hard":
            move = (self.find_winning_move("O") 
                    or self.find_winning_move("X") 
                    or self.random_move())
        elif difficulty == "expert":
            move = (self.find_winning_move("O") 
                    or self.find_winning_move("X") 
                    or self.best_move() 
                    or self.random_move())
            
        if move:
            self.make_move(*move)

    def find_winning_move(self, player):
        for row in range(5):
            for col in range(5):
                if self.board[row][col] == "":
                    self.board[row][col] = player
                    if self.check_winner()[0] == player:
                        self.board[row][col] = ""
                        return (row, col)
                    self.board[row][col] = ""
        return None

    def random_move(self):
        empty = [(row, col) for row in range(5) for col in range(5) if self.board[row][col] == ""]
        return random.choice(empty) if empty else None

    def best_move(self):
        priority = [
            (2, 2), (0, 0), (0, 4), (4, 0), (4, 4),
            (1, 1), (1, 3), (3, 1), (3, 3), 
        ]
        
        for pos in priority:
            if self.board[pos[0]][pos[1]] == "":
                return pos
        return self.random_move()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        lang = self.lang[self.language.get()]
        self.status_label.config(text=lang["status"].format(self.current_player))

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(5):
            for col in range(5):
                if self.board[row][col] == "":
                    continue
                symbol = self.board[row][col]
                for dx, dy in directions:
                    if (row + 4*dx < 5) and (col + 4*dy >= 0) and (col + 4*dy < 5):
                        if all(self.board[row + k*dx][col + k*dy] == symbol for k in range(5)):
                            return (symbol, [(row + k*dx, col + k*dy) for k in range(5)])
        return (None, [])

    def highlight_win(self, positions):
        for row, col in positions:
            self.cells[row][col].config(bg=self.colors["win"])

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(5)] for _ in range(5)]
        for row in self.cells:
            for cell in row:
                cell.config(text="", bg=self.colors["cell"])    
        lang = self.lang[self.language.get()]
        self.status_label.config(text=lang["status"].format(self.current_player))

    def show_help(self):
        lang = self.lang[self.language.get()]
        messagebox.showinfo(lang["help"], lang["help_text"])

    def reset_scores(self):
        self.scores = {"X": 0, "O": 0, "draw": 0}
        self.update_ui()


if __name__ == "__main__":
    root = tk.Tk()
    game = CaroGame(root)
    root.protocol("WM_DELETE_WINDOW", game.confirm_exit)  
    root.mainloop()
