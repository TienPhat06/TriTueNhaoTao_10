import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import heapq
import random 

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, cost=0, depth=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action 
        self.cost = cost          # Chi phí tổng quát f(n) hoặc g(n) tùy thuật toán
        self.depth = depth        # Độ sâu g(n) từ nút gốc
        self.heuristic = heuristic  # Giá trị h(n)

    def __lt__(self, other):
        return self.cost < other.cost

def get_possible_moves(state):
    moves = []
    zero_index = state.index(0)
    row, col = zero_index // 3, zero_index % 3
    directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

    for action, (dr, dc) in directions.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_index], new_state[new_zero_index] = new_state[new_zero_index], new_state[zero_index]
            moves.append((tuple(new_state), action))
    return moves

def count_misplaced_tiles(state, goal):
    """🛠️ Heuristic 1: Chỉ đếm các ô SỐ sai vị trí, BỎ QUA ô trống số 0"""
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1
    return count

def count_manhattan_distance(state, goal):
    """🧩 Heuristic 2: Tính tổng khoảng cách Manhattan của các ô số (bỏ qua ô trống số 0)"""
    distance = 0
    for i in range(9):
        val = state[i]
        if val != 0:
            curr_row, curr_col = i // 3, i % 3
            goal_index = goal.index(val)
            goal_row, goal_col = goal_index // 3, goal_index % 3
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

def generate_random_solvable_state(goal, steps=20):
    """🎲 Sinh trạng thái ngẫu nhiên chắc chắn giải được bằng cách trượt từ ĐÍCH (dùng cho Restart / Beam)"""
    current = list(goal)
    for _ in range(steps):
        moves = get_possible_moves(tuple(current))
        if moves:
            current = list(random.choice(moves)[0])
    return tuple(current)

# =========================================================================
# THUẬT TOÁN ĐỒ THỊ VÀ KHÔNG GIAN TRẠNG THÁI (1 ĐẾN 7)
# =========================================================================

def run_bfs(start, goal):
    history_log = []
    trace_init = f"🌐 [THUẬT TOÁN: BFS - BREADTH-FIRST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO BAN ĐẦU)\n--------------------------------------------------\n▶️ Nút gốc được nạp vào Frontier Queue (FIFO).\n   + Trạng thái gốc: {start}\n   + Danh sách đóng Explored: Trống rỗng []\n"
    history_log.append({'current_node': start, 'frontier': [(start, 0)], 'explored': [], 'trace_text': trace_init})

    if start == goal: 
        return PuzzleNode(start), 0, history_log
    
    frontier = deque([PuzzleNode(start)])
    explored = set()
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        node = frontier.popleft()
        explored.add(node.state)

        trace = f"🌐 [THUẬT TOÁN: BFS - BREADTH-FIRST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Lấy nút từ ĐẦU HÀNG ĐỢI Queue (FIFO):\n   + Trạng thái: {node.state}\n   + Độ sâu d = {node.depth}\n\n🌿 PHÁT TRIỂN CÁC NHÁNH CON VÀ ĐƯA VÀO CUỐI QUEUE:\n"

        for s, a in get_possible_moves(node.state):
            if s not in explored and not any(f.state == s for f in frontier):
                child = PuzzleNode(s, parent=node, action=a, cost=node.depth+1, depth=node.depth+1)
                if s == goal: 
                    trace += f"   [🎯] Tìm thấy ĐÍCH bằng hành động [{a}] -> {s}\n"
                    current_frontier_data = [(n.state, n.depth) for n in frontier] + [(child.state, child.depth)]
                    history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': list(explored), 'trace_text': trace})
                    return child, nodes_expanded, history_log
                frontier.append(child)
                trace += f"   [+ Add] Xếp vào CUỐI hàng đợi: [{a}] -> {s} (d = {child.depth})\n"
            else:
                trace += f"   [x Skip] Bỏ qua nhánh {s} (Đã nằm trong tập đóng/mở)\n"

        current_frontier_data = [(n.state, n.depth) for n in frontier]
        history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': list(explored), 'trace_text': trace})
        
    return None, nodes_expanded, history_log

def run_dfs(start, goal, max_depth=15):
    history_log = []
    trace_init = f"🌲 [THUẬT TOÁN: DFS - DEPTH-FIRST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO BAN ĐẦU)\n--------------------------------------------------\n▶️ Nút gốc được đẩy vào Frontier Stack (LIFO).\n   + Trạng thái gốc: {start}\n   + Danh sách đóng Explored: Trống rỗng []\n"
    history_log.append({'current_node': start, 'frontier': [(start, 0)], 'explored': [], 'trace_text': trace_init})

    if start == goal: 
        return PuzzleNode(start), 0, history_log
    
    frontier = [PuzzleNode(start)]
    explored = set()
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        node = frontier.pop()
        explored.add(node.state)

        trace = f"🌲 [THUẬT TOÁN: DFS - DEPTH-FIRST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Lấy nút từ ĐỈNH NGĂN XẾP Stack (LIFO):\n   + Trạng thái: {node.state}\n   + Độ sâu d = {node.depth}\n\n"

        if node.state == goal:
            trace += f"   [🎯] Tìm thấy TRẠNG THÁI ĐÍCH tại độ sâu d = {node.depth}!\n"
            history_log.append({'current_node': node.state, 'frontier': [(n.state, n.depth) for n in frontier], 'explored': list(explored), 'trace_text': trace})
            return node, nodes_expanded, history_log
        
        trace += f"🌿 PHÁT TRIỂN CÁC NHÁNH CON VÀ ĐẨY VÀO ĐỈNH STACK:\n"
        if node.depth < max_depth:
            for s, a in reversed(get_possible_moves(node.state)):
                if s not in explored and not any(f.state == s for f in frontier):
                    frontier.append(PuzzleNode(s, parent=node, action=a, cost=node.depth+1, depth=node.depth+1))
                    trace += f"   [+ Push] Đẩy vào ĐỈNH Stack: [{a}] -> {s} (d = {node.depth + 1})\n"
                else:
                    trace += f"   [x Skip] Trùng lặp trạng thái: Bỏ qua -> {s}\n"
        else:
            trace += f"   [⚠️ CẮT NHÁNH] Đã chạm ngưỡng giới hạn độ sâu tối đa d = {max_depth}!\n"

        current_frontier_data = [(n.state, n.depth) for n in frontier]
        history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': list(explored), 'trace_text': trace})
        
    return None, nodes_expanded, history_log

def run_ids(start, goal, max_limit=25):
    total_nodes = 0
    history_log = []
    trace_init_total = f"🔄 [THUẬT TOÁN: IDS - ITERATIVE DEEPENING SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (TỔNG KHỞI TẠO)\n--------------------------------------------------\n▶️ Sẵn sàng thực hiện các chu kỳ lặp tăng dần giới hạn độ sâu (Limit).\n"
    history_log.append({'current_node': start, 'frontier': [(start, 0)], 'explored': [], 'trace_text': trace_init_total})

    for limit in range(max_limit):
        frontier = [PuzzleNode(start)]
        explored = {} 
        trace_init = f"🔄 [THUẬT TOÁN: IDS - ITERATIVE DEEPENING SEARCH]\n==================================================\n🚀 BẮT ĐẦU CHU KỲ MỚI VỚI GIỚI HẠN ĐỘ SÂU (LIMIT) = {limit}\n"
        history_log.append({'current_node': start, 'frontier': [(start, 0)], 'explored': [], 'trace_text': trace_init})

        while frontier:
            node = frontier.pop()
            total_nodes += 1
            trace = f"🔄 [THUẬT TOÁN: IDS - SÂU DẦN LẶP LẠI]\n📌 LIMIT HIỆN TẠI: {limit} | TỔNG VÒNG LẶP: #{total_nodes}\n--------------------------------------------------\n▶️ Pop từ Stack: {node.state} (d = {node.depth})\n\n"
            
            if node.state == goal:
                trace += f"   [🎯] Tìm thấy ĐÍCH tại độ sâu d = {node.depth}!\n"
                history_log.append({'current_node': node.state, 'frontier': [(n.state, n.depth) for n in frontier], 'explored': list(explored.keys()), 'trace_text': trace})
                return node, total_nodes, history_log
                
            trace += f"🌿 PHÁT TRIỂN CÁC NHÁNH CON THEO LIMIT:\n"
            if node.depth < limit:
                if node.state not in explored or node.depth < explored[node.state]:
                    explored[node.state] = node.depth
                    for s, a in reversed(get_possible_moves(node.state)):
                        frontier.append(PuzzleNode(s, parent=node, action=a, cost=node.depth+1, depth=node.depth+1))
                        trace += f"   [+ Push] Nhánh con d = {node.depth+1}: [{a}] -> {s}\n"
                else:
                    trace += f"   [x Skip] Đã từng duyệt trạng thái này ở độ sâu tối ưu hơn.\n"
            else:
                trace += f"   [⚠️ NGẮT NHÁNH] Đã chặn đứng do chạm giới hạn Limit = {limit}.\n"
                
            current_frontier_data = [(n.state, n.depth) for n in frontier]
            history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': list(explored.keys()), 'trace_text': trace})
            
    return None, total_nodes, history_log

