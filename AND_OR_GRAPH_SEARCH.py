import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Nâng giới hạn đệ quy tối đa của Python để hỗ trợ thuật toán đi sâu
sys.setrecursionlimit(100000)

# --- CẤU HÌNH TRẠNG THÁI MẶC ĐỊNH ---
INITIAL_STATE = [1, 2, 3, 4, 0, 5, 7, 8, 6] 
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# --- 1. CÁC HÀM CƠ SỞ 8-PUZZLE ---
def get_actions(state):
    actions = []
    z = state.index(0)
    r, c = z // 3, z % 3
    if r > 0: actions.append('UP')
    if r < 2: actions.append('DOWN')
    if c > 0: actions.append('LEFT')
    if c < 2: actions.append('RIGHT')
    return actions

def get_results(state, action):
    z = state.index(0)
    t = z
    if action == 'UP': t = z - 3
    elif action == 'DOWN': t = z + 3
    elif action == 'LEFT': t = z - 1
    elif action == 'RIGHT': t = z + 1
    
    new_state = list(state)
    new_state[z], new_state[t] = new_state[t], new_state[z]
    return [new_state]


# --- 2. LỚP CHỨA THUẬT TOÁN (GHI NHẬN LOG THEO TỪNG BƯỚC DUYỆT) ---
class PuzzleSolver:
    def __init__(self):
        self.explored = []      # Đổi thành list để giữ nguyên thứ tự duyệt tuyến tính
        self.explored_set = set()
        self.logs = []
        self.goal = []

    def solve_and_or_graph_search(self, init_state, goal_state):
        self.goal = goal_state
        self.explored = []
        self.explored_set = set()
        self.logs = []
        plan = self.or_search(init_state, [])
        return {"logs": self.logs, "plan": plan}

    def or_search(self, state, path):
        state_tuple = tuple(state)
        if state_tuple not in self.explored_set:
            self.explored_set.add(state_tuple)
            self.explored.append(state)
            
        if state == self.goal:
            self.logs.append({
                'state': list(state), 
                'action': 'STOP', 
                'frontier': [], 
                'explored': list(self.explored)
            })
            return []
            
        if state in path:
            return "failure"
            
        for action in get_actions(state):
            result_states = get_results(state, action)
            
            # Lưu vết thông tin tại thời điểm duyệt nhánh này
            self.logs.append({
                'state': list(state), 
                'action': action, 
                'frontier': [list(r) for r in result_states], 
                'explored': list(self.explored)
            })
            
            plan = self.and_search(result_states, path + [state])
            if plan != "failure":
                return [action, plan]
                
        return "failure"

    def and_search(self, states, path):
        plans = {}
        for s in states:
            plan_s = self.or_search(s, path)
            if plan_s == "failure":
                return "failure"
            plans[str(s)] = plan_s
        return plans


