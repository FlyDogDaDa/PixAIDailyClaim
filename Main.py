import json
import socket
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def build_driver(driver_path, chrome_path, user_data_dir, port):
    # 檢查 port 是否開啟
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.25)  # 設定一個短的超時時間
    try:
        s.connect(("127.0.0.1", port))
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        # 啟動瀏覽器
        cmd = f'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="{user_data_dir}"'
        subprocess.Popen(cmd)
    # 連接到瀏覽器
    service = webdriver.ChromeService(driver_path)
    options = ChromeOptions()
    options.chrome_options = {"profile.managed_default_content_settings.images": 2}
    # 關閉圖片載入
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    browser = webdriver.Chrome(service=service, options=options)
    browser.minimize_window()
    return browser


def login(driver, timeout: float):
    # 等待器
    wait = WebDriverWait(driver, timeout)
    # 等待通知按鈕載入(有登入才會有通知按鈕)
    notification_button_selector = "button[title='open notification']"
    try:
        # 登入過了
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, notification_button_selector))
        )
        return  # 早退
    except TimeoutException:
        # 沒登入
        pass  # 繼續流程
    header_section_selector = "div.sticky.top-0.z-20"
    header_section = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, header_section_selector))
    )
    # 找到登入按鈕
    login_button_selector = ".//button[.//span[text()='登入']]"
    login_button = header_section.find_element(By.XPATH, login_button_selector)
    # 點登入
    login_button.click()
    # 等google登入按鈕
    google_login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[./span[text()='Continue with Google']]")
        )
    )
    google_login_button.click()


def claim_all(driver, timeout: float):
    button_selector = (
        "div.flex-none.w-\\[155px\\].px-3.border-l.border-zinc-500\\/50 button"
    )
    reward_selector = "div.grid.gap-3.grid-cols-1.mmd\\:grid-cols-2.mlg\\:grid-cols-3"
    # 等待器
    wait = WebDriverWait(driver, timeout)
    # 等到獎勵區塊出現
    reward_section = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, reward_selector))
    )
    # 等到有三個按鈕可以按
    wait.until(
        lambda d: len(reward_section.find_elements(By.CSS_SELECTOR, button_selector))
        >= 3
    )
    # 找到所有按鈕
    buttons = reward_section.find_elements(
        By.CSS_SELECTOR,
        button_selector,
    )
    # 點所有可以點的按鈕
    for button in buttons:
        # 可以點
        if not button.get_attribute("disabled"):
            # 點他
            button.click()


def main():
    # load config
    with open("config.json", "r") as f:
        config = json.load(f)

    # C:\Users\Home\AppData\Local\Google\Chrome\User Data\Default
    # D:\\KnScriptsPackage\\PixAIDailyClaim\\Chrome_dev_session

    chrome_config = config["chrome"]
    driver = build_driver(
        chrome_config["driver_path"],
        chrome_config["chrome_path"],
        chrome_config["user_data_dir"],
        chrome_config["debug_port"],
    )
    url = "https://pixai.art/zh/@flydog-kwenen/files"
    # 只有當前網址不是目標網址時才前往
    if driver.current_url != url:
        print("網頁跳轉中...", end="")
        driver.get(url)  # 前往 PixAI
        print("結束!")
    try:
        print("帳號登入中...", end="")
        login(driver, 4)  # 登入
        print("登入結束!")
    except TimeoutException:
        print("登入失敗，請你先登入Google帳號，謝謝。")
        input("登入後按Enter繼續")
        return
    print("獎勵挖掘中...", end="")
    claim_all(driver, 3)
    print("結束!")
    driver.close()
    driver.quit()


if __name__ == "__main__":
    main()
