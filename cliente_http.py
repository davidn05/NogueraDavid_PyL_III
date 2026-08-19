import requests  # Librería para realizar peticiones HTTP

URL_BASE = "https://jsonplaceholder.typicode.com/posts"

# 1. Petición GET - obtener lista de datos
respuesta_get = requests.get(URL_BASE)

# 2. Status Code y Headers de la respuesta
print("=== GET ===")
print("Status Code:", respuesta_get.status_code)
print("Content-Type:", respuesta_get.headers["Content-Type"])

# 3. Petición POST - enviar un objeto JSON en el body
nuevo_post = {
    "title": "Aprendiendo REST con Python",
    "body": "Post creado mediante una petición POST.",
    "userId": 1
}

respuesta_post = requests.post(URL_BASE, json=nuevo_post)

print("\n=== POST ===")
print("Status Code:", respuesta_post.status_code)
print("Content-Type:", respuesta_post.headers["Content-Type"])

# Validar que el recurso fue creado (201 Created)
if respuesta_post.status_code == 201:
    print("Recurso creado correctamente.")
    print("Respuesta del servidor:", respuesta_post.json())
else:
    print("No se pudo crear el recurso.")

