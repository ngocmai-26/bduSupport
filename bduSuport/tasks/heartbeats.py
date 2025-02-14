import logging
import requests

def send_heartbeat(heartbeat_id: str, failed=False):
    try:
        failed_path = "/fail" if failed else ""
        heartbeat_url = f"https://uptime.betterstack.com/api/v1/heartbeat/{heartbeat_id}{failed_path}"
        resp = requests.get(heartbeat_url)
        logging.getLogger().info(f"{resp.status_code}, {heartbeat_url}")
    except Exception as e:
        logging.getLogger().exception("send_heartbeat exc=%s", str(e))