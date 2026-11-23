# Run the game in Docker

The existing Tkinter game runs on a virtual display. noVNC shows it
in your browser. All browser clients share one game and its score.

## Build and run

Run from the game repository on the Docker host:

```sh
docker compose up -d --build
docker compose ps
docker compose logs --tail=50
```

On that same computer, open:
http://localhost:6080/vnc.html?autoconnect=true&resize=scale

For a remote server, run this on your own computer and keep it open:

```sh
ssh -N -o ExitOnForwardFailure=yes -L 6080:127.0.0.1:6080 USER@SERVER
```

Then open the same localhost URL in your computer's browser. If local port
6080 is occupied, use `-L 6081:127.0.0.1:6080` and browse to port 6081.

## Without Compose

```sh
docker build -t rock-paper-scissors:local .
docker run -d --name rps-game --restart unless-stopped \
  --security-opt no-new-privileges --cap-drop ALL \
  -p 127.0.0.1:6080:6080 rock-paper-scissors:local
docker logs rps-game
docker stop rps-game
```

Use either Compose or plain Docker, not both on the same port.

## Stop and update manually

```sh
docker compose down
```

After changing the code, `docker compose up -d --build` rebuilds and replaces
the container. Closing the browser does not stop the game. Replacing or
restarting the container resets the score. Automatic Git updates are not included.

## What is included

- Debian 12 (bookworm) slim base, Python 3.11, and its matching Tkinter package.
- Xvfb virtual screen, x11vnc, noVNC, and websockify.
- DejaVu fonts, display checks, and tini for process cleanup.
- A non-root player account; no host desktop access or privileged mode.

Package patch versions come from Debian at build time; they are not exact pins.
The image contains no Git repository and needs no pip installation.
`start.sh` starts the display, waits for readiness, then launches VNC, the web
gateway, and the game. When a child exits it stops the remaining services.
The health check probes HTTP, the VNC protocol, and the virtual display.
Docker restart policy handles process exits, not an unhealthy status alone.

## Remote server requirements

The host needs a compatible Linux kernel, Docker, and optionally Compose v2+.
It does not need Python, Tkinter, or a desktop. Build on the target machine
to select its native architecture. Compatibility with your old Debian server
must be checked using its OS, kernel, architecture, and Docker version.

Port 6080 binds to host loopback only; VNC port 5900 is not published.
There is no application password: access is intended for trusted local users
or an authenticated SSH tunnel. Do not change the binding to `0.0.0.0`.
Docker versions older than 28 have a documented caveat allowing same-L2-network
access to localhost-published ports. Upgrade Docker or arrange host firewall
protection before using this setup on such a server.

References:
- https://docs.docker.com/engine/network/port-publishing/
- https://github.com/novnc/noVNC
