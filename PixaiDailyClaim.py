import requests
import json

_version_date = "2025_04_08-10:31"


def claim_daily_reward(authorization_token):
    """
    嘗試領取PixAI每日獎勵。

    Args:
        authorization_token: 用戶的授權令牌。

    Returns:
        一個字典，包含請求是否成功的信息。  不指示是否實際領取了獎勵。
        {'success': True/False, 'message': '...', 'error': '...'}
    """

    url = "https://api.pixai.art/graphql"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://pixai.art",
        "priority": "u=1, i",
        "referer": "https://pixai.art/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "x-browser-id": "dff0ac0cf4998ee5165aaf728ad132f4",  # *重要*: 驗證這個值是否會變動!
        "authorization": f"Bearer {authorization_token}",
    }

    data = {
        "query": """
            mutation dailyClaimQuota {
              dailyClaimQuota
            }
        """
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()

        # 即使請求成功，我們仍然不確定是否實際領取了獎勵。
        return {
            "success": True,
            "message": "Claim request sent successfully.",
            "error": None,
            "response": json_response,
        }  # 返回原始回應以進行除錯
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": None,
            "error": f"Request failed: {e}",
            "response": None,
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "message": None,
            "error": f"JSON decode error: {e} - Response Text: {response.text if 'response' in locals() else 'No Response'}",
            "response": None,
        }
    except Exception as e:
        return {
            "success": False,
            "message": None,
            "error": f"An unexpected error occurred: {e}",
            "response": None,
        }


def check_daily_reward(authorization_token):
    """
    檢查PixAI是否有每日獎勵可以領取。
    """
    url = "https://api.pixai.art/graphql"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {authorization_token}",
        "content-type": "application/json",
        "origin": "https://pixai.art",
        "priority": "u=1, i",
        "referer": "https://pixai.art/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "x-browser-id": "dff0ac0cf4998ee5165aaf728ad132f4",  # 你需要確保這個值是否會變動。如果會變動，需要找到方法來抓取/生成這個值。
    }

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

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()

        if "data" in json_response and "me" in json_response["data"]:
            me_data = json_response["data"]["me"]
            available = me_data.get("dailyClaimAvailable", False)
            amount = me_data.get("dailyClaimAmount")
            return {"available": available, "amount": amount, "error": None}
        else:
            return {
                "available": False,
                "amount": None,
                "error": f"Unexpected response structure: {json_response}",
            }

    except requests.exceptions.RequestException as e:
        return {"available": False, "amount": None, "error": f"Request failed: {e}"}
    except json.JSONDecodeError as e:
        return {
            "available": False,
            "amount": None,
            "error": f"JSON decode error: {e} - Response Text: {response.text if 'response' in locals() else 'No Response'}",
        }
    except Exception as e:
        return {
            "available": False,
            "amount": None,
            "error": f"An unexpected error occurred: {e}",
        }


def main():
    # 填入授權Token
    my_token = "eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJsZ2EiOjE3NDQwNzY5MDcsImlhdCI6MTc0NDA3NzYxNywiZXhwIjoxNzQ0NjgyNDE3LCJpc3MiOiJwaXhhaSIsInN1YiI6IjE2NDg5MTEzMDc4NzA1NjUzMzEiLCJqdGkiOiIxODY2MTYxMTUzMzU3OTAxMTMyIn0.ALVeYHKzj7-v5XsWAWEvOkuGmgd_iQPy35-Fnm5bdWCzxFU7EpyaIyzs_cnU_beZ6Gn0tKfs-w3JLTQ0aez20dp9AMRWYRrR_yZeMtPPVVLasVrVXNs5G1AvR_K3nq593v53McOx1IVEqMWnKyL-9h2Q5U4liDi8ROtAsMpP8FCUXVQo"
    # 1. 檢查是否可領取獎勵
    result_check_before = check_daily_reward(my_token)

    if result_check_before["error"]:
        print(
            f"Error checking daily reward (before claim): {result_check_before['error']}"
        )
        return  # 提早退出，因為無法檢查

    if not result_check_before["available"]:
        print("No daily reward available today.")
        return  # 提早退出，因為沒有獎勵可領取

    print(f"You have a daily reward of {result_check_before['amount']} available!")

    # 2. 嘗試領取獎勵
    result_claim = claim_daily_reward(my_token)

    if result_claim["error"]:
        print(f"Error claiming daily reward: {result_claim['error']}")
        return  # 提早退出，因為領取請求失敗

    # 3. 再次檢查是否可領取獎勵
    result_check_after = check_daily_reward(my_token)

    if result_check_after["error"]:
        print(
            f"Error checking daily reward (after claim): {result_check_after['error']}"
        )
        return  # 提早退出，因為無法驗證

    # 4. 根據前後的檢查結果，判斷是否成功領取
    if result_check_after["available"]:
        print(
            "Claiming daily reward appears to have failed.  Reward is still available."
        )
    else:
        print("Daily reward claimed successfully!")


if __name__ == "__main__":
    main()
