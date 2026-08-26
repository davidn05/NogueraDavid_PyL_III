from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
import json

# "Base de datos" en memoria
productos = [
    {"id": 1, "nombre": "Fernet con Coca", "precio": 3500},
    {"id": 2, "nombre": "Cerveza Artesanal IPA", "precio": 4200},
]


class ManejadorHTTP(BaseHTTPRequestHandler):

    def _enviar_json(self, codigo, data):
        cuerpo = json.dumps(data).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path == "/api/v1/health":
            respuesta = {
                "status": "online",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self._enviar_json(200, respuesta)

        elif self.path == "/api/v1/productos":
            self._enviar_json(200, productos)

        else:
            self._enviar_json(404, {"error": "Recurso no encontrado"})

    def do_POST(self):
        if self.path == "/api/v1/productos":
            largo = int(self.headers.get("Content-Length", 0))
            cuerpo_crudo = self.rfile.read(largo)

            try:
                nuevo_producto = json.loads(cuerpo_crudo)
            except json.JSONDecodeError:
                self._enviar_json(400, {"error": "JSON inválido"})
                return

            if "nombre" in nuevo_producto and "precio" in nuevo_producto:
                nuevo_producto["id"] = len(productos) + 1
                productos.append(nuevo_producto)
                self._enviar_json(201, nuevo_producto)
            else:
                self._enviar_json(400, {"error": "Faltan campos: nombre y precio son requeridos"})

        else:
            self._enviar_json(404, {"error": "Recurso no encontrado"})


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8080), ManejadorHTTP)
    print("Servidor corriendo en http://localhost:8080")
    servidor.serve_forever()