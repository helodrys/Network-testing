import socket
import threading
import time

# Target server
TARGET_IP = "127.0.0.1"  # change to server IP if testing on LAN
TARGET_PORT = 9999

# Load test configuration
USERS = 5
PACKETS_PER_USER = 50
INITIAL_SIZE = 100
SIZE_INCREMENT = 50
DELAY = 0.05  
WARNING_THRESHOLD = 20 

# Shared stats
stats = {
    "total": 0,
    "last_total": 0,
    "user_packet_sizes": [INITIAL_SIZE] * USERS
}
lock = threading.Lock()
done = False

def udp_user(user_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_size = INITIAL_SIZE
    for i in range(PACKETS_PER_USER):
        try:
            data = b"x" * packet_size
            sock.sendto(data, (TARGET_IP, TARGET_PORT))
            with lock:
                stats["total"] += 1
                stats["user_packet_sizes"][user_id] = packet_size
            print(f"[User {user_id}] Packet {i+1}, size {packet_size} bytes sent")
        except Exception as e:
            print(f"[User {user_id}] Error: {e}")
        packet_size += SIZE_INCREMENT
        time.sleep(DELAY)

def monitor():
    """Advanced monitor for packets/sec and packet size."""
    while not done:
        time.sleep(1)
        with lock:
            current_total = stats["total"]
            packets_sec = current_total - stats["last_total"]
            stats["last_total"] = current_total

            # Display info
            print(f"\n[MONITOR] Total packets: {current_total}, Packets/sec: {packets_sec}")
            for uid, size in enumerate(stats["user_packet_sizes"]):
                print(f"  User {uid} current packet size: {size} bytes")

            # Warning if sending too fast (simulated "server stress")
            if packets_sec > WARNING_THRESHOLD:
                print("⚠️ Warning: Sending rate high — server may start acting wild!\n")

# Start monitor thread
monitor_thread = threading.Thread(target=monitor, daemon=True)
monitor_thread.start()

# Start user threads
threads = []
for u in range(USERS):
    t = threading.Thread(target=udp_user, args=(u,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

done = True
time.sleep(1)
print("UDP load test completed safely ✅")
print(f"Final total packets sent: {stats['total']}")
