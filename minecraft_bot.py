import socket
import json
import struct

class MinecraftBot:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.socket = None

    def connect(self):
        # Tạo kết nối socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"Bot đã kết nối đến server {self.host}:{self.port}")
            self.login()
            self.listen()
        except socket.error as e:
            print(f"Lỗi kết nối: {e}")

    def login(self):
        # Gửi gói đăng nhập
        packet_id = 0x00  # Gói đăng nhập
        data = json.dumps({"name": self.username})
        self.send_packet(packet_id, data)

    def send_packet(self, packet_id, data):
        # Gửi gói tin đến server
        data_encoded = data.encode('utf-8')
        length = struct.pack('>H', len(data_encoded))
        self.socket.sendall(length + struct.pack('B', packet_id) + data_encoded)

    def listen(self):
        while True:
            try:
                # Lắng nghe phản hồi từ server
                response_length = self.socket.recv(2)
                if not response_length:
                    print("Server đã ngắt kết nối.")
                    break
                
                length = struct.unpack('>H', response_length)[0]
                response = self.socket.recv(length).decode('utf-8')
                print("Nhận:", response)
            except Exception as e:
                print(f"Lỗi khi lắng nghe: {e}")
                break

    def close(self):
        if self.socket:
            self.socket.close()
            print("Bot đã ngắt kết nối!")

if __name__ == "__main__":
    host = "localhost"  # Địa chỉ IP của server Minecraft
    port = 25565        # Cổng của server
    username = "BotName" # Tên bot

    bot = MinecraftBot(host, port, username)
    
    try:
        bot.connect()
    except KeyboardInterrupt:
        bot.close()
