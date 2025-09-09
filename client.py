import socket
import pickle

HEADER = 64 
PORT = 5050
FORMAT = " utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "169.254.92.141" # ใส่ ip address ของ client
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4 TCP
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT) #แปลงข้อความเป็น byte
    msg_length = len(message) #หาขนาดของข้อความ
    send_length = str(msg_length).encode(FORMAT) #แปลงขนาดของข้อความเป็น byte ให้รู้ขนาดของ message ทั้งหทด (อยู่ใน header)
    send_length += b' ' * (HEADER - len(send_length)) #เติม byte ให้ครบ 64 byte
    client.send(send_length) #ส่งขนาดของข้อความไปก่อน
    client.send(message) #ส่งข้อความจริงไป
    print(client.recv(2048).decode(FORMAT)) #รอรับข้อความตอบกลับจาก server

send("Hello WOrld!")
input()
send("Hello Everyone!")
input()
send("Hello User!")

send(DISCONNECT_MESSAGE)