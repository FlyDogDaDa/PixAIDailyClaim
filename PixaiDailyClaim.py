import requests


class Pixai:
    def __init__(self, graphql_url: str, authorization: str, headers: str):
        self.graphql_url = graphql_url
        self.headers = dict(**headers, authorization=authorization)

    def check_daily(self) -> bool:
        """
        檢查PixAI是否有每日獎勵可以領取。

        Returns:
            bool: 是否成功領取獎勵。
        """
        # graphql query
        data = {
            "query": """
            query getDailyClaimAvailable {
              me {
                dailyClaimAvailable
                dailyClaimAmount
              }
            }
        """,
            "variables": {},
        }
        # 發送請求
        response = requests.post(self.graphql_url, headers=self.headers, json=data)
        # 若請求發起錯誤
        response.raise_for_status()
        # 回傳是否可領
        return response.json()["data"]["me"]["dailyClaimAvailable"]

    def claim_daily(self) -> None:
        """
        嘗試領取PixAI每日獎勵。
        """
        # graphql query
        data = {"query": """mutation dailyClaimQuota { dailyClaimQuota }"""}
        # 發送請求
        requests.post(self.graphql_url, headers=self.headers, json=data)
