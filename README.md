# 🏙️ Smart City Monitoring System

> Hệ thống Giám sát Thành phố Thông minh - Nền tảng AI Edge Computing cho An ninh Đô thị


## 📋 Giới thiệu

Hệ thống web-based giám sát mạng lưới edge devices (Jetson Nano/Orin) phát hiện sự kiện an ninh đô thị real-time. Bao gồm bản đồ tương tác, phân tích thống kê, và quản lý cấu hình node/camera.

**Tính năng:** 🗺️ Interactive Map | 📊 Analytics Dashboard | ⚙️ Node Management | 🔄 Auto Refresh | 📍 Click-to-Select Location

---

## 🚀 Cài đặt

```bash
# Clone & di chuyển vào thư mục
git clone https://github.com/quanngo018/smart_city_surveilance_system.git
cd smart_city_surveilance_system/web

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

**Truy cập:** http://localhost:8503

---

## 📖 Hướng dẫn Sử dụng

### 1. Bảng Điều khiển (Main)
- **Bản đồ:** Xem vị trí node (🟢 online, 🔴 offline), click marker để xem chi tiết
- **Sự kiện:** Lọc, xem, và đánh dấu xử lý các sự kiện phát hiện

### 2. Phân tích (Stats)
- **Bộ lọc:** Chọn khoảng thời gian, loại sự kiện
- **Biểu đồ:** Line (theo ngày), Bar (theo giờ/vị trí), Pie (phân bố loại)
- **Xuất dữ liệu:** Download CSV

### 3. Cài đặt (Settings)
- **Node:** Click bản đồ → Điền form → Add/Edit/Delete
- **Camera:** Thêm/xóa camera cho từng node
- **Display:** Điều chỉnh số sự kiện hiển thị, tần suất refresh

---

## 📁 Cấu trúc Dự án

```
web/
├── app.py              # Entry point
├── config/             # Cấu hình tập trung
├── pages/              # Stats, Main, Settings pages
├── ui/                 # Theme system (modular CSS)
├── utils/              # Logger, data loader, map utils
└── data/               # nodes.csv, events.csv
```

---

## 🔧 Tùy chỉnh

**Bản đồ:** Sửa `config/settings.py` → `MAP_CONFIG`  
**Theme:** Sửa `ui/base.py` → màu sắc palettes  
**Logs:** Xem `logs/app.log`

---


**© 2025 HUST-EDABK-AIOT** | Built with ❤️ using Streamlit & Python