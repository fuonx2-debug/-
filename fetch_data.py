import requests
import json
import os

API_KEY = os.environ.get("FRED_API_KEY")

series_map = {
    "us10y_bond": "DGS10",
    "jp10y_bond": "IRLTLT01JPM156N",
    "usdjpy": "DEXJPUS",
    "eurusd": "DEXUSEU"
}

out = {}
history_limit = 60

for name, sid in series_map.items():
    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={sid}&api_key={API_KEY}&file_type=json"
        f"&sort_order=desc&limit={history_limit}"
    )
    resp = requests.get(url)
    data = resp.json()
    obs_list = data["observations"]
    latest = obs_list[0]
    out[name] = {
        "latest": {"date": latest["date"], "value": latest["value"]},
        "history": [{"date": x["date"], "value": x["value"]} for x in reversed(obs_list)]
    }

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
