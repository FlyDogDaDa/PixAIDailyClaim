import os
import json
from datetime import datetime

from DiscordWebHook import WebHook
from PixaiDailyClaim import Pixai

ERROR_LOG_PATH = "error_log"


def claim(pixai: Pixai, webhook: WebHook):
    # 1. 檢查是否可領取獎勵
    if not pixai.check_daily():
        print("No daily reward available today.")
        return
    # 2. 嘗試領取獎勵
    pixai.claim_daily()
    # 3. 檢查獎勵是否沒了
    if pixai.check_daily():
        webhook.send_message(
            "Claiming daily reward appears to have failed.  Reward is still available."
        )


def main() -> None:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    assert isinstance(config, dict), "config.json is not a valid JSON object"
    # 取出要領取的參數
    accounts: list[dict[str, str]] = config.get("accounts", [])
    graphql_url = config["graphql"]
    headers = config["headers"]
    #
    for account in accounts:
        authorization = account["authorization"]
        pixai = Pixai(graphql_url, authorization, headers)
        webhook = WebHook(account["webhook"])
        # 開始領取
        try:
            claim(pixai, webhook)
        except Exception as e:
            webhook.send_message(f"Error claiming daily reward: \n{repr(e)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        os.makedirs("error_log", exist_ok=True)
        time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(ERROR_LOG_PATH, time_str + ".txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(repr(e))
