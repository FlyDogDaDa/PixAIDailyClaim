import requests
import json


class WebHook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, message):
        # 資料與標頭
        headers = {"Content-Type": "application/json"}
        data = {"content": message}
        # 發送請求
        response = requests.post(
            self.webhook_url, data=json.dumps(data), headers=headers
        )
        # 若有請求錯誤
        response.raise_for_status()


def main():
    url = "https://discord.com/api/webhooks/1363019151366553600/3fL3fxDzR9QOe2mR-T9v5luQkNrKD0Phf1td7kaG0GG1tf-ooMLkWX7d7zUj_6SFYY3U"
    webhook = WebHook(url)
    webhook.send_message("Hello World!")


if __name__ == "__main__":
    main()
