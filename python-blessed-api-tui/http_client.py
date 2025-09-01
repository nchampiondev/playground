# http_client.py
import requests

class HttpClient:
    def get(self, url: str, params: dict = None):
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
