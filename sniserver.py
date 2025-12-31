#!/usr/bin/env python3
# multi_cert_tls_server.py

import ssl
import socket
import threading
import os

# Status symbols
OK = "[OK]"
WARN = "[WARN]"
ERROR = "[ERROR]"
INFO = "[INFO]"

# Certificate mapping with types
CERT_MAP = {
    'valid.example.com': ('server/valid-chain.pem', 'server/serverkey.pem', 'VALID'),
    'expired.example.com': ('server/expired-chain.pem', 'server/serverkey.pem', 'EXPIRED'),
    'revoked.example.com': ('server/revoked-chain.pem', 'server/serverkey.pem', 'REVOKED'),
    'selfsigned.example.com': ('server/selfsigned-chain.pem', 'server/selfsignedkey.pem', 'SELF-SIGNED'),
}

def sni_callback(ssl_socket, server_name, ssl_context):
    """SNI callback: Return the appropriate certificate based on the client's requested domain"""
    print(f"{INFO} Client requested: {server_name}")

    if server_name in CERT_MAP:
        cert_file, key_file, cert_type = CERT_MAP[server_name]
        try:
            # Create a new SSL context
            new_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            new_context.load_cert_chain(cert_file, key_file)
            ssl_socket.context = new_context
            print(f"{OK} Loaded certificate [{cert_type}]")
        except FileNotFoundError as e:
            print(f"{ERROR} Certificate file not found [{cert_type}]: {cert_file} or {key_file}")
            print(f"        Error details: {e}")
            print(f"        Using default certificate instead")
        except Exception as e:
            print(f"{ERROR} Failed to load certificate [{cert_type}]: {e}")
            print(f"        Using default certificate instead")
    else:
        print(f"{WARN} Unknown server name: {server_name}, using default")

def handle_client(conn, addr):
    """Handle client connection"""
    print()
    print(f"{INFO} Connection from {addr}")
    try:
        data = conn.recv(1024)
        if data:
            conn.sendall(b"TLS Server: Connection successful!\n")
    except Exception as e:
        print(f"{ERROR} {e}")
    finally:
        conn.close()
def main():
    # Validate certificate files on startup
    print("=" * 60)
    print("Validating certificate files...")
    print("-" * 60)
    for domain, (cert_file, key_file, cert_type) in CERT_MAP.items():
        if os.path.exists(cert_file) and os.path.exists(key_file):
            print(f"{OK} [{cert_type}] {domain}")
            print(f"     Cert: {cert_file}")
            print(f"     Key:  {key_file}")
        else:
            if not os.path.exists(cert_file):
                print(f"{WARN} [{cert_type}] {domain}: Certificate file not found")
                print(f"       Missing: {cert_file}")
            if not os.path.exists(key_file):
                print(f"{WARN} [{cert_type}] {domain}: Key file not found")
                print(f"       Missing: {key_file}")
    print("=" * 60)
    print()

    # Default SSL context (using valid certificate)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        context.load_cert_chain('server/valid-chain.pem', 'server/serverkey.pem')
    except FileNotFoundError as e:
        print(f"{ERROR} Default certificate files not found!")
        print(f"        Please ensure server/valid-chain.pem and server/serverkey.pem exist.")
        print(f"        Error: {e}")
        return

    context.sni_callback = sni_callback  # Register SNI callback

    # Create server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 4443))
        sock.listen(10)
        print("=" * 60)
        print("Multi-certificate TLS server listening on port 4443")
        print("=" * 60)
        print("Available certificates:")
        for domain, (cert_file, key_file, cert_type) in CERT_MAP.items():
            print(f"  - [{cert_type:12s}] {domain}")
        print("=" * 60)
        print()

        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                try:
                    conn, addr = ssock.accept()
                    # Handle each connection in a separate thread (supports concurrent connections)
                    client_thread = threading.Thread(
                        target=handle_client,
                        args=(conn, addr)
                    )
                    client_thread.start()
                except ssl.SSLError as e:
                    print(f"{ERROR} SSL Error: {e}")
                except KeyboardInterrupt:
                    print(f"\n{INFO} Server shutting down...")
                    break

if __name__ == '__main__':
    main()

