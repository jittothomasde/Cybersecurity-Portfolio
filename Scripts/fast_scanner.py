import socket
import threading
from queue import Queue
import sys
from datetime import datetime
import time

# ====================================================================
# CONFIGURATION
# ====================================================================
print_lock = threading.Lock()
MAX_THREADS = 100 
TIMEOUT = 0.5
# ====================================================================

# Function to check a single port
def portscan(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        # connect_ex returns 0 if the connection succeeds
        result = s.connect_ex((target, port))
        if result == 0:
            with print_lock:
                print(f"[+] TCP Port {port} is OPEN")
        s.close()
    except Exception:
        s.close()

# The worker function that each thread will execute
def threader(target, q):
    while True:
        worker_port = q.get()
        portscan(target, worker_port)
        q.task_done()

# Main function to initialize the scan
def run_scanner():
    if len(sys.argv) < 2:
        print("Usage: python3 fast_scanner.py <target_ip> <port_start> <port_end>")
        print("Example: python3 fast_scanner.py 192.168.56.101 1 1000")
        sys.exit(1)

    target_ip = sys.argv[1]
    # Default to scanning ports 1-1024 if range is not specified
    try:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    except:
        start_port = 1
        end_port = 1024
        print(f"[-] Invalid port range. Scanning ports {start_port} to {end_port} by default.")

    print("-" * 60)
    print(f"Scanning Target: {target_ip}")
    print(f"Ports: {start_port} to {end_port}")
    print(f"Scan started at: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)

    # 1. Create the Queue
    q = Queue()

    # 2. Create and start the Thread pool
    for x in range(MAX_THREADS):
        t = threading.Thread(target=threader, args=(target_ip, q))
        t.daemon = True
        t.start()

    # 3. Fill the Queue with all ports to scan
    for port in range(start_port, end_port + 1):
        q.put(port)

    # 4. Wait for all jobs in the queue to finish
    q.join()

    print("-" * 60)
    print("Scan completed.")
    print("-" * 60)

if __name__ == "__main__":
    run_scanner()