def run_ucs(start, goal):
    history_log = []
    trace_init = f"⚖️ [THUẬT TOÁN: UCS - UNIFORM COST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO BAN ĐẦU)\n--------------------------------------------------\n▶️ Nút gốc nạp vào Min-Heap Priority Queue dựa theo chi phí g(n).\n   + Trạng thái gốc: {start} | g(n) = 0\n"
    history_log.append({'current_node': start, 'frontier': [(0, start)], 'explored': [], 'trace_text': trace_init})

    frontier = [PuzzleNode(start, cost=0)]
    explored = {}
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        node = heapq.heappop(frontier)
        explored[node.state] = node.cost

        trace = f"⚖️ [THUẬT TOÁN: UCS - UNIFORM COST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Pop nút có CHI PHÍ ĐƯỜNG ĐI g(n) THẤP NHẤT từ Heap:\n   + Trạng thái: {node.state}\n   + Chi phí tích lũy g(n) = {node.cost}\n\n🌿 PHÁT TRIỂN CÁC NHÁNH CON (Tính g_mới = g_cha + 1):\n"

        if node.state == goal:
            trace += f"   [🎯] Đạt trạng thái ĐÍCH tối ưu thành công!\n"
            history_log.append({'current_node': node.state, 'frontier': [(n.cost, n.state) for n in frontier], 'explored': list(explored.keys()), 'trace_text': trace})
            return node, nodes_expanded, history_log
            
        for s, a in get_possible_moves(node.state):
            new_cost = node.cost + 1
            if s not in explored:
                in_frontier = False
                for f_node in frontier:
                    if f_node.state == s:
                        in_frontier = True
                        if new_cost < f_node.cost:
                            trace += f"   [🔄 Cập nhật] Tìm thấy đường tốt hơn tới {s}: g cũ = {f_node.cost} -> g mới = {new_cost}\n"
                            f_node.cost = new_cost
                            f_node.parent = node
                            f_node.action = a
                            heapq.heapify(frontier)
                        break
                if not in_frontier:
                    heapq.heappush(frontier, PuzzleNode(s, parent=node, action=a, cost=new_cost, depth=node.depth+1))
                    trace += f"   [+ Insert] Thêm vào Heap: [{a}] -> {s} với g(n) = {new_cost}\n"
        
        current_frontier_data = [(n.cost, n.state) for n in frontier]
        history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': list(explored.keys()), 'trace_text': trace})
        
    return None, nodes_expanded, history_log

def run_greedy(start, goal):
    history_log = []
    h_start = count_misplaced_tiles(start, goal)
    trace_init = f"🎯 [THUẬT TOÁN: GREEDY BEST-FIRST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO BAN ĐẦU)\n--------------------------------------------------\n▶️ Nút gốc được sắp xếp vào Min-Heap dựa theo giá trị Heuristic h(n).\n   + Trạng thái gốc: {start} | h(n) = {h_start}\n"
    history_log.append({'current_node': start, 'frontier': [(h_start, start)], 'explored': [], 'trace_text': trace_init})

    frontier = [PuzzleNode(start, cost=h_start, heuristic=h_start)]
    explored = set()
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        node = heapq.heappop(frontier)
        explored.add(node.state)

        trace = f"🎯 [THUẬT TOÁN: GREEDY BEST-FIRST SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Chọn nút có HEURISTIC h(n) THẤP NHẤT (Tham lam):\n   + Trạng thái: {node.state}\n   + h(n) = {node.heuristic}\n\n🌿 TÍNH TOÁN HEURISTIC h(n) CHO CÁC NHÁNH CON KẾ TIẾP:\n"

        if node.state == goal:
            trace += f"   [🎯] Tìm thấy đích thành công!\n"
            history_log.append({'current_node': node.state, 'frontier': [(n.heuristic, n.state) for n in frontier], 'explored': list(explored), 'trace_text': trace})
            return node, nodes_expanded, history_log

        for s, a in get_possible_moves(node.state):
            if s not in explored and not any(f.state == s for f in frontier):
                h_child = count_misplaced_tiles(s, goal)
                child = PuzzleNode(s, parent=node, action=a, cost=h_child, depth=node.depth+1, heuristic=h_child)
                heapq.heappush(frontier, child)
                trace += f"   [+] Đẩy vào Heap: [{a}] -> {s} có h(n) = {h_child}\n"

        current_frontier_data = [(n.heuristic, n.state) for n in frontier]
        history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': list(explored), 'trace_text': trace})
        
    return None, nodes_expanded, history_log

def run_astar(start, goal):
    history_log = []
    h_start = count_misplaced_tiles(start, goal)
    trace_init = f"⭐ [THUẬT TOÁN: A* SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO BAN ĐẦU)\n--------------------------------------------------\n▶️ Đưa nút gốc vào Min-Heap. Sắp xếp theo tổng hàm đánh giá f(n) = g(n) + h(n).\n   + Trạng thái gốc: {start} | f={h_start}\n"
    history_log.append({'current_node': start, 'frontier': [(h_start, start)], 'explored': [], 'trace_text': trace_init})

    frontier = [PuzzleNode(start, cost=0 + h_start, depth=0, heuristic=h_start)]
    explored = {}
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        node = heapq.heappop(frontier)
        explored[node.state] = node.cost

        trace = f"⭐ [THUẬT TOÁN: A* SEARCH]\n⏳ VÒNG LẶP DUYỆT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Lấy nút có hàm tổng chi phí f(n) nhỏ nhất từ Min-Heap:\n   + Trạng thái: {node.state}\n   + f(n) = g({node.depth}) + h({node.heuristic}) = {node.cost}\n\n🌿 KHAI TRIỂN NHÁNH CON PHỐI HỢP CHI PHÍ f(n) MỚI:\n"

        if node.state == goal:
            trace += f"   [🎯] Đã tìm được cấu hình ĐÍCH tối ưu nhất!\n"
            history_log.append({'current_node': node.state, 'frontier': [(n.cost, n.state) for n in frontier], 'explored': list(explored.keys()), 'trace_text': trace})
            return node, nodes_expanded, history_log

        for s, a in get_possible_moves(node.state):
            g_child = node.depth + 1
            h_child = count_misplaced_tiles(s, goal)
            f_child = g_child + h_child

            if s not in explored:
                in_frontier = False
                for f_node in frontier:
                    if f_node.state == s:
                        in_frontier = True
                        if f_child < f_node.cost:
                            trace += f"   [🔄 Cập nhật f] Tối ưu hóa lộ trình tới {s}: f cũ {f_node.cost} -> f mới {f_child}\n"
                            f_node.cost = f_child
                            f_node.depth = g_child
                            f_node.heuristic = h_child
                            f_node.parent = node
                            f_node.action = a
                            heapq.heapify(frontier)
                        break
                if not in_frontier:
                    child = PuzzleNode(s, parent=node, action=a, cost=f_child, depth=g_child, heuristic=h_child)
                    heapq.heappush(frontier, child)
                    trace += f"   [+] Thêm vào Heap: [{a}] -> {s} (f={f_child})\n"

        current_frontier_data = [(n.cost, n.state) for n in frontier]
        history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': list(explored.keys()), 'trace_text': trace})
        
    return None, nodes_expanded, history_log

