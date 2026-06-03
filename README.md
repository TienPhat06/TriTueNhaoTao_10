        Các thuật toán tìm kiếm được tích hợp

1. Uninformed Search Algorithm (Tìm kiếm mù)
Đây là nhóm thuật toán duyệt qua không gian trạng thái một cách hệ thống theo cấu trúc dữ liệu định sẵn mà không có bất kỳ thông tin gợi ý (Heuristic) nào về vị trí của trạng thái đích (Goal State).

    1.1. Breadth-First Search (BFS - Tìm kiếm theo chiều rộng):
    Duyệt theo từng tầng của cây trạng thái bằng hàng đợi deque (FIFO). Đảm bảo tìm thấy đường đi ngắn nhất nếu mọi bước đi có chi phí bằng nhau.

    1.2. Depth-First Search (DFS - Tìm kiếm theo chiều sâu):
    Duyệt sâu xuống một nhánh cho đến khi gặp trạng thái chết hoặc trạng thái lặp rồi mới quay lui, sử dụng danh sách như một Ngăn xếp (Stack - LIFO).

    1.3. Iterative Deepening Search (IDS - Tìm kiếm sâu dần):
    Khắc phục nhược điểm tốn bộ nhớ của BFS và vô hạn lặp của DFS bằng cách chạy DFS nhiều lần với giới hạn độ sâu (Depth Limit) tăng dần từ 0 cho đến khi tìm thấy đích.

    1.4. Uniform Cost Search (UCS - Tìm kiếm chi phí đồng nhất):
    Mở rộng nút có chi phí đường đi g(n) thấp nhất từ nút gốc bằng cách sử dụng hàng đợi ưu tiên (Min-Heap). Do bài toán 8-Puzzle có chi phí mỗi bước bằng 1 nên UCS trong trường hợp này hoạt động tương đương với BFS.

2. Informed Search Algorithm (Tìm kiếm có thông tin / Heuristic)
Nhóm thuật toán này sử dụng thêm hàm đánh giá Heuristic h(n) (cụ thể trong code sử dụng hàm đếm Số ô sai vị trí - Misplaced Tiles) để ước lượng khoảng cách từ trạng thái hiện tại đến đích, giúp tối ưu hóa hướng đi và giảm thiểu số nút phải bóc tách.

    2.1. Greedy Best-First Search (Tìm kiếm tham lam):
    Luôn ưu tiên mở rộng nút có giá trị Heuristic $h(n)$ nhỏ nhất (gần đích nhất về mặt cảm tính), sử dụng cấu trúc Min-Heap. Thuật toán chạy rất nhanh nhưng không đảm bảo tìm ra đường đi ngắn nhất.

    2.2. A* Search Algorithm (Tìm kiếm A*):
    Thuật toán tìm kiếm tối ưu phổ biến nhất, chọn nút mở rộng dựa trên hàm tổng chi phí f(n) = g(n) + h(n) (với g(n) là độ sâu hiện tại và h(n) là số ô sai vị trí). Đảm bảo tìm ra đường đi ngắn nhất một cách thông minh và hiệu quả.

    2.3. Iterative Deepening A* (IDA* - Tìm kiếm A* sâu dần):
    Sự kết hợp giữa tìm kiếm sâu dần (IDS) và hàm đánh giá f(n) của A*. Thuật toán sử dụng một ngưỡng chặn (Bound) dựa trên giá trị $f(n)$ thay vì độ sâu, giúp tiết kiệm tối đa bộ nhớ vì chỉ lưu trữ đường đi hiện tại trên Stack.

3. Local Search Algorithm (Tìm kiếm cục bộ)
Nhóm thuật toán tìm kiếm cục bộ hoạt động bằng cách chỉ giữ lại trạng thái hiện tại (hoặc một số lượng trạng thái giới hạn) và liên tục di chuyển sang các trạng thái lân cận có điểm số tốt hơn theo một hàm đánh giá (Sử dụng Số ô sai vị trí hoặc Khoảng cách Manhattan). Nhóm này cực kỳ tiết kiệm bộ nhớ nhưng có nguy cơ cao bị kẹt ở các cực đại cục bộ.

    3.1. Simple Hill Climbing (Leo đồi đơn giản):
    Duyệt các trạng thái lân cận, ngay khi gặp trạng thái đầu tiên có hàm đánh giá tốt hơn trạng thái hiện tại thì lập tức chọn và di chuyển sang nó mà không cần kiểm tra các lân cận còn lại.

    3.2. Steepest-Ascent Hill Climbing (Leo đồi dốc đứng): 
    Khảo sát toàn bộ các trạng thái lân cận có thể đi được từ vị trí hiện tại, so sánh tất cả và chọn ra duy nhất một trạng thái có bước cải tiến tốt nhất (độ dốc cao nhất) để di chuyển.

    3.3. Stochastic Hill Climbing (Leo đồi ngẫu nhiên): 
    Thay vì chọn bước tốt nhất, thuật toán quét các lân cận tốt hơn hiện tại, sau đó chọn ngẫu nhiên một trong số các trạng thái tốt hơn đó dựa trên độ phân bổ xác suất (Sử dụng khoảng cách Manhattan làm Heuristic).

    3.4. Random Restart Hill Climbing (Leo đồi khởi động lại ngẫu nhiên): 
    Nếu quá trình leo đồi thông thường bị rơi vào trạng thái kẹt (Local Maximum) mà chưa đạt đích, thuật toán sẽ tự động xáo trộn ma trận để tạo ra một trạng thái khởi đầu hoàn toàn mới và tiếp tục leo đồi lại từ đầu cho đến khi tìm thấy đích.

    3.5. Local Beam Search (Tìm kiếm chùm cục bộ): 
    Thay vì chỉ giữ 1 trạng thái như leo đồi, giải thuật này theo dõi song song k trạng thái (trong code thiết lập k = 4). Tại mỗi bước, sinh ra tất cả các lân cận của cả k trạng thái này, sau đó dùng Min-Heap lọc ra 4 trạng thái tốt nhất trên toàn cục để giữ lại cho bước tiếp theo.

    Hướng dẫn chạy chương trình
