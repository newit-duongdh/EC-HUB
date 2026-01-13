Tổng quan kiến trúc & luồng xử lý
Luồng xử lý một request trong hệ thống:
1. Request từ bên ngoài 
2. Đi vào Controller 
3. Controller gọi Application Service
4. Application Service điều phối Domain
5. Domain thực thi nghiệp vụ, có thể phát Domain Event
6. Application / Infrastructure lắng nghe event để xử lý hạ tầng (lưu DB, gửi email…)
7. Kết quả quay lại Controller để trả response
Chiều ngược lại (Domain cần thao tác hạ tầng)
* Domain không gọi trực tiếp DB, Email, Queue
* Domain chỉ định nghĩa interface
* Application giữ interface
* Infrastructure implement interface đó
👉 Domain độc lập hoàn toàn với framework và hạ tầng

1. Core Architecture: Domain & Repository
Domain là gì?
Domain là phần quan trọng nhất của hệ thống, nơi chứa:
* Entity
* Value Object
* …
Vai trò của Domain
* Biến dữ liệu rời rạc thành đối tượng có ý nghĩa
* Kiểm soát tính hợp lệ dữ liệu ngay trong model
* Chỉ dùng ngôn ngữ lập trình thuần túy
* Không phụ thuộc framework, database, ORM
Ví dụ:
* Order::create(...)
* Product::isInStock(...)

Repository là gì?
Repository là lớp trung gian giữa Domain và Data Source.
Repository làm gì?
* Cung cấp các phương thức:
    * Lấy entity
    * Lưu entity
* Domain không biết dữ liệu được lưu ở đâu và bằng cách nào
Nguyên tắc quan trọng
* Interface Repository nằm ở Domain
* Implementation Repository nằm ở Infrastructure
Domain
 └─ OrderRepository (interface)

Infrastructure
 └─ MySQLOrderRepository implements OrderRepository

Domain & Repository trong luồng nghiệp vụ
1. Application tạo Domain Entity
2. Gọi Repository
3. Repository lưu xuống DB (Infrastructure)
4. Trả kết quả lên Application
👉 Controller không chứa nghiệp vụ👉 Logic nằm trong Domain + Application Service
Lợi ích
* Controller gọn, dễ đọc
* Domain dễ test (mock repository)
* Không lộ chi tiết DB
* Dễ thay đổi hạ tầng

2. Read Model & View Model
Sai lầm thường gặp ❌
Dùng Domain Entity (write model) cho việc đọc / hiển thị dữ liệu
👉 Hậu quả:
* Entity phình to
* Query phức tạp
* Hiệu năng kém

Giải pháp: Tách Read & Write
Write Model (Domain Entity)
* Tập trung nghiệp vụ
* Dùng cho tạo / cập nhật dữ liệu
Read Model
* Chỉ dùng để đọc / tra cứu
* Chứa đúng dữ liệu cần cho từng màn hình / báo cáo
* Có repository riêng, có thể query trực tiếp DB
View Model (DTO cho UI / API)
* Là dạng đặc biệt của Read Model
* Đóng gói dữ liệu đúng format UI cần
* Không chứa logic nghiệp vụ
Controller
 → ReadRepository
 → ViewModel
 → Render / Response
👉 UI không làm việc trực tiếp với Domain Entity

Lợi ích khi tách Read / View Model
* Truy vấn nhanh hơn
* Domain gọn gàng
* UI không phụ thuộc Domain

3. Application Service & DTO
Vấn đề khi để tất cả trong Controller ❌
* Controller phình to
* Lẫn request, nghiệp vụ, DB
* Khó test, khó tái sử dụng

Application Service là gì?
* Đại diện cho một use case
* Điều phối Domain & Repository
* Không chứa logic hạ tầng
* Có thể dùng cho nhiều endpoint khác nhau
Controller lúc này chỉ:
1. Nhận request
2. Tạo DTO
3. Gọi Application Service
4. Trả response

Ví dụ: PlaceOrder
PlaceOrderDTO
final class PlaceOrderDTO
{
    public function __construct(
        public string $customerId,
        public string $productId,
        public int $quantity
    ) {}
}

PlaceOrderService (Application Service)
final class PlaceOrderService
{
    public function __construct(
        private OrderRepository $orderRepo,
        private ProductRepository $productRepo
    ) {}

    public function handle(PlaceOrderDTO $dto): OrderId
    {
        // Lấy thông tin sản phẩm
        $product = $this->productRepo->getById($dto->productId);

        // Kiểm tra tồn kho
        if (!$product->isInStock($dto->quantity)) {
            throw new OutOfStockException();
        }

        // Tính giá trị đơn hàng
        $orderAmount = $product->price()->multiply($dto->quantity);

        // Tạo ID mới cho Order
        $orderId = $this->orderRepo->nextIdentity();

        // Tạo Domain Entity
        $order = Order::create(
            $orderId,
            $dto->customerId,
            $product,
            $dto->quantity,
            $orderAmount
        );

        // Lưu Order
        $this->orderRepo->save($order);

        return $orderId;
    }
}

Controller
$dto = new PlaceOrderDTO(
    $request->customerId,
    $request->productId,
    $request->quantity
);

$orderId = $placeOrderService->handle($dto);

return response()->json(['orderId' => $orderId]);

Tổng kết
* Domain: nghiệp vụ cốt lõi
* Repository: abstraction giữa Domain & DB
* Application Service: điều phối use case
* DTO: dữ liệu đầu vào cho use case
* Read / View Model: tối ưu cho hiển thị
