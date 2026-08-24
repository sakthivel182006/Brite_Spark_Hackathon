import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from app.resident_adapter import get_all_residents
from app.benefits_adapter import get_all_benefits
from app.aggregator import build_unified_view


HOST = "127.0.0.1"
PORT = 8080


class UnifiedAPIHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        response = json.dumps(data, indent=2).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        path = urlparse(self.path).path

        if path == "/health":
            self.send_json(
                200,
                {
                    "status": "ok",
                    "service": "unified-api"
                }
            )
            return

        if path == "/unified":

            # -------------------------------------------------
            # 1. Get Resident Index independently
            # -------------------------------------------------
            residents = []
            resident_available = True
            resident_error = None

            try:
                residents = get_all_residents()

            except Exception as error:
                resident_available = False
                resident_error = str(error)

            # -------------------------------------------------
            # 2. Get Benefits Register independently
            # -------------------------------------------------
            try:
                benefits = get_all_benefits()

            except Exception as error:
                benefits = {
                    "available": False,
                    "records": [],
                    "error": str(error)
                }

            # -------------------------------------------------
            # 3. Aggregate both results
            # -------------------------------------------------
            unified_view = build_unified_view(
                residents=residents,
                benefits_result=benefits,
                resident_available=resident_available,
                resident_error=resident_error
            )

            self.send_json(200, unified_view)
            return

        self.send_json(
            404,
            {
                "status": "error",
                "message": "Endpoint not found"
            }
        )

    def log_message(self, format, *args):
        print(f"[Unified API] {format % args}")


def start_server():

    server = ThreadingHTTPServer(
        (HOST, PORT),
        UnifiedAPIHandler
    )

    print(
        f"Unified API running on "
        f"http://{HOST}:{PORT}"
    )

    print("Endpoints:")
    print("  GET /health")
    print("  GET /unified")

    server.serve_forever()


if __name__ == "__main__":
    start_server()