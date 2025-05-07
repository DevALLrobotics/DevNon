import socket

# Target IP
target_ip = "35.213.174.146"

# Common ports to scan (you can expand this list or use range)
ports_to_scan = [22, 80, 443, 3306, 5432, 8080, 5000, 8000]

print(f"Scanning {target_ip} for open ports...")

for port in ports_to_scan:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Timeout of 1 second
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"✅ Port {port} is OPEN")
        else:
            print(f"❌ Port {port} is CLOSED or FILTERED")
