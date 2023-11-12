import socket
import subprocess
import re

def es_direccion_ip(entrada):
    # Utiliza una expresión regular para verificar si la entrada es una dirección IP válida
    patron_ip = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    return bool(patron_ip.match(entrada))

def obtener_informacion_servidor(target, guardar_resultados=False):
    try:
        if es_direccion_ip(target):
            ip = target
        else:
            # Obtener información de la dirección IP del host
            ip = socket.gethostbyname(target)

        # Obtener información sobre el servidor
        servidor_info = socket.gethostbyaddr(ip)

        print(f'Información del servidor para {target} ({ip}):')
        print(f'Nombre del host: {servidor_info[0]}')
        print(f'Alias del host: {servidor_info[1]}')
        print(f'IPs asociadas: {servidor_info[2]}')

        # Realizar escaneo de puertos con Nmap
        print('\nEscaneo de puertos con Nmap:')
        nmap_comando = f'nmap -p- {ip}'
        resultado_nmap = subprocess.run(nmap_comando, shell=True, capture_output=True, text=True)
        print(resultado_nmap.stdout)

        # Guardar resultados en un archivo
        if guardar_resultados:
            with open("resultado_nmap.txt", "w") as archivo:
                archivo.write(f'Información del servidor para {target} ({ip}):\n')
                archivo.write(f'Nombre del host: {servidor_info[0]}\n')
                archivo.write(f'Alias del host: {servidor_info[1]}\n')
                archivo.write(f'IPs asociadas: {servidor_info[2]}\n\n')
                archivo.write('Escaneo de puertos con Nmap:\n')
                archivo.write(resultado_nmap.stdout)

    except socket.error as e:
        print(f'Error al obtener información del servidor: {e}')

if __name__ == "__main__":
    entrada = input("Ingresa la URL, dominio o dirección IP: ")
    guardar_resultados = input("¿Quieres guardar los resultados en un archivo? (si/no): ").lower() == 'si'

    obtener_informacion_servidor(entrada, guardar_resultados)