def run_idastar(start, goal, max_limit=3000):
    history_log = []
    trace_init_total = f"🧩 [THUẬT TOÁN: IDA* - ITERATIVE DEEPENING A*]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO TỔNG QUAN)\n--------------------------------------------------\n▶️ Chuẩn bị tiến hành tìm kiếm sâu dần trên cơ sở ngưỡng chặn Bound f(n).\n"
    history_log.append({'current_node': start, 'frontier': [(count_misplaced_tiles(start, goal), start)], 'explored': [], 'trace_text': trace_init_total})

    def search(node, g, bound, history_log, context_dict):
        context_dict['nodes_expanded'] += 1
        f = g + count_misplaced_tiles(node.state, goal)
        current_frontier_data = [(bound, node.state)]

        trace = f"🧩 [THUẬT TOÁN: IDA*]\n📈 NÚT DUYỆT THỨ #{context_dict['nodes_expanded']} | BOUND = {bound}\n--------------------------------------------------\n▶️ Phân tích trạng thái: {node.state}\n   + g = {g}, h = {count_misplaced_tiles(node.state, goal)} => f = {f}\n"

        if f > bound:
            trace += f"   [❌ VƯỢT NGƯỠNG] f = {f} > Bound = {bound}. Ngắt nhánh.\n"
            history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': [], 'trace_text': trace})
            return f, None
        if node.state == goal:
            trace += f"   [🎯🎯🎯] TÌM THẤY ĐÍCH TRONG TẦNG GIỚI HẠN BOUND!\n"
            history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': [], 'trace_text': trace})
            return "FOUND", node

        min_val = float('inf')
        history_log.append({'current_node': node.state, 'frontier': current_frontier_data, 'explored': [], 'trace_text': trace})

        for s, a in get_possible_moves(node.state):
            if node.parent and s == node.parent.state: continue
            child = PuzzleNode(s, parent=node, action=a, depth=g+1)
            t, res_node = search(child, g + 1, bound, history_log, context_dict)
            if t == "FOUND": return "FOUND", res_node
            if t < min_val: min_val = t
        return min_val, None

    bound = count_misplaced_tiles(start, goal)
    root_node = PuzzleNode(start, depth=0)
    context_dict = {'nodes_expanded': 0}

    while True:
        trace_bound = f"🔄 --- IDA* KHỞI CHẠY VÒNG QUÉT MỚI VỚI GIỚI HẠN BOUND = {bound} ---\n"
        history_log.append({'current_node': start, 'frontier': [(bound, start)], 'explored': [], 'trace_text': trace_bound})
        t, res_node = search(root_node, 0, bound, history_log, context_dict)
        if t == "FOUND": return res_node, context_dict['nodes_expanded'], history_log
        if t == float('inf') or context_dict['nodes_expanded'] > max_limit: return None, context_dict['nodes_expanded'], history_log
        bound = t

# =========================================================================
# THUẬT TOÁN LOCAL SEARCH & LEO ĐỒI (8 ĐẾN 12)
# =========================================================================

def run_hill_climbing(start, goal):
    history_log = []
    h_start = count_misplaced_tiles(start, goal)
    trace_init = f"⛰️ [THUẬT TOÁN: LEO ĐỒI ĐƠN GIẢN - SIMPLE HILL CLIMBING]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO ĐỈNH ĐỒI)\n--------------------------------------------------\n▶️ Trạng thái xuất phát: {start} | h(n) = {h_start}\n"
    history_log.append({'current_node': start, 'frontier': [], 'explored': [], 'trace_text': trace_init})

    current_node = PuzzleNode(start, cost=h_start, heuristic=h_start)
    nodes_expanded = 0

    while True:
        nodes_expanded += 1
        trace = f"⛰️ [THUẬT TOÁN: LEO ĐỒI ĐƠN GIẢN]\n⏳ BƯỚC KHẢO SÁT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Điểm đứng hiện tại: {current_node.state} | h = {current_node.heuristic}\n\n"

        if current_node.state == goal:
            trace += f"   [🎯] Tìm thấy ĐÍCH hoàn hảo thành công!\n"
            history_log.append({'current_node': current_node.state, 'frontier': [], 'explored': [], 'trace_text': trace})
            return current_node, nodes_expanded, history_log

        neighbors = get_possible_moves(current_node.state)
        found_better = False
        neighbor_list_data = []

        trace += f"🌿 Sinh LẦN LƯỢT các lân cận (Gặp nút tốt hơn sẽ CHỐT NGAY & NGẮT SINH):\n"
        for s, a in neighbors:
            h_val = count_misplaced_tiles(s, goal)
            neighbor_list_data.append((h_val, s))
            
            if h_val < current_node.heuristic:
                trace += f"   [+ Chọn ngay] Nhánh [{a}] -> {s} có h = {h_val} (< {current_node.heuristic}).\n"
                trace += f"   🛑 ĐÃ TỐI ƯU HƠN! Chặn đứng hoàn toàn việc sinh các lân cận còn lại.\n"
                next_node = PuzzleNode(s, parent=current_node, action=a, cost=h_val, depth=current_node.depth+1, heuristic=h_val)
                found_better = True
                history_log.append({'current_node': current_node.state, 'frontier': list(neighbor_list_data), 'explored': [], 'trace_text': trace})
                break
            else:
                trace += f"   [x Xem xét] Nhánh [{a}] -> {s} có h = {h_val} (Không tốt hơn hiện tại h = {current_node.heuristic})\n"

        if found_better:
            current_node = next_node
        else:
            trace += f"\n   [🛑 KẸT CỰC ĐẠI CỤC BỘ / LOCAL MAXIMUM]\n   + Tất cả lân cận đã duyệt qua đều không tốt hơn hiện tại.\n"
            history_log.append({'current_node': current_node.state, 'frontier': neighbor_list_data, 'explored': [], 'trace_text': trace})
            return None, nodes_expanded, history_log

