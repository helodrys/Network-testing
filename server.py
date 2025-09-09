import socket
import threading #สามารถ run code พร้อมกันได้ โดยไม่ต้องรอจากบนลงล่าง
import time

HEADER = 64 
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # หรือจะ static ip address ก็ได้ -> private ip ของเรา
ADDR = (SERVER, PORT) 
FORMAT = " utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

print(socket.gethostname()) # DESKTOP-XXXXXXX ชื่อเตรื่อง
print(SERVER) # 172.22.128.1

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4 TCP ใช้เชื่อมต่อระหว่าง 2 device  หรือ 2 โปรเเกรม
server.bind(ADDR) #ผูก socket กับ ip address

# ตอนนี้ server รับการเชื่อมต่อได้ผ่าน socket



def handle_client(connect, address): # run  เเยกในเเต่ละ client
    print(f"[*] New connection {address} connected.")

    connected = True
    while connected:
        msg_length = connect.recv(HEADER).decode(FORMAT) #รอรับข้อมูล HEADER จาก client ที่จะบอกว่า request มีขนาดเท่าไหร ปกติ 64 byte
        # ต้อง decode เพราะข้อมูลที่รับมาเป็น byte เป็น utf -8
        if msg_length: #เมื่อเชื่อมต่อกันตอนเเรกจะ ได้ข้อมูลเปล่าดังนั้นรอให้มีข้อมูลก่อน
            msg_length = int(msg_length)
            msg = connect.recv(msg_length).decode(FORMAT) #รอรับข้อมูลจริงจาก client request
            if msg == DISCONNECT_MESSAGE: #ถ้า client ส่งข้อความ !DISCONNECT มา ก็จะตัดการเชื่อมต่อ
                connected = False

            print(f"[*] {address} says: {msg}")
            connect.send("Msg received".encode(FORMAT)) #ส่งข้อความตอบกลับไปหา client
    connect.close() #ปิดการเชื่อมต่อ

def start(): 
    server.listen() #รอการเชื่อมต่อ
    print(f"[*] Server is listening on {SERVER}")
    while True:
        connect, address = server.accept() #รอการเชื่อมต่อจาก client เมื่อได้ข้อมูลก็จะเก็บข้อมูลไว้ที่ connect, address
        #connect -> ทำให้เราคุยกับ client ได้ address -> ข้อมูล ip เเละ port ของ client
        thread = threading.Thread(target=handle_client, args=(connect, address)) #เมื่อมี client เชื่อมต่อเข้ามา ก็จะไป run handle_client function
        thread.start()
        print(f"[*] Active connections: {threading.active_count() - 1}") # -1 เพราะ thread ที่ run start function ก็จะถูกนับด้วย
print("[*] Server is starting...")
start()