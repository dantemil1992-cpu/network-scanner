import socket

# Lista de objetivos (IP, Puerto, Protocolo)
targets = [
    {"ip": "8.8.8.8", "port": 53, "proto": "UDP"},
    {"ip": "1.1.1.1", "port": 53, "proto": "UDP"},
    {"ip": "8.8.8.8", "port": 80, "proto": "TCP"},
    {"ip": "10.255.255.1", "port": 80, "proto": "TCP"} # IP remota inalcanzable para probar timeout
]

resultados = {}

for target in targets:
    ip = target["ip"]
    port = target["port"]
    proto = target["proto"]
    key = f"{ip}:{port}/{proto}"
    
    print(f"[+] Escaneando {key}...")
    
    if proto == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2.0)
        try:
            # Petición DNS mínima
            sock.sendto(b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00', (ip, port))
            data, _ = sock.recvfrom(512)
            # Guardamos la longitud de los bytes recibidos
            resultados[key] = f"ABIERTO (Respuesta de {len(data)} bytes)"
        except socket.timeout:
            resultados[key] = "FILTRADO / TIMEOUT"
        except Exception as e:
            resultados[key] = f"ERROR: {type(e).__name__}"
        finally:
            sock.close()
            
    elif proto == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        res = sock.connect_ex((ip, port))
        if res == 0:
            resultados[key] = "ABIERTO"
        else:
            resultados[key] = f"CERRADO (Código {res})"
        sock.close()

# Reporte final formateado
print("\n--- RESUMEN DEL ESCANEO ---")
for objetivo, estado in resultados.items():
    print(f"[{objetivo}] -> {estado}")