def run_steepest_ascent_hill_climbing(start, goal):
    history_log = []
    h_start = count_misplaced_tiles(start, goal)
    trace_init = f"⛰️💥 [THUẬT TOÁN: LEO ĐỒI DỐC ĐỨNG - STEEPEST-ASCENT]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO ĐỈNH ĐỒI)\n--------------------------------------------------\n▶️ Trạng thái xuất phát: {start} | h(n) = {h_start}\n"
    history_log.append({'current_node': start, 'frontier': [], 'explored': [], 'trace_text': trace_init})

    current_node = PuzzleNode(start, cost=h_start, heuristic=h_start)
    nodes_expanded = 0

    while True:
        nodes_expanded += 1
        trace = f"⛰️💥 [THUẬT TOÁN: LEO ĐỒI DỐC ĐỨNG]\n⏳ BƯỚC KHẢO SÁT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Điểm đứng hiện tại: {current_node.state} | h = {current_node.heuristic}\n\n"

        if current_node.state == goal:
            trace += f"   [🎯] Tìm thấy ĐÍCH hoàn hảo thành công!\n"
            history_log.append({'current_node': current_node.state, 'frontier': [], 'explored': [], 'trace_text': trace})
            return current_node, nodes_expanded, history_log

        neighbors = get_possible_moves(current_node.state)
        neighbor_list_data = []

        trace += f"🌿 Sinh TOÀN BỘ các lân cận để so sánh diện rộng:\n"
        best_neighbor_state = None
        best_neighbor_action = None
        best_neighbor_h = float('inf')

        for s, a in neighbors:
            h_val = count_misplaced_tiles(s, goal)
            neighbor_list_data.append((h_val, s))
            trace += f"   [+ Khảo sát] Nhánh [{a}] -> {s} có h = {h_val}\n"
            
            if h_val < best_neighbor_h:
                best_neighbor_h = h_val
                best_neighbor_state = s
                best_neighbor_action = a

        trace += f"\n   📊 Kết quả thu hoạch: Trạng thái con tốt nhất có h = {best_neighbor_h}\n"

        if best_neighbor_h < current_node.heuristic:
            trace += f"   👉 Chấp nhận! Lấy nút tốt nhất [{best_neighbor_action}] với h = {best_neighbor_h} làm điểm đứng mới.\n"
            current_node = PuzzleNode(best_neighbor_state, parent=current_node, action=best_neighbor_action, cost=best_neighbor_h, depth=current_node.depth+1, heuristic=best_neighbor_h)
            history_log.append({'current_node': current_node.state, 'frontier': neighbor_list_data, 'explored': [], 'trace_text': trace})
        else:
            trace += f"\n   [🛑 KẸT CỰC ĐẠI CỤC BỘ / LOCAL MAXIMUM]\n   + Trạng thái con tốt nhất (h = {best_neighbor_h}) không tối ưu hơn hiện tại (h = {current_node.heuristic}).\n"
            history_log.append({'current_node': current_node.state, 'frontier': neighbor_list_data, 'explored': [], 'trace_text': trace})
            return None, nodes_expanded, history_log

def run_stochastic_hill_climbing(start, goal):
    history_log = []
    h_start = count_manhattan_distance(start, goal)
    
    trace_init = f"⛰️🎲 [THUẬT TOÁN: LEO ĐỒI NGẪU NHIÊN - STOCHASTIC]\n⏳ VÒNG LẶP DUYỆT THỨ #0 (KHỞI TẠO ĐỈNH ĐỒI)\n--------------------------------------------------\n▶️ Trạng thái xuất phát: {start} | h_Manhattan(n) = {h_start}\n"
    history_log.append({'current_node': start, 'frontier': [], 'explored': [], 'trace_text': trace_init})

    current_node = PuzzleNode(start, cost=h_start, heuristic=h_start)
    nodes_expanded = 0

    while True:
        nodes_expanded += 1
        trace = f"⛰️🎲 [THUẬT TOÁN: LEO ĐỒI NGẪU NHIÊN]\n⏳ BƯỚC KHẢO SÁT THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Điểm đứng hiện tại: {current_node.state} | h = {current_node.heuristic}\n\n"

        if current_node.state == goal:
            trace += f"   [🎯] Tìm thấy ĐÍCH hoàn hảo thành công!\n"
            history_log.append({'current_node': current_node.state, 'frontier': [], 'explored': [], 'trace_text': trace})
            return current_node, nodes_expanded, history_log

        neighbors = get_possible_moves(current_node.state)
        better_neighbors_list = []
        raw_neighbor_data = []

        trace += f"🌿 Khảo sát lân cận và lọc tập tốt hơn (Better_Neighbors):\n"
        for s, a in neighbors:
            h_val = count_manhattan_distance(s, goal)
            raw_neighbor_data.append([h_val, s, a, False])
            
            if h_val < current_node.heuristic:
                trace += f"   [+ Lọt tập tốt] Nhánh [{a}] -> {s} có h = {h_val} (< {current_node.heuristic})\n"
                child_node = PuzzleNode(s, parent=current_node, action=a, cost=h_val, depth=current_node.depth+1, heuristic=h_val)
                better_neighbors_list.append(child_node)
            else:
                trace += f"   [x Loại bỏ]      Nhánh [{a}] -> {s} có h = {h_val} (Không tốt hơn)\n"

        if not better_neighbors_list:
            trace += f"\n   [🛑 KẸT CỰC ĐẠI CỤC BỘ / LOCAL MAXIMUM]\n"
            trace += f"   + Tập Better_Neighbors RỖNG! Không có lân cận nào tối ưu hơn.\n"
            history_log.append({'current_node': current_node.state, 'frontier': raw_neighbor_data, 'explored': [], 'trace_text': trace})
            return None, nodes_expanded, history_log
        else:
            chosen_node = random.choice(better_neighbors_list)
            
            for item in raw_neighbor_data:
                if item[1] == chosen_node.state:
                    item[3] = True
                    
            trace += f"\n   🎲 Số lượng con tốt hơn: {len(better_neighbors_list)} nút.\n"
            trace += f"   👉 Chọn NGẪU NHIÊN: Lấy nhánh [{chosen_node.action}] -> {chosen_node.state} làm điểm đứng mới.\n"
            current_node = chosen_node
            history_log.append({'current_node': current_node.state, 'frontier': raw_neighbor_data, 'explored': [], 'trace_text': trace})

def run_random_restart_hill_climbing(start, goal, max_restart=5):
    history_log = []
    total_steps = 0
    
    trace_init = f"🔄⛰️ [THUẬT TOÁN: LEO ĐỒI KHỞI ĐỘNG LẠI NGẪU NHIÊN]\n"
    trace_init += f"⚙️ Cấu hình MAX_RESTART = {max_restart} lượt khởi động lại tối đa.\n"
    trace_init += f"--------------------------------------------------\n"
    history_log.append({'current_node': start, 'frontier': [], 'explored': [], 'trace_text': trace_init})

    for i in range(1, max_restart + 1):
        if i == 1:
            current_state = start
        else:
            current_state = generate_random_solvable_state(goal, steps=22)
            
        h_start = count_manhattan_distance(current_state, goal)
        current_node = PuzzleNode(current_state, cost=h_start, heuristic=h_start)
        
        trace_turn = f"🔄 🔥 [LƯỢT RESTART KHỞI ĐỘNG LẠI MỚI MẺ: i = {i} / {max_restart}]\n"
        trace_turn += f"🎲 Trạng thái được bốc thăm cho lượt này: {current_state} | h_Manhattan = {h_start}\n"
        trace_turn += f"==================================================\n"
        history_log.append({'current_node': current_state, 'frontier': [], 'explored': [], 'trace_text': trace_turn})

        while True:
            total_steps += 1
            trace = f"🔄 [LƯỢT RESTART: i = {i}] | BƯỚC KHẢO SÁT CHUNG THỨ #{total_steps}\n"
            trace += f"--------------------------------------------------\n"
            trace += f"▶️ Điểm đứng hiện tại: {current_node.state} | h = {current_node.heuristic}\n\n"

            if current_node.state == goal:
                trace += f"   [🎯🎯🎯] TUYỆT VỜI! TẠI LƯỢT i = {i} ĐÃ TIẾP CẬN ĐƯỢC ĐÍCH HOÀN HẢO!\n"
                history_log.append({'current_node': current_node.state, 'frontier': [], 'explored': [], 'trace_text': trace})
                return current_node, total_steps, history_log

            neighbors = get_possible_moves(current_node.state)
            better_neighbors_list = []
            raw_neighbor_data = []

            trace += f"🌿 Khảo sát lân cận và lọc tập tốt hơn (Value tốt hơn):\n"
            for s, a in neighbors:
                h_val = count_manhattan_distance(s, goal)
                raw_neighbor_data.append([h_val, s, a, False])
                
                if h_val < current_node.heuristic:
                    trace += f"   [+] Nhánh con tốt: [{a}] -> {s} (h = {h_val})\n"
                    better_neighbors_list.append(PuzzleNode(s, parent=current_node, action=a, cost=h_val, depth=current_node.depth+1, heuristic=h_val))
                else:
                    trace += f"   [x] Nhánh con kém: [{a}] -> {s} (h = {h_val})\n"

            if not better_neighbors_list:
                trace += f"\n   [🛑 LƯỢT CHẠY i = {i} BỊ KẸT CỰC ĐẠI CỤC BỘ]\n"
                trace += f"   ❌ Tập Better_Neighbors trống rỗng! Không thể đi tiếp.\n"
                history_log.append({'current_node': current_node.state, 'frontier': raw_neighbor_data, 'explored': [], 'trace_text': trace})
                break 
            else:
                chosen_node = random.choice(better_neighbors_list)
                
                for item in raw_neighbor_data:
                    if item[1] == chosen_node.state:
                        item[3] = True
                        
                trace += f"\n   🎲 [Lượt i = {i}] Bốc thăm ngẫu nhiên trong {len(better_neighbors_list)} con tối ưu hơn:\n"
                trace += f"   👉 Lấy nhánh [{chosen_node.action}] -> {chosen_node.state} làm điểm đứng mới.\n"
                current_node = chosen_node
                history_log.append({'current_node': current_node.state, 'frontier': raw_neighbor_data, 'explored': [], 'trace_text': trace})

    trace_fail = f"❌ KẾT QUẢ CUỐI CÙNG: THẤT BẠI HOÀN TOÀN!\n"
    history_log.append({'current_node': start, 'frontier': [], 'explored': [], 'trace_text': trace_fail})
    return None, total_steps, history_log

