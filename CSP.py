# Tên: Hồng Tiến Phát (24110295)
# link github: https://github.com/TienPhat06/TriTueNhaoTao_10
import tkinter as tk
from tkinter import ttk
import random

# ---------------------------------------------------------------------------
# 1. CẤU HÌNH BÀI TOÁN 1: BẢN ĐỒ NƯỚC ÚC (Dành cho Backtracking, FC, Min-Conflicts)
# ---------------------------------------------------------------------------
VARIABLES_MAP = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
DOMAINS_MAP_INIT = {v: ['red', 'green', 'blue'] for v in VARIABLES_MAP}

NEIGHBORS_MAP = {
    'WA': ['NT', 'SA'], 'NT': ['WA', 'Q', 'SA'], 'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['Q', 'SA', 'V'], 'V': ['SA', 'NSW'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'T': []
}

MAP_POLYGONS = {
    'WA': [30,110, 150,110, 150,330, 70,330, 45,300, 30,250, 25,180],
    'NT': [150,110, 260,110, 260,200, 150,200],
    'SA': [150,200, 260,200, 300,200, 300,330, 240,330, 210,310, 150,330],
    'Q':  [260,110, 350,130, 380,180, 370,230, 300,230, 300,200, 260,200],
    'NSW': [300,230, 370,230, 380,270, 360,310, 315,310, 300,300],
    'V':  [300,300, 315,310, 360,310, 340,340, 300,330],
    'T':  [320,365, 345,365, 350,390, 315,390]
}

TEXT_POSITIONS = {
    'WA': (85, 210), 'NT': (205, 150), 'Q': (320, 170),
    'SA': (215, 265), 'NSW': (340, 265), 'V': (330, 320), 'T': (332, 378)
}

