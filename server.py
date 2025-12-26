import eventlet
eventlet.monkey_patch()
import serial
import socketio
import threading

# Khởi tạo Socket.io Server (Cổng 3000)
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Cấu hình cổng COM - Thay "COM5" bằng cổng thực tế của bạn
try:
    ser = serial.Serial("COM5", 115200, timeout=1)
except Exception as e:
    print(f"Lỗi: Không thể mở cổng COM5. Chi tiết: {e}")

def read_serial():
    print("Python đang lắng nghe dữ liệu từ STM32 trên cổng 3000...")
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Chuyển chuỗi "1,2,3..." thành mảng số
                raw_data = [int(x) for x in line.split(',') if x]
                
                if len(raw_data) == 3600:
                    # Chuyển mảng phẳng thành ma trận 60x60
                    matrix = [raw_data[i:i + 60] for i in range(0, 3600, 60)]
                    sio.emit("updateData", matrix)
        except Exception:
            continue

# Chạy luồng đọc serial
threading.Thread(target=read_serial, daemon=True).start()

@sio.event
def calibrate(sid, data):
    print("Nhận lệnh hiệu chuẩn từ Web -> Gửi xuống STM32")
    ser.write(b"CAL\n")

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 3000)), app)
    