def run_local_beam_search(start, goal, k=4):
    history_log = []
    nodes_expanded = 0
    
    current_state_set = [start]
    for _ in range(k - 1):
        random_s = generate_random_solvable_state(start, steps=random.randint(5, 15))
        if random_s not in current_state_set:
            current_state_set.append(random_s)
        else:
            current_state_set.append(generate_random_solvable_state(goal, steps=20))

    current_nodes = [PuzzleNode(s, cost=count_manhattan_distance(s, goal), heuristic=count_manhattan_distance(s, goal)) for s in current_state_set]

    trace_init = f"🌿🔦 [THUẬT TOÁN: TÌM KIẾM CHÙM CỤC BỘ - LOCAL BEAM SEARCH]\n⚙️ Cấu hình độ rộng chùm k = {k}\n--------------------------------------------------\n▶️ Khởi tạo chùm trạng thái ban đầu (Current_State_set):\n"
    for idx, n in enumerate(current_nodes):
        trace_init += f"   + Nút [{idx}]: {n.state} | h_Manhattan = {n.heuristic}\n"
    history_log.append({'current_node': start, 'frontier': [], 'explored': [], 'trace_text': trace_init})

    while True:
        nodes_expanded += 1
        trace = f"🌿 🔦 [LOCAL BEAM SEARCH] | BƯỚC DUYỆT CHÙM THỨ #{nodes_expanded}\n--------------------------------------------------\n▶️ Chùm hiện tại đang đứng ở các trạng thái:\n"
        for n in current_nodes:
            trace += f"   • {n.state} (h = {n.heuristic})\n"
        trace += f"\n"

        for n in current_nodes:
            if n.state == goal:
                trace += f"   [🎯] Tìm thấy ĐÍCH ngay trong tập chùm hiện thời!\n"
                history_log.append({'current_node': n.state, 'frontier': [], 'explored': [], 'trace_text': trace})
                return n, nodes_expanded, history_log

        neighbor_nodes_pool = []
        raw_frontier_data = []

        trace += f"🔄 [2.1] TIẾN HÀNH SINH CÁC LÂN CẬN CHO TOÀN BỘ CHÙM:\n"
        for idx, p_node in enumerate(current_nodes):
            moves = get_possible_moves(p_node.state)
            trace += f"   + Từ Nút chùm [{idx}] -> Sinh được {len(moves)} nhánh con:\n"
            for s, a in moves:
                h_val = count_manhattan_distance(s, goal)
                child = PuzzleNode(s, parent=p_node, action=a, cost=h_val, depth=p_node.depth+1, heuristic=h_val)
                neighbor_nodes_pool.append(child)
                raw_frontier_data.append([h_val, s, a, False])
                trace += f"     -> Nhánh [{a}] tới {s} (h = {h_val})\n"

        trace += f"\n🔍 [2.2] KIỂM TRA ĐÍCH TRÊN TẬP LÂN CẬN CHUNG:\n"
        for child in neighbor_nodes_pool:
            if child.state == goal:
                trace += f"   [🎯🎯🎯] TÌM THẤY ĐÍCH TRONG TẬP LÂN CẬN: {child.state}! Dừng thuật toán.\n"
                for item in raw_frontier_data:
                    if item[1] == goal: item[3] = True
                history_log.append({'current_node': child.state, 'frontier': raw_frontier_data, 'explored': [], 'trace_text': trace})
                return child, nodes_expanded, history_log
        trace += f"   -> Chưa thấy trạng thái đích nào trong {len(neighbor_nodes_pool)} nút lân cận.\n"

        trace += f"\n📊 [2.3] LỰA CHỌN CHÙM (Sắp xếp hàm h tốt dần để lấy {k} nút tốt nhất):\n"
        neighbor_nodes_pool.sort(key=lambda x: x.heuristic)
        next_nodes = neighbor_nodes_pool[:k]

        chosen_states = [n.state for n in next_nodes]
        for item in raw_frontier_data:
            if item[1] in chosen_states:
                item[3] = True

        trace += f"   👉 Đã chọn xong {k} trạng thái tốt nhất đưa vào vòng lặp sau:\n"
        for i, n in enumerate(next_nodes):
            trace += f"     [{i}] {n.state} với h = {n.heuristic}\n"
        
        current_nodes = next_nodes
        history_log.append({'current_node': current_nodes[0].state, 'frontier': raw_frontier_data, 'explored': [n.state for n in current_nodes], 'trace_text': trace})

