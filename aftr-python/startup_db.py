#!/usr/bin/env python3
import socket
import sys
import time
import os

def wait_for_service(host, port, timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"✅ Connected to {host}:{port}")
                return
        except Exception:
            if time.time() - start_time > timeout:
                print(f"❌ Timeout: Could not connect to {host}:{port} after {timeout} seconds")
                sys.exit(1)
            print(f"⏳ Waiting for {host}:{port}...")
            time.sleep(1)

if __name__ == "__main__":
    services = [
        ("db", 5432),
        ("redis", 6379),
    ]
    for host, port in services:
        wait_for_service(host, port)

    # Start actual command if passed
    if len(sys.argv) > 1:
        print(f"🚀 Starting: {' '.join(sys.argv[1:])}")
        os.execvp(sys.argv[1], sys.argv[1:])