from __future__ import annotations
from dataclasses import dataclass
DEFAULT_PORT = 7000

@dataclass
class Packet:
    ip: str
    port: int
    ttl: int
    msg: bytes

#Lo que guarda el cache es
# key: la
cache = dict()

def get_address(packet: Packet) -> tuple[str,int]:
    return (packet.ip, packet.port)

def parse_packet(msg: bytes):
    ip, port, ttl, msg = msg.split(b";")
    ip = ip.decode()
    ttl = int(ttl)
    port = int(port)
    return Packet(ip, port, ttl,  msg)


def create_packet(packet: Packet):
    l = [packet.ip.encode(), str(packet.port).encode(), str(packet.ttl).encode(), packet.msg]
    return b";".join(l)


def check_routes(routes_file_name: str, dest_addr: tuple[str,int], is_default_router=False) -> tuple[str,int] | None :
    global cache
    dest_ip, dest_port = dest_addr
    #si la direccion de cache no esta en el destino
    if cache.get(dest_addr) == None:
        #la inicializamos; donde la llave es la direccion de destino
        cache[dest_addr] = 0
    with open(routes_file_name, "r") as f:
        lines = f.readlines()
        
        #funcion para filtar las lineas
        def filter_lines(line):
            network_ip, puerto_inicial, puerto_final, ip_para_llegar, puerto_para_llegar = line.split(" ")
            
            puerto_inicial = int(puerto_inicial)
            puerto_final = int(puerto_final)
            return dest_port in range(puerto_inicial, puerto_final+1) and \
                puerto_final != DEFAULT_PORT
        
        #obtenemos los posibles puertos destinos
        lines_filtered = list(filter(filter_lines, lines))

        # Si es posible llegar a ellos
        if len(lines_filtered) != 0:
            print(cache)

            #vemos que para llegar, tomo la llave, obtengo la linea donde estoy actualmente y obtengo la ip 
            # y el puerto para llegar
            _,_,_, ip_para_llegar, puerto_para_llegar = lines_filtered[cache[dest_addr]%len(lines_filtered)].split(" ")

            # le sumo 1 al cache
            cache[dest_addr] +=1

            #retorno la direccion
            return ip_para_llegar, int(puerto_para_llegar)
        
        
        
        # si no, soy el default y no encontre nada y por lo tanto tiro none
        return None