Bước 1: Khởi chạy ứng dụng: Mở terminal tại thư mục chứa file BTVN_10.py và chạy lệnh python BTVN_10.py. Giao diện đồ họa (GUI) của chương trình sẽ hiển thị lên màn hình.

Bước 2: Cấu hình bài toán: Bạn có thể sử dụng trạng thái mặc định của hệ thống hoặc tự nhập trạng thái ĐẦU (Initial) và ĐÍCH (Goal) bất kỳ bằng cách điền chuỗi 9 số (từ 0 đến 8, cách nhau bằng dấu cách, với 0 đại diện cho ô trống) vào các ô nhập liệu, sau đó bấm nút "Cập nhật ma trận tùy chỉnh".

Bước 3: Chọn thuật toán: Tại thanh menu cấu hình ở góc trên, nhấp vào thanh cuộn thả xuống (Combobox) để lựa chọn 1 trong 12 giải thuật bạn muốn kiểm tra hoặc phân tích.

Bước 4: Xuất lời giải nhanh: Nhấp vào nút "XUẤT NGAY ĐƯỜNG ĐI LỜI GIẢI ĐÍCH" ở góc dưới bên trái để chương trình thực hiện tính toán nền (Background) và in ngay chuỗi hành động kết quả (ví dụ: UP -> LEFT -> DOWN...) ra màn hình.

Bước 5: Trực quan hóa và Kiểm soát không gian Workspace (Playback):
    Bấm nút "▶️ Go" để hệ thống tự động chạy mô phỏng dịch chuyển các ô số (tốc độ cập nhật mặc định là 700ms).
    Bạn có thể bấm "⏸️" để tạm dừng, sử dụng hai nút tiến "⏭️" hoặc lùi "⏮️" để chủ động xem biến động dữ liệu theo từng vòng lặp (vòng lặp while của thuật toán).
    Quan sát các khung panel bên phải bao gồm: Nhật ký bóc tách trạng thái (giải thích hành động thực tế bằng tiếng Việt), Danh sách Frontier (các nút đang chờ duyệt trong hàng đợi/ngăn xếp) và Danh sách Explored (các nút đã duyệt qua) để hiểu rõ bản chất hoạt động của thuật toán.

Bước 6: Làm mới hệ thống: Bấm nút "Reset" để xóa toàn bộ lịch sử phân tích, xóa các log văn bản cũ và đưa ma trận đồ thị về lại trạng thái khởi tạo ban đầu.

    Lưu ý quan trọng
Hiện tượng kẹt cực đại cục bộ (Local Maximum): Đối với các thuật toán Tìm kiếm cục bộ như Simple Hill Climbing hay Steepest-Ascent Hill Climbing, do đặc thù giải thuật không lưu lại cây trạng thái nên rất dễ bị rơi vào trạng thái "kẹt" (không tìm được trạng thái lân cận nào tốt hơn hiện tại nhưng vẫn chưa đến được đích). Khi điều này xảy ra, hệ thống sẽ dừng lại và thông báo "KẸT CỰC ĐẠI CỤC BỘ / THẤT BẠI", đây là hành vi đúng theo lý thuyết AI của thuật toán chứ không phải lỗi chương trình.

Thời gian xử lý đối với Tìm kiếm mù (Uninformed Search): Khi bạn cấu hình các trạng thái ban đầu có độ khó cao (cần nhiều bước dịch chuyển để tới đích), các thuật toán như DFS hoặc IDS có thể mất rất nhiều thời gian để xử lý hoặc tiêu tốn bộ nhớ lớn do phải bóc tách số lượng nút khổng lồ theo cấp số nhân. Nếu chương trình có dấu hiệu bị "đơ" (Not Responding), hãy kiên nhẫn chờ đợi thuật toán hoàn thành tính toán ngầm hoặc thử lại với một trạng thái đơn giản hơn.