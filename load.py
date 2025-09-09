import requests
import threading
import time
import random

URL = "http://127.0.0.1:5000/api/data"
USERS = 5
REQUESTS_PER_USER = 50

stats = {"total": 0, "success": 0, "error": 0}
lock = threading.Lock()
done = False

def simulate_user(user_id):
    session = requests.Session()  # persistent connection
    packet_size = 100  # start small
    for i in range(REQUESTS_PER_USER):
        try:
            payload = {"data": "x" * packet_size}  # bigger payload each time
            r = session.get(URL, params=payload, timeout=5)
            with lock:
                stats["total"] += 1
                if r.status_code == 200:
                    stats["success"] += 1
                else:
                    stats["error"] += 1
            print(f"User {user_id} request {i} -> {r.status_code} | packet {packet_size}")
        except Exception as e:
            with lock:
                stats["total"] += 1
                stats["error"] += 1
            print(f"User {user_id} error: {e}")
        
        #time.sleep(random.uniform(0.1, 0.5))  # human-like delay
        packet_size += 50  # gradually increase payload size

def monitor():
    while not done:
        with lock:
            print(f"[MONITOR] Total: {stats['total']}, Success: {stats['success']}, Error: {stats['error']}")
        time.sleep(1)

# start monitor
monitor_thread = threading.Thread(target=monitor, daemon=True)
monitor_thread.start()

threads = []
for u in range(USERS):
    t = threading.Thread(target=simulate_user, args=(u,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

done = True
time.sleep(1)
print("Test completed safely ✅")
print(stats)