def is_consistent_map(var, value, assignment):
    for neighbor in NEIGHBORS_MAP[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

# 2. LOGIC CÁC GIẢI THUẬT CSP
def run_backtracking(history):
    assignment = {}
    current_domains = {v: list(DOMAINS_MAP_INIT[v]) for v in VARIABLES_MAP}
    history.append((dict(assignment), dict(current_domains), "Bắt đầu Backtracking: Tập gán rỗng {}", ""))
    
    def _search(assign):
        if len(assign) == len(VARIABLES_MAP):
            history.append((dict(assign), dict(current_domains), "Thành công! Đã tìm ra lời giải hoàn chỉnh.", ""))
            return True
        var = next(v for v in VARIABLES_MAP if v not in assign)
        history.append((dict(assign), dict(current_domains), f"Chọn biến chưa gán: {var}", var))
        for value in DOMAINS_MAP_INIT[var]:
            history.append((dict(assign), dict(current_domains), f"Thử gán màu {value.upper()} cho {var}", var))
            if is_consistent_map(var, value, assign):
                assign[var] = value
                history.append((dict(assign), dict(current_domains), f"Hợp lệ. Gán thành công: {var} = {value.upper()}", var))
                if _search(assign): return True
                del assign[var]
                history.append((dict(assign), dict(current_domains), f"⚠️ Quay lui (Backtrack): Bỏ gán {var}", var))
            else:
                history.append((dict(assign), dict(current_domains), f"❌ Bị trùng! {var}={value.upper()} xung đột vùng kề.", var))
        return False
    _search(assignment)

def run_forward_checking(history):
    assignment = {}
    domains = {v: list(DOMAINS_MAP_INIT[v]) for v in VARIABLES_MAP}
    history.append((dict(assignment), dict(domains), "Bắt đầu Forward Checking: Tập gán rỗng {}", ""))
    
    def _search(assign, doms):
        if len(assign) == len(VARIABLES_MAP):
            history.append((dict(assign), dict(doms), "Thành công! Bản đồ đã được giải xong.", ""))
            return True
        var = next(v for v in VARIABLES_MAP if v not in assign)
        history.append((dict(assign), dict(doms), f"Chọn biến chưa gán: {var}", var))
        for value in doms[var]:
            assign[var] = value
            local_domains = {v: list(doms[v]) for v in VARIABLES_MAP}
            local_domains[var] = [value]
            history.append((dict(assign), dict(local_domains), f"Tạm gán {var} = {value.upper()}. Tiến hành nhìn trước...", var))
            
            failed = False
            removed_logs = []
            for neighbor in NEIGHBORS_MAP[var]:
                if neighbor not in assign:
                    if value in local_domains[neighbor]:
                        local_domains[neighbor].remove(value)
                        removed_logs.append(f"Xóa {value.upper()} khỏi {neighbor}")
                        if not local_domains[neighbor]:
                            failed = True
                            removed_logs.append(f"💥 LỖI: {neighbor} rỗng miền!")
            if removed_logs:
                history.append((dict(assign), dict(local_domains), " -> " + ", ".join(removed_logs), var))
            if not failed:
                if _search(assign, local_domains): return True
            else:
                history.append((dict(assign), dict(local_domains), f"❌ FC Thất bại! Hủy gán {var} = {value.upper()}", var))
            del assign[var]
        return False
    _search(assignment, domains)

def run_ac3_numeric(history):
    variables = ['X', 'Y', 'Z']
    domains = {'X': [1, 2, 3], 'Y': [1, 2, 3], 'Z': [2, 3]}
    queue = [('X', 'Y'), ('Y', 'X'), ('Y', 'Z'), ('Z', 'Y')]
    
    history.append(({}, {v: list(domains[v]) for v in variables}, f"Khởi tạo AC-3: Miền ban đầu X={domains['X']}, Y={domains['Y']}, Z={domains['Z']}. Queue: {queue}", ""))
    
    def check_constraint(v1, val1, v2, val2):
        mapping = {v1: val1, v2: val2}
        if 'X' in mapping and 'Y' in mapping:
            return mapping['X'] < mapping['Y']
        if 'Y' in mapping and 'Z' in mapping:
            return mapping['Y'] < mapping['Z']
        return True

    while queue:
        xi, xj = queue.pop(0)
        q_state_str = str(queue)
        history.append(({}, {v: list(domains[v]) for v in variables}, f"Pop cung ({xi} -> {xj}) ra xét. Queue còn lại: {q_state_str}", f"{xi}->{xj}"))
        
        revised = False
        removed_values = []
        for x in list(domains[xi]):
            has_support = False
            for y in domains[xj]:
                if check_constraint(xi, x, xj, y):
                    has_support = True
                    break
            if not has_support:
                domains[xi].remove(x)
                removed_values.append(x)
                revised = True
        
        if revised:
            history.append(({}, {v: list(domains[v]) for v in variables}, f"✂️ REVISE: Xóa giá trị {removed_values} khỏi miền của {xi} do không thỏa mãn ràng buộc với {xj}. Miền mới {xi} = {domains[xi]}", f"{xi}->{xj}"))
            if not domains[xi]:
                history.append(({}, {v: list(domains[v]) for v in variables}, f"💥 THẤT BẠI: Miền {xi} bị rỗng! Hệ thống vô nghiệm.", f"{xi}->{xj}"))
                return
            
            neighbors = []
            if xi == 'Y': neighbors = ['X', 'Z']
            elif xi in ['X', 'Z']: neighbors = ['Y']
                
            added_arcs = []
            for xk in neighbors:
                if xk != xj:
                    if (xk, xi) not in queue:
                        queue.append((xk, xi))
                        added_arcs.append(f"({xk}->{xi})")
            if added_arcs:
                history.append(({}, {v: list(domains[v]) for v in variables}, f"🔄 Lan truyền (Propagation): Do miền của {xi} thay đổi, nạp lại các cung kề hướng về {xi}: " + ", ".join(added_arcs) + f". Queue mới: {str(queue)}", f"{xi}->{xj}"))
        else:
            history.append(({}, {v: list(domains[v]) for v in variables}, f"✔️ Không đổi: Tất cả giá trị trong miền {xi} đều có sự hỗ trợ hợp lệ từ {xj}.", f"{xi}->{xj}"))
                
    history.append(({}, {v: list(domains[v]) for v in variables}, f"Thành công! Queue rỗng. Toàn bộ mạng lưới đạt trạng thái Nhất quán cung vĩnh viễn. Nghiệm duy nhất: X={domains['X']}, Y={domains['Y']}, Z={domains['Z']}", ""))

def run_min_conflicts(history, max_steps=30):
    """MÔ PHỎNG MIN-CONFLICTS CHI TIẾT TỪNG BƯỚC ĐẾM XUNG ĐỘT RÀNG BUỘC"""
    # Khởi tạo trạng thái ngẫu nhiên đầy đủ cho tất cả các vùng ban đầu
    assignment = {v: random.choice(DOMAINS_MAP_INIT[v]) for v in VARIABLES_MAP}
    domains = {v: [assignment[v]] for v in VARIABLES_MAP}
    
    history.append((dict(assignment), dict(domains), f"Khởi tạo Min-Conflicts với trạng thái ngẫu nhiên ban đầu: {str(assignment)}", ""))
    
    for step in range(1, max_steps + 1):
        # 1. Tìm tất cả các biến đang bị vi phạm ràng buộc (trùng màu với vùng kề)
        conflicted_vars = []
        for v in VARIABLES_MAP:
            # Đếm xem biến v hiện tại có bao nhiêu xung đột với lân cận của nó
            c_count = sum(1 for n in NEIGHBORS_MAP[v] if assignment[n] == assignment[v])
            if c_count > 0:
                conflicted_vars.append(v)
                
        # Nếu không còn biến nào bị xung đột -> Đã tìm thấy lời giải thành công
        if not conflicted_vars:
            history.append((dict(assignment), dict(domains), f"🎉 THÀNH CÔNG ở bước {step-1}! Hệ thống sạch xung đột hoàn toàn.", ""))
            return
            
        # 2. Chọn ngẫu nhiên một biến nằm trong danh sách xung đột để tối ưu hóa
        var = random.choice(conflicted_vars)
        current_color = assignment[var]
        
        # Ghi log thông báo danh sách biến lỗi và biến được chọn để xử lý
        history.append((dict(assignment), dict(domains), f"👉 Bước {step}: Các biến đang lỗi màu: {conflicted_vars}. Chọn ngẫu nhiên biến [{var}] để sửa (Màu hiện tại: {current_color.upper()})", var))
        
        # 3. Thử nghiệm tính toán đếm số lượng xung đột đối với TỪNG GIÁ TRỊ trong miền
        best_values = []
        min_conf = float('inf')
        conflict_report = []
        
        for val in DOMAINS_MAP_INIT[var]:
            # Đếm số xung đột nếu biến 'var' nhận màu 'val'
            conf_count = 0
            conf_details = []
            for n in NEIGHBORS_MAP[var]:
                if assignment[n] == val:
                    conf_count += 1
                    conf_details.append(n)
            
            # Lưu lại chuỗi log chi tiết cho từng màu để in ra màn hình
            detail_str = f"trùng với {conf_details}" if conf_details else "hợp lệ hoàn toàn"
            conflict_report.append(f"Màu {val.upper()}: {conf_count} lỗi ({detail_str})")
            
            # Cập nhật giá trị tối ưu (chọn giá trị có số lượng xung đột ít nhất)
            if conf_count < min_conf:
                min_conf = conf_count
                best_values = [val]
            elif conf_count == min_conf:
                best_values.append(val)
                
        # In báo cáo chi tiết đếm lỗi của các màu lên Log Console
        history.append((dict(assignment), dict(domains), f" 🔍 Kiểm tra số xung đột cho [{var}]: " + " | ".join(conflict_report), var))
        
        # Nếu có nhiều màu cùng có số xung đột tối thiểu bằng nhau, chọn ngẫu nhiên một màu
        chosen_color = random.choice(best_values)
        
        # Tiến hành cập nhật trạng thái
        assignment[var] = chosen_color
        domains = {v: [assignment[v]] for v in VARIABLES_MAP}
        
        # Ghi log kết quả quyết định đổi màu sau khi cân nhắc số xung đột
        if chosen_color == current_color:
            history.append((dict(assignment), dict(domains), f" ⚖️ Quyết định: Giữ nguyên màu {chosen_color.upper()} cho [{var}] vì đây đã là mức xung đột nhỏ nhất ({min_conf} lỗi).", var))
        else:
            history.append((dict(assignment), dict(domains), f" 🔄 Quyết định: Đổi màu [{var}]: {current_color.upper()} ➔ {chosen_color.upper()} để giảm số xung đột xuống tối thiểu còn {min_conf} lỗi.", var))
            
    history.append((dict(assignment), dict(domains), "❌ Thất bại: Đã vượt quá giới hạn số bước (Max Steps) nhưng bản đồ vẫn còn vùng trùng màu.", ""))

def run_down_placeholder(history):
    pass

# ---------------------------------------------------------------------------
# 3. GIAO DIỆN ĐỒ HỌA TRỰC QUAN (GUI) ĐA NĂNG
# ---------------------------------------------------------------------------
class UltimateCSPVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Mô phỏng Giải thuật Ràng buộc CSP trực quan")
        self.root.geometry("1020x620")
        self.root.resizable(False, False)
        
        self.history = []
        self.current_step_idx = -1
        self.is_playing = False
        self.play_speed = 1000 
        
        # --- TOP CONTROL BAR ---
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(top_frame, text="Thuật toán:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=3)
        self.algo_combo = ttk.Combobox(top_frame, values=[
            "Backtracking Search", "Forward Checking", "AC-3 (Mô phỏng Số Học)", "Min-Conflicts"
        ], state="readonly", width=22, font=("Arial", 10))
        self.algo_combo.current(0)
        self.algo_combo.pack(side=tk.LEFT, padx=3)
        self.algo_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_simulation())
        
        self.btn_load = ttk.Button(top_frame, text="Nạp dữ liệu", command=self.load_algorithm)
        self.btn_load.pack(side=tk.LEFT, padx=3)
        
        ttk.Separator(top_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        
        self.btn_prev = ttk.Button(top_frame, text="⏮ Previous", command=self.prev_step, state=tk.DISABLED)
        self.btn_prev.pack(side=tk.LEFT, padx=1)
        self.btn_go = ttk.Button(top_frame, text="▶ Go", command=self.play_auto, state=tk.DISABLED)
        self.btn_go.pack(side=tk.LEFT, padx=1)
        self.btn_pause = ttk.Button(top_frame, text="⏸ Pause", command=self.pause_auto, state=tk.DISABLED)
        self.btn_pause.pack(side=tk.LEFT, padx=1)
        self.btn_next = ttk.Button(top_frame, text="⏭ Next", command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=1)
        self.btn_reset = ttk.Button(top_frame, text="🔄 Reset", command=self.reset_simulation)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        self.lbl_step_counter = ttk.Label(top_frame, text="Bước: 0/0", font=("Arial", 10, "bold"), foreground="#7f8c8d")
        self.lbl_step_counter.pack(side=tk.RIGHT, padx=10)

        # --- CENTRAL MAIN PANEL ---
        main_frame = ttk.Frame(root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(main_frame, bg="#ecf0f1", highlightthickness=1, highlightbackground="#bdc3c7", width=440)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        log_subframe = ttk.LabelFrame(right_frame, text=" Nhật ký thực thi logic (Log Console) ")
        log_subframe.pack(fill=tk.BOTH, expand=True, pady=2)
        self.log_text = tk.Text(log_subframe, wrap=tk.WORD, font=("Consolas", 10), bg="#2d3436", fg="#dfe6e9", height=15)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar = ttk.Scrollbar(log_subframe, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.domain_subframe = ttk.LabelFrame(right_frame, text=" Trạng thái Miền giá trị hiện tại (Domains status) ")
        self.domain_subframe.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, pady=5)
        self.domain_text = tk.Text(self.domain_subframe, wrap=tk.WORD, font=("Consolas", 11, "bold"), 
                                   bg="#34495e", fg="#ecf0f1", height=8, padx=10, pady=5)
        self.domain_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        dom_scrollbar = ttk.Scrollbar(self.domain_subframe, command=self.domain_text.yview)
        dom_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.domain_text.config(yscrollcommand=dom_scrollbar.set)
        self.domain_text.config(state=tk.DISABLED)
        
        self.log_text.tag_config("success", foreground="#00b894", font=("Consolas", 10, "bold"))
        self.log_text.tag_config("fail", foreground="#ff7675")
        self.log_text.tag_config("current", background="#0984e3", foreground="white", font=("Consolas", 10, "bold"))
        
        self.reset_simulation()

    def draw_map_australia(self, assignment, active_var):
        self.canvas.delete("all")
        self.canvas.create_text(220, 25, text="BÀI TOÁN TÔ MÀU BẢN ĐỒ NƯỚC ÚC", font=("Arial", 12, "bold"), fill="#2c3e50")
        
        for var, points in MAP_POLYGONS.items():
            color = assignment.get(var, "#ffffff")
            outline_color = "#e67e22" if var == active_var else "#2c3e50"
            border_w = 4 if var == active_var else 2
            
            self.canvas.create_polygon(points, fill=color, outline=outline_color, width=border_w)
            tx, ty = TEXT_POSITIONS[var]
            text_color = "white" if color in ['red', 'blue', 'green'] else "#2c3e50"
            self.canvas.create_text(tx, ty, text=var, font=("Arial", 11, "bold"), fill=text_color)

    def draw_ac3_numeric_graph(self, domains, active_arc):
        self.canvas.delete("all")
        self.canvas.create_text(220, 25, text="BÀI TOÁN AC-3 SỐ HỌC: X < Y và Y < Z", font=("Arial", 12, "bold"), fill="#2c3e50")
        
        node_pos = {'X': (80, 240), 'Y': (220, 240), 'Z': (360, 240)}
        
        def draw_arrow(p1, p2, is_active):
            color = "#e74c3c" if is_active else "#95a5a6"
            width = 3.5 if is_active else 1.5
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], arrow=tk.LAST, fill=color, width=width, arrowshape=(10,12,4))

        draw_arrow(node_pos['X'], node_pos['Y'], active_arc == "X->Y")
        draw_arrow(node_pos['Y'], node_pos['X'], active_arc == "Y->X")
        draw_arrow(node_pos['Y'], node_pos['Z'], active_arc == "Y->Z")
        draw_arrow(node_pos['Z'], node_pos['Y'], active_arc == "Z->Y")
        
        self.canvas.create_text(150, 215, text="X < Y", font=("Arial", 10, "italic"), fill="#16a085")
        self.canvas.create_text(290, 215, text="Y < Z", font=("Arial", 10, "italic"), fill="#16a085")

        for node, (nx, ny) in node_pos.items():
            is_in_arc = active_arc and node in active_arc.split("->")
            node_bg = "#f1c40f" if is_in_arc else "#ffffff"
            
            self.canvas.create_oval(nx-35, ny-35, nx+35, ny+35, fill=node_bg, outline="#2c3e50", width=2.5)
            self.canvas.create_text(nx, ny-48, text=f"Biến {node}", font=("Arial", 11, "bold"), fill="#2c3e50")
            
            current_vals = domains.get(node, [])
            full_vals = [1, 2, 3] if node in ['X', 'Y'] else [2, 3]
            
            for idx, num in enumerate(full_vals):
                offset_y = ny - 15 + idx * 16
                if num in current_vals:
                    self.canvas.create_text(nx, offset_y, text=str(num), font=("Consolas", 12, "bold"), fill="#27ae60")
                else:
                    self.canvas.create_text(nx, offset_y, text=str(num), font=("Consolas", 12, "overstrike"), fill="#c0392b")

    def print_history_to_log_box(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        for idx, (_, _, msg, _) in enumerate(self.history):
            self.log_text.insert(tk.END, f"[{idx+1:02d}] {msg}\n")
        self.log_text.config(state=tk.DISABLED)

    def highlight_log_line(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.tag_remove("current", "1.0", tk.END)
        self.log_text.tag_remove("success", "1.0", tk.END)
        self.log_text.tag_remove("fail", "1.0", tk.END)
        
        current_line = self.current_step_idx + 1
        self.log_text.tag_add("current", f"{current_line}.0", f"{current_line}.end")
        
        for i in range(1, len(self.history) + 1):
            text_content = self.log_text.get(f"{i}.0", f"{i}.end")
            if "THÀNH CÔNG" in text_content or "Thành công" in text_content:
                self.log_text.tag_add("success", f"{i}.0", f"{i}.end")
            elif "❌" in text_content or "⚠️" in text_content or "💥" in text_content or "Thất bại" in text_content or "✂️" in text_content or "🔍" in text_content:
                self.log_text.tag_add("fail", f"{i}.0", f"{i}.end")
                
        self.log_text.see(f"{current_line}.0")
        self.log_text.config(state=tk.DISABLED)

    def update_domain_display(self, domains):
        self.domain_text.config(state=tk.NORMAL)
        self.domain_text.delete("1.0", tk.END)
        
        current_algo = self.algo_combo.get()
        vars_to_show = ['X', 'Y', 'Z'] if "AC-3" in current_algo else VARIABLES_MAP
        
        for var in vars_to_show:
            vals = domains.get(var, [])
            vals_str = [str(v).upper() for v in vals]
            self.domain_text.insert(tk.END, f" ■ Màu vùng hiện tại của {var:<3} : {{ {', '.join(vals_str)} }}\n")
            
        self.domain_text.config(state=tk.DISABLED)

    def load_algorithm(self):
        self.pause_auto()
        algo_name = self.algo_combo.get()
        self.history = []
        
        if algo_name == "Backtracking Search": run_backtracking(self.history)
        elif algo_name == "Forward Checking": run_forward_checking(self.history)
        elif algo_name == "AC-3 (Mô phỏng Số Học)": run_ac3_numeric(self.history)
        elif algo_name == "Min-Conflicts": run_min_conflicts(self.history)
            
        self.current_step_idx = 0
        self.print_history_to_log_box()
        self.update_ui_by_step()
        
        self.btn_go.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.NORMAL)
        self.btn_prev.config(state=tk.DISABLED)

    def update_ui_by_step(self):
        if not self.history: return
        assignment, domains, _, active_info = self.history[self.current_step_idx]
        total_steps = len(self.history)
        
        self.lbl_step_counter.config(text=f"Bước: {self.current_step_idx + 1}/{total_steps}")
        self.highlight_log_line()
        self.update_domain_display(domains)
        
        if "AC-3" in self.algo_combo.get():
            self.draw_ac3_numeric_graph(domains, active_info)
        else:
            self.draw_map_australia(assignment, active_info)
        
        if self.current_step_idx >= total_steps - 1:
            self.btn_next.config(state=tk.DISABLED)
            self.is_playing = False 
            self.btn_go.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.DISABLED)
            self.algo_combo.config(state="readonly")
            self.btn_load.config(state=tk.NORMAL)
        else:
            if not self.is_playing: self.btn_next.config(state=tk.NORMAL)
            
        if self.current_step_idx <= 0:
            self.btn_prev.config(state=tk.DISABLED)
        else:
            if not self.is_playing: self.btn_prev.config(state=tk.NORMAL)

    def next_step(self):
        if self.current_step_idx < len(self.history) - 1:
            self.current_step_idx += 1
            self.update_ui_by_step()

    def prev_step(self):
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.update_ui_by_step()

    def play_auto(self):
        if self.is_playing or self.current_step_idx >= len(self.history) - 1: return
        self.is_playing = True
        self.btn_go.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.DISABLED)
        self.btn_prev.config(state=tk.DISABLED)
        self.algo_combo.config(state=tk.DISABLED)
        self.btn_load.config(state=tk.DISABLED)
        self._play_loop()

    def _play_loop(self):
        if self.is_playing and self.current_step_idx < len(self.history) - 1:
            self.next_step()
            self.root.after(self.play_speed, self._play_loop)

    def pause_auto(self):
        self.is_playing = False
        self.btn_go.config(state=tk.NORMAL if self.history and self.current_step_idx < len(self.history) - 1 else tk.DISABLED)
        self.btn_pause.config(state=tk.DISABLED)
        self.algo_combo.config(state="readonly")
        self.btn_load.config(state=tk.NORMAL)
        if self.history:
            if self.current_step_idx < len(self.history) - 1: self.btn_next.config(state=tk.NORMAL)
            if self.current_step_idx > 0: self.btn_prev.config(state=tk.NORMAL)

    def reset_simulation(self):
        self.pause_auto()
        self.history = []
        self.current_step_idx = -1
        self.lbl_step_counter.config(text="Bước: 0/0")
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.domain_text.config(state=tk.NORMAL)
        self.domain_text.delete("1.0", tk.END)
        self.domain_text.config(state=tk.DISABLED)
        
        self.btn_go.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)
        self.btn_prev.config(state=tk.DISABLED)
        
        if "AC-3" in self.algo_combo.get():
            init_domains_demo = {'X': [1,2,3], 'Y': [1,2,3], 'Z': [2,3]}
            self.draw_ac3_numeric_graph(init_domains_demo, "")
        else:
            self.draw_map_australia({}, "")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateCSPVisualizer(root)
    root.mainloop()