# --- 3. GIAO DIỆN ĐỒ HỌA TKINTER ---
class App8Puzzle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI 8-Puzzle Visualizer (Pure AND-OR Graph Search)")
        self.geometry("1200x780")
        self.configure(bg="#f0f2f5")

        self.history_states = []
        self.timeline_logs = []
        self.optimal_actions = []
        self.current_index = 0
        self.is_playing = False
        self.play_job = None
        
        self.init_state_cfg = list(INITIAL_STATE)
        self.goal_state_cfg = list(GOAL_STATE)

        self.create_widgets()
        self.init_blank_board()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_panel = ttk.Frame(main_frame, width=340)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        cfg_frame = ttk.LabelFrame(left_panel, text=" ⚙️ Cấu Hình Bài Toán ", padding=10)
        cfg_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(cfg_frame, text="Chọn thuật toán giải:").pack(anchor=tk.W)
        self.cbo_algo = ttk.Combobox(cfg_frame, state="readonly")
        self.cbo_algo['values'] = ("AND-OR Graph Search",) 
        self.cbo_algo.current(0)
        self.cbo_algo.pack(fill=tk.X, pady=(2, 8))

        ttk.Label(cfg_frame, text="Trạng thái đầu (cách bởi dấu cách):").pack(anchor=tk.W)
        self.ent_init = ttk.Entry(cfg_frame)
        self.ent_init.insert(0, " ".join(map(str, INITIAL_STATE)))
        self.ent_init.pack(fill=tk.X, pady=(2, 8))

        ttk.Label(cfg_frame, text="Trạng thái đích (cách bởi dấu cách):").pack(anchor=tk.W)
        self.ent_goal = ttk.Entry(cfg_frame)
        self.ent_goal.insert(0, " ".join(map(str, GOAL_STATE)))
        self.ent_goal.pack(fill=tk.X, pady=(2, 10))

        btn_submit = ttk.Button(cfg_frame, text="Cập Nhật Cấu Hình", command=self.submit_config)
        btn_submit.pack(fill=tk.X)

        self.board_frame = ttk.Frame(left_panel, padding=10)
        self.board_frame.pack(pady=5)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text="", font=("Segoe UI", 24, "bold"), width=5, height=2, relief="groove")
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(btn)

        ctrl_frame = ttk.Frame(left_panel)
        ctrl_frame.pack(fill=tk.X, pady=10)
        for i in range(5): ctrl_frame.columnconfigure(i, weight=1)

        self.btn_go = ttk.Button(ctrl_frame, text="GO", command=self.play)
        self.btn_go.grid(row=0, column=0, padx=2, sticky="ew")

        self.btn_pause = ttk.Button(ctrl_frame, text="Pause", command=self.pause, state=tk.DISABLED)
        self.btn_pause.grid(row=0, column=1, padx=2, sticky="ew")

        self.btn_prev = ttk.Button(ctrl_frame, text="Prev", command=self.preview, state=tk.DISABLED)
        self.btn_prev.grid(row=0, column=2, padx=2, sticky="ew")

        self.btn_next = ttk.Button(ctrl_frame, text="Next", command=self.next_step)
        self.btn_next.grid(row=0, column=3, padx=2, sticky="ew")

        self.btn_reset = ttk.Button(ctrl_frame, text="Reset", command=self.reset_board)
        self.btn_reset.grid(row=0, column=4, padx=2, sticky="ew")

        self.lbl_status = ttk.Label(left_panel, text="Bước: 0 / 0", font=("Segoe UI", 11, "bold"), foreground="#7f8c8d")
        self.lbl_status.pack(pady=5)

        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_log_box(right_panel, "🏆 GIẢI PHÁP TỐI ƯU", "sol", height=3, bg="#2f3542", fg="#eccc68")
        self.create_log_box(right_panel, "📜 NHẬT KÝ HÀNH ĐỘNG ĐANG CHẠY (Action Log)", "act", height=3)
        self.create_log_box(right_panel, "🌿 TRẠNG THÁI BIÊN ĐANG MỞ RỘNG (Frontier List)", "frn", height=5)
        self.create_log_box(right_panel, "🔒 DANH SÁCH ĐÃ DUYỆT (Explored List)", "exp", height=7)

    def create_log_box(self, parent, title, attr_name, height, bg="#1e272e", fg="#0be881"):
        frame = ttk.LabelFrame(parent, text=f" {title} ")
        frame.pack(fill=tk.BOTH, expand=True, pady=4)
        txt = tk.Text(frame, height=height, font=("Courier New", 10), bg=bg, fg=fg, wrap=tk.WORD)
        txt.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll = ttk.Scrollbar(frame, command=txt.yview)
        scroll.pack(fill=tk.Y, side=tk.RIGHT)
        txt.configure(yscrollcommand=scroll.set)
        setattr(self, f"txt_{attr_name}", txt)

    def clear_all_logs(self):
        for key in ["sol", "act", "frn", "exp"]:
            txt_box = getattr(self, f"txt_{key}")
            txt_box.delete("1.0", tk.END)

    def init_blank_board(self):
        self.clear_all_logs()
        self.history_states = [self.init_state_cfg]
        self.timeline_logs = [{"act": "Chưa khởi chạy thuật toán.", "frn": "Trống", "exp": "Trống"}]
        self.optimal_actions = []
        self.current_index = 0
        
        for i, num in enumerate(self.init_state_cfg):
            if num == 0:
                self.buttons[i].config(text="", bg="#ecf0f1", activebackground="#ecf0f1")
            else:
                self.buttons[i].config(text=str(num), bg="#2c3e50", fg="white", activebackground="#2c3e50")
                
        self.lbl_status.config(text="Bước: 0 / 0")
        self.btn_prev.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL)
        self.btn_go.config(state=tk.NORMAL)

    def run_algorithm(self):
        self.clear_all_logs()
        selected_algo = self.cbo_algo.get()
        self.history_states = [self.init_state_cfg]
        self.timeline_logs = []
        self.optimal_actions = []

        solver = PuzzleSolver()
        if selected_algo == "AND-OR Graph Search":
            res = solver.solve_and_or_graph_search(self.init_state_cfg, self.goal_state_cfg)
        else:
            return

        plan = res["plan"]
        if plan == "failure" or plan is None:
            self.history_states = [self.init_state_cfg]
            self.timeline_logs = [{"act": "Vòng lặp #1: Thuật toán thất bại lập tức.", "frn": "Trống", "exp": f"[{self.init_state_cfg}]"}]
            self.current_index = 0
            self.render_ui()
            self.txt_sol.insert(tk.END, "Không tìm được đường đi")
            messagebox.showerror("Thông báo", "Thuật toán trả về Thất bại (Failure)!")
            return

        # Tạo cây tiến trình timeline đồng bộ các bước hành động tối ưu
        cur = list(self.init_state_cfg)
        self.timeline_logs.append({
            "act": "Vòng lặp #1: Trạng thái Khởi tạo ban đầu.",
            "frn": f"Cấu hình gốc: {self.init_state_cfg}",
            "exp": f"1. {self.init_state_cfg}"
        })

        step_counter = 1
        while plan and len(plan) > 0:
            act = plan[0]
            self.optimal_actions.append(act)
            next_s = get_results(cur, act)[0]
            self.history_states.append(next_s)
            
            step_counter += 1
            # Tìm kiếm thông tin log của trạng thái hiện tại trong cây duyệt giải thuật
            step_log = next((l for l in res["logs"] if l['state'] == cur and l['action'] == act), None)
            
            if step_log:
                # 1. Định dạng hiển thị cụ thể các trạng thái con sinh ra trong ô Frontier List
                frn_text = ""
                for idx, child in enumerate(step_log['frontier']):
                    frn_text += f" Con thứ {idx+1}: {child}\n"
                if not frn_text: frn_text = " Hết nhánh con sinh ra."
                
                # 2. Định dạng hiển thị toàn bộ danh sách trạng thái đã duyệt cụ thể
                exp_text = ""
                for idx, exp_s in enumerate(step_log['explored']):
                    exp_text += f"{idx+1}. {exp_s}\n"
                
                act_text = f"Vòng lặp #{step_counter}: Tại trạng thái {cur} ➔ Đẩy ô trống sang hướng [{act}]"
            else:
                frn_text = " Không có dữ liệu biên"
                exp_text = " Không có dữ liệu đóng"
                act_text = f"Vòng lặp #{step_counter}: Di chuyển sang [{act}]"

            self.timeline_logs.append({
                "act": act_text,
                "frn": frn_text,
                "exp": exp_text
            })
            cur = next_s
            plan = plan[1].get(str(cur))

        # Hiển thị giải pháp tối ưu lên ô log trên cùng
        sol_text = " ➔ ".join([f"B{i+1}:[{a}]" for i, a in enumerate(self.optimal_actions)])
        if sol_text: 
            sol_text += f"\n\nTổng cộng: Hoàn thành trong {len(self.optimal_actions)} bước!"
        else: 
            sol_text = "Trạng thái đầu trùng khớp với Đích!"
        
        self.txt_sol.insert(tk.END, sol_text)
        self.current_index = 0
        self.render_ui()

    def render_ui(self):
        if not self.timeline_logs or self.current_index >= len(self.timeline_logs):
            return
            
        state = self.history_states[self.current_index]
        log = self.timeline_logs[self.current_index]

        # Đổi màu nổi bật ô số vừa di chuyển dịch chuyển
        highlight_idx = -1
        if self.current_index > 0:
            prev_state = self.history_states[self.current_index - 1]
            highlight_idx = prev_state.index(0)

        for i, num in enumerate(state):
            if num == 0:
                self.buttons[i].config(text="", bg="#ecf0f1", activebackground="#ecf0f1")
            else:
                bg_color = "#e67e22" if i == highlight_idx else "#2c3e50"
                self.buttons[i].config(text=str(num), bg=bg_color, fg="white", activebackground=bg_color, activeforeground="white")

        # ĐỒNG BỘ NỘI DUNG hiển thị chi tiết lên cả 3 ô log bên dưới dựa trên index hiện tại
        for key in ["act", "frn", "exp"]:
            txt_box = getattr(self, f"txt_{key}")
            txt_box.delete("1.0", tk.END)
            txt_box.insert(tk.END, log[key])

        self.lbl_status.config(text=f"Bước: {self.current_index} / {len(self.history_states) - 1}")
        self.update_buttons()

    def update_buttons(self):
        max_idx = len(self.history_states) - 1
        self.btn_prev.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_index < max_idx and not self.is_playing else tk.DISABLED)
        self.btn_go.config(state=tk.NORMAL if self.current_index < max_idx and not self.is_playing else tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL if self.is_playing else tk.DISABLED)

    def play(self):
        if len(self.history_states) <= 1 and not self.optimal_actions:
            self.run_algorithm()
            
        if self.current_index >= len(self.history_states) - 1: return
        self.is_playing = True
        self.update_buttons()
        self.auto_step()

    def auto_step(self):
        if self.current_index < len(self.history_states) - 1 and self.is_playing:
            self.current_index += 1
            self.render_ui()
            self.play_job = self.after(900, self.auto_step)
        else:
            self.pause()

    def pause(self):
        self.is_playing = False
        if self.play_job:
            self.after_cancel(self.play_job)
            self.play_job = None
        self.render_ui()

    def next_step(self):
        if len(self.history_states) <= 1 and not self.optimal_actions:
            self.run_algorithm()
            
        if self.current_index < len(self.history_states) - 1 and not self.is_playing:
            self.current_index += 1
            self.render_ui() # Tự động cập nhật đồng bộ các log tương ứng

    def preview(self):
        if self.current_index > 0:
            if self.is_playing: self.pause()
            self.current_index -= 1
            self.render_ui() # Tự động cập nhật đồng bộ lùi lại các log trước đó

    def reset_board(self):
        self.pause()
        self.init_blank_board()

    def submit_config(self):
        try:
            init_list = [int(x.strip()) for x in self.ent_init.get().split() if x.strip()]
            goal_list = [int(x.strip()) for x in self.ent_goal.get().split() if x.strip()]
            
            if len(init_list) != 9 or len(goal_list) != 9:
                raise ValueError("Bàn cờ phải có đủ 9 ô số.")
                
            if set(init_list) != set(range(9)) or set(goal_list) != set(range(9)):
                raise ValueError("Các số nhập vào phải từ 0 đến 8 và không trùng lặp.")
                
            self.init_state_cfg = init_list
            self.goal_state_cfg = goal_list
            self.run_algorithm()
        except ValueError as e:
            messagebox.showerror("Lỗi nhập liệu", str(e) if str(e) else "Vui lòng nhập các số cách nhau bằng dấu cách!")

if __name__ == "__main__":
    app = App8Puzzle()
    app.mainloop()