"""Check browser endpoint, VNC handshake, and virtual display."""
import socket
import subprocess
import urllib.request

with urllib.request.urlopen("http://127.0.0.1:6080/vnc.html", timeout=2) as response:
    assert response.status == 200
with socket.create_connection(("127.0.0.1", 5900), timeout=2) as connection:
    assert connection.recv(12).startswith(b"RFB ")
subprocess.run(["xdpyinfo"], check=True, stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL, timeout=2)
