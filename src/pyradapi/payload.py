import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Payload:
    def __init__(self, url: str, payload: str) -> None:
        self.payload = payload
        self.url = url

    def __repr__(self) -> str:
        return f"url:\t\t{self.url} \npayload:\t{json.dumps(self.payload)}"


# standard posting payload
def post_payload(url: str, payload: dict = dict()):
    try:
        http = urllib3.PoolManager()
        resp = http.request(
            method="POST",
            url=url,
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload),
        )
        return json.loads(resp.data.decode("utf-8"))
    except:
        return resp.data.decode("utf-8", errors="ignore")


def post_payload_object(payloadObj: Payload):
    return post_payload(url=payloadObj.url, payload=payloadObj.payload)
