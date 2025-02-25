import socket
import threading
import argparse

# Colors for better visibility
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Function to grab banner
def grab_banner(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)  # Set timeout
            s.connect((target, port))
            s.send(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            banner = s.recv(1024).decode(errors='ignore').strip()
            print(f"{GREEN}[+] Port {port} - {banner}{RESET}")

            # Save results
            with open("banners.txt", "a") as f:
                f.write(f"{target}:{port} - {banner}\n")

    except socket.timeout:
        print(f"{YELLOW}[!] Port {port} - Timed out{RESET}")
    except Exception:
        print(f"{RED}[-] Port {port} - Connection failed{RESET}")

# Function to scan for open ports and grab banners
def scan_target(target, ports):
    threads = []
    for port in ports:
        t = threading.Thread(target=grab_banner, args=(target, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# Function to auto-detect open ports
def detect_open_ports(target, port_range):
    print(f"{YELLOW}[*] Scanning {target} for open ports...{RESET}")
    open_ports = []
    for port in port_range:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((target, port)) == 0:
                    open_ports.append(port)
                    print(f"{GREEN}[+] Port {port} is open{RESET}")
        except:
            continue
    return open_ports

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Banner Grabber Tool")
    parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
    parser.add_argument("-p", "--ports", help="Comma-separated list of ports (e.g., 22,80,443) or 'auto' for auto-scan")
    args = parser.parse_args()

    if args.ports == "auto":
        port_list = detect_open_ports(args.target, range(1, 10000))
    else:
        port_list = [int(p) for p in args.ports.split(",")]

    if port_list:
        scan_target(args.target, port_list)
    else:
        print(f"{RED}[!] No open ports detected.{RESET}")