# =========================================================================
# GIAO DIỆN ĐỒ HỌA MÔ PHỎNG SỬ DỤNG TKINTER
# =========================================================================
class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Advanced Workspace Analyser (12 Algorithms Loaded)")
        self.root.geometry("1350x780")
        self.root.configure(bg="#f5f6fa")

        self.initial_state = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        
        self.algorithm_history = []
        self.current_step_index = 0
        self.is_playing = False
        self.auto_job = None
        self.saved_res_node = None 
        self.has_solution = False 

        self.create_widgets()
        self.update_board_visual(self.initial_state)

    def create_widgets(self):
        main_paned = tk.PanedWindow(self.root, orient="horizontal", bg="#f5f6fa")
        main_paned.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_paned, bg="#f5f6fa")
        main_paned.add(left_frame, width=430)

        # --- KHUNG CẤU HÌNH ĐẦU VÀO SỬ DỤNG GRID RỘNG RÃI, KHÔNG LO BỊ ĐÈ CHỮ ---
        cfg_box = tk.LabelFrame(left_frame, text=" Cấu hình thuật toán & Bài toán ", font=("Helvetica", 10, "bold"), fg="#2980b9", bg="#f5f6fa")
        cfg_box.pack(fill="x", pady=5, ipady=5)
        
        self.algo_combo = ttk.Combobox(cfg_box, values=[
            "BFS (Breadth-First Search)", 
            "DFS (Depth-First Search)", 
            "IDS (Iterative Deepening)", 
            "UCS (Uniform Cost Search)",
            "Greedy (Best-First Search)",
            "A* Search (g + h)",
            "IDA* (Iterative Deepening A*)",
            "Hill Climbing (Leo đồi đơn giản)",
            "Steepest Hill Climbing (Leo đồi dốc đứng)",
            "Stochastic Hill Climbing (Leo đồi ngẫu nhiên)",
            "Random Restart Hill Climbing (Leo đồi lặp ngẫu nhiên)",
            "Local Beam Search (Tìm kiếm chùm cục bộ)"
        ], font=("Helvetica", 9), state="readonly")
        self.algo_combo.current(7) 
        self.algo_combo.pack(fill="x", padx=15, pady=6)

        io_frame = tk.Frame(cfg_box, bg="#f5f6fa")
        io_frame.pack(fill="x", padx=15, pady=4)
        io_frame.columnconfigure(1, weight=1)
        io_frame.columnconfigure(3, weight=1)

        tk.Label(io_frame, text="Trạng thái ĐẦU:", font=("Helvetica", 9, "bold"), bg="#f5f6fa", fg="#34495e").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_start = tk.Entry(io_frame, font=("Courier New", 10, "bold"), justify="center", bd=1, relief="solid")
        self.entry_start.insert(0, "1 2 3 4 0 6 7 5 8")
        self.entry_start.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=2)
        
        tk.Label(io_frame, text="Trạng thái ĐÍCH:", font=("Helvetica", 9, "bold"), bg="#f5f6fa", fg="#34495e").grid(row=0, column=2, sticky="w", pady=2)
        self.entry_goal = tk.Entry(io_frame, font=("Courier New", 10, "bold"), justify="center", bd=1, relief="solid")
        self.entry_goal.insert(0, "1 2 3 4 5 6 7 8 0")
        self.entry_goal.grid(row=0, column=3, sticky="ew", padx=(5, 0), pady=2)

        tk.Button(cfg_box, text="🔄 Cập nhật ma trận tùy chỉnh", font=("Helvetica", 9, "bold"), bg="#718093", fg="white", bd=0, cursor="hand2", command=self.submit_custom_states).pack(fill="x", padx=15, pady=(6, 2))
        
        self.btn_solve = tk.Button(left_frame, text="⚡ XUẤT NGAY ĐƯỜNG ĐI LỜI GIẢI ĐÍCH", font=("Helvetica", 10, "bold"), bg="#1e90ff", fg="white", bd=0, height=2, cursor="hand2", command=self.solve_and_print_immediately)
        self.btn_solve.pack(fill="x", pady=4)

        self.lbl_status = tk.Label(left_frame, text="Sẵn sàng khảo sát.", font=("Helvetica", 9, "bold"), bg="#f5f6fa", fg="#7f8c8d")
        self.lbl_status.pack()

        self.board_frame = tk.Frame(left_frame, bg="#a4b0be", bd=2, relief="solid")
        self.board_frame.pack(pady=2)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(left_frame, text="", font=("Helvetica", 16, "bold"), width=4, height=2, relief="flat", state="disabled")
            btn.grid(in_=self.board_frame, row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

        playback_group = tk.LabelFrame(left_frame, text=" Bộ điều khiển xem tiến trình từng bước duyệt ", font=("Helvetica", 9), bg="#f5f6fa")
        playback_group.pack(fill="x", pady=2)
        btn_box = tk.Frame(playback_group, bg="#f5f6fa")
        btn_box.pack(pady=2, fill="x")
        self.btn_prev = tk.Button(btn_box, text="⏮️", command=self.prev_step, state="disabled", width=4)
        self.btn_prev.pack(side="left", expand=True)
        self.btn_pause = tk.Button(btn_box, text="⏸️", command=self.pause_simulation, state="disabled", width=4)
        self.btn_pause.pack(side="left", expand=True)
        self.btn_continue = tk.Button(btn_box, text="▶️ Go", bg="#2ecc71", fg="white", font=("Helvetica", 9, "bold"), command=self.continue_simulation, width=6)
        self.btn_continue.pack(side="left", expand=True)
        self.btn_next = tk.Button(btn_box, text="⏭️", command=self.next_step, state="disabled", width=4)
        self.btn_next.pack(side="left", expand=True)
        self.btn_reset = tk.Button(btn_box, text="🔄", bg="#e74c3c", fg="white", command=self.reset_simulation, state="disabled", width=4)
        self.btn_reset.pack(side="left", expand=True)
        self.lbl_progress = tk.Label(playback_group, text="Vòng duyệt: 0 / 0", font=("Helvetica", 8, "italic"), bg="#f5f6fa")
        self.lbl_progress.pack()

        solution_panel = tk.LabelFrame(left_frame, text=" 🌟 CHI TIẾT ĐƯỜNG ĐI LỜI GIẢI KẾT QUẢ ", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#27ae60")
        solution_panel.pack(fill="both", expand=True, pady=4)
        self.txt_solution_path = tk.Text(solution_panel, wrap="word", font=("Courier New", 9, "bold"), bg="#1e272e", fg="#7bed9f", bd=0)
        scr_s = tk.Scrollbar(solution_panel, command=self.txt_solution_path.yview)
        self.txt_solution_path.configure(yscrollcommand=scr_s.set)
        scr_s.pack(side="right", fill="y")
        self.txt_solution_path.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        right_frame = tk.Frame(main_paned, bg="#f5f6fa")
        main_paned.add(right_frame, width=880)

        trace_panel = tk.LabelFrame(right_frame, text=" Nhật ký bóc tách trạng thái hiện thời & Khảo sát nhánh con ", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#c0392b")
        trace_panel.pack(fill="both", expand=True, pady=2)
        self.txt_trace = tk.Text(trace_panel, wrap="word", font=("Courier New", 9), bg="#2f3542", fg="#7fffd4", bd=0)
        scr_t = tk.Scrollbar(trace_panel, command=self.txt_trace.yview)
        self.txt_trace.configure(yscrollcommand=scr_t.set)
        scr_t.pack(side="right", fill="y")
        self.txt_trace.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        bottom_paned = tk.PanedWindow(right_frame, orient="horizontal", bg="#f5f6fa")
        bottom_paned.pack(fill="both", expand=True, pady=2)

        self.front_panel = tk.LabelFrame(bottom_paned, text=" Nhánh lân cận (Đang sinh thực tế) ", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#2980b9")
        bottom_paned.add(self.front_panel, width=440)
        self.txt_frontier = tk.Text(self.front_panel, wrap="none", font=("Courier New", 9), bg="#1e272e", fg="#ffffff", bd=0)
        scr_f = tk.Scrollbar(self.front_panel, command=self.txt_frontier.yview)
        self.txt_frontier.configure(yscrollcommand=scr_f.set)
        scr_f.pack(side="right", fill="y")
        self.txt_frontier.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        explored_panel = tk.LabelFrame(bottom_paned, text=" Explored List (Trạng thái đóng trùng lặp) ", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#27ae60")
        bottom_paned.add(explored_panel, width=440)
        self.txt_explored = tk.Text(explored_panel, wrap="none", font=("Courier New", 9), bg="#1e272e", fg="#a4b0be", bd=0)
        scr_e = tk.Scrollbar(explored_panel, command=self.txt_explored.yview)
        self.txt_explored.configure(yscrollcommand=scr_e.set)
        scr_e.pack(side="right", fill="y")
        self.txt_explored.pack(side="left", fill="both", expand=True, padx=2, pady=2)

    def update_board_visual(self, current_state, parent_state=None):
        moved_index = parent_state.index(0) if parent_state else None
        for i in range(9):
            val = current_state[i]
            if val == 0: self.buttons[i].config(text="", bg="#34495e")
            elif i == moved_index: self.buttons[i].config(text=str(val), bg="#f1c40f", fg="#000000")
            else: self.buttons[i].config(text=str(val), bg="#ffffff", fg="#2f3542")

    def reset_simulation_on_algo_change(self):
        self.pause_simulation()
        self.algorithm_history = []
        self.current_step_index = 0
        self.has_solution = False
        self.saved_res_node = None
        self.update_board_visual(self.initial_state)
        self.txt_trace.delete("1.0", tk.END)
        self.txt_frontier.delete("1.0", tk.END)
        self.txt_explored.delete("1.0", tk.END)
        self.txt_solution_path.delete("1.0", tk.END)
        
        algo_choice = self.algo_combo.get()
        if "BFS" in algo_choice: self.front_panel.config(text=" Frontier List (Hàng đợi Queue - FIFO) ")
        elif "DFS" in algo_choice: self.front_panel.config(text=" Frontier List (Ngăn xếp Stack - LIFO) ")
        elif "IDS" in algo_choice: self.front_panel.config(text=" Frontier List (Ngăn xếp Stack DFS giới hạn tầng) ")
        elif "UCS" in algo_choice: self.front_panel.config(text=" Frontier List (Min-Heap sắp xếp theo g(n)) ")
        elif "Greedy" in algo_choice: self.front_panel.config(text=" Frontier List (Min-Heap ưu tiên theo h(n)) ")
        elif "A*" in algo_choice: self.front_panel.config(text=" Frontier List (Min-Heap sắp xếp theo f(n) = g + h) ")
        elif "IDA*" in algo_choice: self.front_panel.config(text=" Frontier Trạng thái duyệt theo Bound f(n) ")
        elif "Beam" in algo_choice: self.front_panel.config(text=" Toàn bộ lân cận sinh ra (Neighbor_States) ")
        else: self.front_panel.config(text=" Nhánh lân cận (Đang sinh thực tế) ")

        self.lbl_status.config(text="Đã chuyển thuật toán. Hãy nhấn nút Go!", fg="#e67e22")
        self.lbl_progress.config(text="Vòng duyệt: 0 / 0")
        self.disable_playback_buttons()
        self.btn_continue.config(state="normal")

    def submit_custom_states(self):
        try:
            s_str = self.entry_start.get().strip().split()
            g_str = self.entry_goal.get().strip().split()
            if len(s_str) != 9 or len(g_str) != 9: raise ValueError
            self.initial_state = tuple(int(x) for x in s_str)
            self.goal_state = tuple(int(x) for x in g_str)
            if set(self.initial_state) != set(range(9)): raise ValueError
            self.reset_simulation_on_algo_change()
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Chuỗi số nhập vào phải từ 0 đến 8 và cách nhau bởi khoảng trắng.")

    def calculate_solution_background(self):
        algo_choice = self.algo_combo.get()
        if "BFS" in algo_choice: res_node, nodes, history = run_bfs(self.initial_state, self.goal_state)
        elif "DFS" in algo_choice: res_node, nodes, history = run_dfs(self.initial_state, self.goal_state)
        elif "IDS" in algo_choice: res_node, nodes, history = run_ids(self.initial_state, self.goal_state)
        elif "UCS" in algo_choice: res_node, nodes, history = run_ucs(self.initial_state, self.goal_state)
        elif "Greedy" in algo_choice: res_node, nodes, history = run_greedy(self.initial_state, self.goal_state)
        elif "A*" in algo_choice: res_node, nodes, history = run_astar(self.initial_state, self.goal_state)
        elif "IDA*" in algo_choice: res_node, nodes, history = run_idastar(self.initial_state, self.goal_state)
        elif "đơn giản" in algo_choice: res_node, nodes, history = run_hill_climbing(self.initial_state, self.goal_state)
        elif "dốc đứng" in algo_choice: res_node, nodes, history = run_steepest_ascent_hill_climbing(self.initial_state, self.goal_state)
        elif "ngẫu nhiên" in algo_choice and "lặp" not in algo_choice: res_node, nodes, history = run_stochastic_hill_climbing(self.initial_state, self.goal_state)
        elif "lặp" in algo_choice: res_node, nodes, history = run_random_restart_hill_climbing(self.initial_state, self.goal_state, max_restart=5)
        else: res_node, nodes, history = run_local_beam_search(self.initial_state, self.goal_state, k=3)

        self.algorithm_history = history
        self.saved_res_node = res_node

        if res_node is None:
            if any(key in algo_choice for key in ["đơn giản", "dốc đứng", "ngẫu nhiên", "Hill Climbing", "lặp", "Beam"]):
                self.lbl_status.config(text="KẸT CỰC ĐẠI CỤC BỘ / THẤT BẠI!", fg="#e74c3c")
            else:
                self.lbl_status.config(text="Không tìm thấy lời giải trong giới hạn quét!", fg="#e74c3c")
            self.has_solution = True  
            return True

        self.has_solution = True
        return True

    def print_solution_log(self):
        self.txt_solution_path.delete("1.0", tk.END)
        if not self.saved_res_node:
            self.txt_solution_path.insert(tk.END, "❌ KHÔNG TÌM ĐƯỢC LỜI GIẢI ĐÍCH!\n(Giải thuật kết thúc tại nút cực đại cục bộ)")
            return
        
        solution_nodes = []
        curr = self.saved_res_node
        while curr is not None:
            solution_nodes.append(curr)
            curr = curr.parent
        solution_nodes.reverse()

        algo_name = self.algo_combo.get().split()[0]
        self.txt_solution_path.insert(tk.END, f"🌟 ĐƯỜNG ĐI LỜI GIẢI [{algo_name}]:\n-> Số bước: {len(solution_nodes) - 1}\n---------------------------------\n")
        for idx, node in enumerate(solution_nodes):
            if idx == 0: self.txt_solution_path.insert(tk.END, f" Trạng thái ĐẦU:\n   {node.state}\n\n")
            else: self.txt_solution_path.insert(tk.END, f" ⏩ Bước {idx}: [{node.action}] -> {node.state}\n\n")
        self.txt_solution_path.see("1.0")

    def sync_all_workspace_logs(self):
        if not self.algorithm_history or self.current_step_index >= len(self.algorithm_history): return
        step_data = self.algorithm_history[self.current_step_index]
        self.txt_trace.delete("1.0", tk.END)
        self.txt_trace.insert(tk.END, step_data['trace_text'])
        
        self.txt_frontier.delete("1.0", tk.END)
        self.txt_explored.delete("1.0", tk.END)
        algo_choice = self.algo_combo.get()
        
        if "BFS" in algo_choice:
            self.txt_frontier.insert(tk.END, f"--- QUEUE HIỆN TẠI ({len(step_data['frontier'])} nút) ---\n")
            for idx, item in enumerate(step_data['frontier']):
                state, d = item if isinstance(item, tuple) else (item, 0)
                flag = " (* ĐẦU QUEUE)" if state == step_data['current_node'] and self.current_step_index > 0 else ""
                self.txt_frontier.insert(tk.END, f"[{idx}] (d={d}): {state}{flag}\n")
        elif "DFS" in algo_choice or "IDS" in algo_choice:
            self.txt_frontier.insert(tk.END, f"--- STACK HIỆN TẠI ({len(step_data['frontier'])} nút) ---\n")
            for idx, item in enumerate(step_data['frontier']):
                state, d = item if isinstance(item, tuple) else (item, 0)
                flag = " (* ĐỈNH STACK)" if state == step_data['current_node'] and self.current_step_index > 0 else ""
                self.txt_frontier.insert(tk.END, f"[{idx}] (d={d}): {state}{flag}\n")
        elif "UCS" in algo_choice or "A*" in algo_choice:
            self.txt_frontier.insert(tk.END, f"--- MIN-HEAP SẮP XẾP ({len(step_data['frontier'])} nút) ---\n")
            for idx, item in enumerate(step_data['frontier']):
                cost, state = item[0], item[1]
                flag = " (* POP DUYỆT)" if state == step_data['current_node'] and self.current_step_index > 0 else ""
                self.txt_frontier.insert(tk.END, f"[{idx}] [Cost={cost}]: {state}{flag}\n")
        elif "Greedy" in algo_choice:
            self.txt_frontier.insert(tk.END, f"--- MIN-HEAP THEO h(n) ({len(step_data['frontier'])} nút) ---\n")
            for idx, item in enumerate(step_data['frontier']):
                h_v, state = item[0], item[1]
                flag = " (* POP DUYỆT)" if state == step_data['current_node'] and self.current_step_index > 0 else ""
                self.txt_frontier.insert(tk.END, f"[{idx}] [h={h_v}]: {state}{flag}\n")
        elif "IDA*" in algo_choice:
            self.txt_frontier.insert(tk.END, f"--- THÔNG TIN BOUND TIẾN TRÌNH ---\n")
            if step_data['frontier']:
                b_v = step_data['frontier'][0][0]
                self.txt_frontier.insert(tk.END, f"Ngưỡng chặn Bound hiện tại: {b_v}\nĐang quét sâu hạ tầng DFS...")
        elif "Hill Climbing" in algo_choice or "Steepest" in algo_choice or "Stochastic" in algo_choice or "lặp" in algo_choice or "Beam" in algo_choice:
            self.txt_frontier.insert(tk.END, f"--- LÂN CẬN (NEIGHBORS) ĐÃ SINH TRONG LƯỢT ---\n")
            if not step_data['frontier']: 
                self.txt_frontier.insert(tk.END, f"(Trống hoặc Vòng khởi tạo/Lượt lặp mới)\n")
            else:
                for idx, item in enumerate(step_data['frontier']):
                    if len(item) == 4 and ("Stochastic" in algo_choice or "lặp" in algo_choice or "Beam" in algo_choice):
                        h_v, state, action, is_chosen = item[0], item[1], item[2], item[3]
                        flag_chosen = "  ⭐ [BETTER CHỌN]" if is_chosen else ""
                        self.txt_frontier.insert(tk.END, f"[{idx}] Nhánh [{action}] h={h_v} -> {state}{flag_chosen}\n")
                    else:
                        h_v, state = item[0], item[1]
                        self.txt_frontier.insert(tk.END, f"[{idx}] Nhánh có h={h_v} -> {state}\n")
            
            if "Steepest" in algo_choice:
                self.txt_frontier.insert(tk.END, f"\n⚠️ Ghi chú dốc đứng: Sinh hết rồi lựa chọn con tốt nhất.")
            elif "lặp" in algo_choice:
                self.txt_frontier.insert(tk.END, f"\n⚠️ Ghi chú lặp ngẫu nhiên: Theo dõi chỉ số lượt lặp 'i' trên bảng Trace log. Nếu kẹt, vòng 'for' nhảy sang lượt 'i' kế tiếp cùng bàn cờ random mới.")
            elif "Stochastic" in algo_choice:
                self.txt_frontier.insert(tk.END, f"\n⚠️ Ghi chú ngẫu nhiên: Lọc những con tốt hơn hiện tại (Manhattan), rồi bốc thăm ngẫu nhiên 1 con.")
            elif "Beam" in algo_choice:
                self.txt_frontier.insert(tk.END, f"\n⚠️ Ghi chú Chùm cục bộ: Tất cả nhánh con gom chung vào tập Neighbor_States, lọc ra k=3 nút có khoảng cách Manhattan ngắn nhất đưa vào chùm kế tiếp.")
            else:
                self.txt_frontier.insert(tk.END, f"\n⚠️ Ghi chú đơn giản: Gặp cấu hình tốt hơn đầu tiên là chốt rẽ nhánh ngay!")
                
        self.txt_explored.insert(tk.END, f"--- TRẠNG THÁI CHÙM HIỆN TẠI / TẬP ĐÓNG ({len(step_data['explored'])} nút) ---\n")
        for state in step_data['explored']: self.txt_explored.insert(tk.END, f" • {state}\n")

    def update_playback_ui_state(self):
        total_history_steps = len(self.algorithm_history) - 1
        if total_history_steps < 0: return
        self.lbl_progress.config(text=f"Vòng duyệt: {self.current_step_index} / {total_history_steps}")
        self.btn_prev.config(state="normal" if self.current_step_index > 0 else "disabled")
        self.btn_next.config(state="normal" if self.current_step_index < total_history_steps else "disabled")
        self.btn_reset.config(state="normal")
        if self.is_playing:
            self.btn_pause.config(state="normal")
            self.btn_continue.config(state="disabled")
        else:
            self.btn_pause.config(state="disabled")
            self.btn_continue.config(state="normal" if self.current_step_index < total_history_steps else "disabled")

    def disable_playback_buttons(self):
        self.btn_prev.config(state="disabled")
        self.btn_pause.config(state="disabled")
        self.btn_continue.config(state="disabled")
        self.btn_next.config(state="disabled")
        self.btn_reset.config(state="disabled")

    def next_step(self):
        if self.current_step_index < len(self.algorithm_history) - 1:
            self.current_step_index += 1
            step_data = self.algorithm_history[self.current_step_index]
            prev_data = self.algorithm_history[self.current_step_index - 1]
            self.update_board_visual(step_data['current_node'], prev_data['current_node'])
            self.sync_all_workspace_logs()
            self.update_playback_ui_state()
            
            if self.current_step_index == len(self.algorithm_history) - 1:
                self.pause_simulation()
                if self.saved_res_node:
                    self.update_board_visual(self.saved_res_node.state)
                    messagebox.showinfo("Mô phỏng hoàn tất", "Thuật toán đã tìm được ĐÍCH thành công!")
                else:
                    algo_choice = self.algo_combo.get()
                    if any(k in algo_choice for k in ["Hill Climbing", "Steepest", "Stochastic", "lặp", "Beam"]):
                        messagebox.showwarning("Dừng giải thuật", "Thuật toán kết thúc (Cực đại cục bộ / Hết lượt lặp / Kẹt chùm)!")
                    else:
                        messagebox.showwarning("Mô phỏng dừng", "Không tìm được đường đi thích hợp!")
                self.print_solution_log()

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            step_data = self.algorithm_history[self.current_step_index]
            next_data = self.algorithm_history[self.current_step_index + 1]
            self.update_board_visual(step_data['current_node'], next_data['current_node'])
            self.sync_all_workspace_logs()
            self.update_playback_ui_state()

    def continue_simulation(self):
        if not self.has_solution:
            self.txt_solution_path.delete("1.0", tk.END)
            if not self.calculate_solution_background(): return
            self.current_step_index = 0
            if self.algorithm_history:
                self.update_board_visual(self.algorithm_history[0]['current_node'])
                self.sync_all_workspace_logs()

        self.is_playing = True
        algo_short = self.algo_combo.get().split()[0]
        self.lbl_status.config(text=f"Đang mô phỏng {algo_short}...", fg="#2ecc71")
        self.update_playback_ui_state()
        self.auto_play_loop()

    def pause_simulation(self):
        self.is_playing = False
        if self.auto_job:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None
        self.lbl_status.config(text="Dừng mô phỏng.", fg="#e67e22")
        self.update_playback_ui_state()

    def reset_simulation(self):
        self.pause_simulation()
        self.current_step_index = 0
        self.txt_solution_path.delete("1.0", tk.END)
        self.txt_trace.delete("1.0", tk.END)
        self.txt_frontier.delete("1.0", tk.END)
        self.txt_explored.delete("1.0", tk.END)
        self.update_board_visual(self.initial_state)
        if self.algorithm_history: self.sync_all_workspace_logs()
        self.lbl_status.config(text="Đã làm mới đồ thị lý thuyết.", fg="#7f8c8d")
        self.update_playback_ui_state()

    def solve_and_print_immediately(self):
        if self.calculate_solution_background():
            self.print_solution_log()
            if self.saved_res_node:
                self.lbl_status.config(text="Đã xuất kết quả giải thuật.", fg="#1e90ff")
            else:
                self.lbl_status.config(text="KẸT CỰC ĐẠI CỤC BỘ / THẤT BẠI!", fg="#e74c3c")

    def auto_play_loop(self):
        if self.is_playing and self.current_step_index < len(self.algorithm_history) - 1:
            self.next_step()
            self.auto_job = self.root.after(700, self.auto_play_loop)
        else:
            self.pause_simulation()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()