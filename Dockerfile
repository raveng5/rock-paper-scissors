FROM debian:bookworm-slim

# Python 3.11 and Tkinter come from the same Debian repository.
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-tk xvfb x11vnc novnc python3-websockify \
    x11-utils fonts-dejavu-core tini \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 player

WORKDIR /app
COPY game.py start.sh healthcheck.py ./
RUN chmod +x /app/start.sh
ENV DISPLAY=:99 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
USER player
EXPOSE 6080
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python3", "/app/healthcheck.py"]
ENTRYPOINT ["/usr/bin/tini", "--", "/app/start.sh"]
