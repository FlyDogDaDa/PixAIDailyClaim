# PixAIDailyClaim

This script automates the process of claiming daily rewards on the PixAI.art platform. It simulates requests to the platform's API and can send notifications to Discord via a webhook when rewards are successfully claimed or if errors occur.

## Features

- **Automated Daily Claiming:** Automatically attempts to claim your daily PixAI rewards.
- **Discord Notifications:** Sends messages to a specified Discord channel when a claim is successful or fails.
- **Error Logging:** Logs any errors encountered during the claim process to text files in the `error_log` directory.
- **Multiple Accounts:** Supports configuring multiple PixAI accounts in the same configuration file.

## Prerequisites

- **Python 3.7+**
- **Packages:**
  - `requests`
  - `datetime`
  - `jsons`

You can install the necessary packages using pip:

```bash
pip install requests jsons
```

Or, simply install using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Setup and Configuration

### 1. Obtain Your PixAI Authorization Token

1. Log in to your PixAI.art account in your web browser.
2. Open your browser's developer tools (usually by pressing F12).
3. Go to the "Network" tab.
4. Refresh the PixAI.art page.
5. Find a request to `https://api.pixai.art/graphql` in the network requests. It's often one of the first ones to appear. (Searching for "graphql" can quickly find)
6. Look at the request headers. There should be an `authorization` header.
7. Copy the value associated with it. The token should start with `Bearer` followed by a long string of letters and numbers.
   - Example: `Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9...`

### 2. Set Up a Discord Webhook

1. Go to your Discord server settings.
2. Navigate to "Integrations" and then click on "Webhooks".
3. Click "New Webhook".
4. Choose the channel where you want notifications to be sent.
5. Copy the "Webhook URL".
   - Example: `https://discord.com/api/webhooks/123456789012345678/aBcDeFgHiJkLmNoPqRsTuVwXyZ`

### 3. Configure the `config.json` File

1. Create a file named `config.json` in the same directory as `Main.py`. (or rename `config.json.example` and modify it)
2. Open `config.json` with a text editor and populate it with the following structure.

```json
{
  "accounts": [
    {
      "webhook": "YOUR_DISCORD_WEBHOOK_URL",
      "authorization": "YOUR_PIXAI_AUTHORIZATION_TOKEN"
    }
  ]
  // Other configs ...
}
```

- **`accounts`** : This is a list that can contain multiple PixAI accounts. Each account is represented by a JSON object.
- **`webhook`** : Replace `YOUR_DISCORD_WEBHOOK_URL` with the Discord webhook URL you copied in step 2.
- **`authorization`** : Replace `YOUR_PIXAI_AUTHORIZATION_TOKEN` with the PixAI authorization token you copied in step 1.
- **`graphql`** : This should be kept as `"https://api.pixai.art/graphql"`. It's the URL of the PixAI GraphQL API.
- **`headers`** : These are the request headers. These are commonly used headers, and are generally acceptable to keep as they are.
- These headers tell the server who is making a request, from what browser, etc.

### 4. Running the Script

> You can also use some scheduling provided by the system or platform to automatically execute the script at a certain time for you.

1. Navigate to the directory where you saved script in your terminal.
2. Run the script using the following command:

```bash
python Main.py
```

The script will attempt to claim the daily rewards for each account configured in `config.json`. You'll receive Discord notifications when claims are made or if there are any errors. Error will be write in the `error_log` directory.

## Multiple Accounts

To use multiple accounts, simply add more account objects to the `accounts` list in `config.json`:

```json
{
  "accounts": [
    {
      "webhook": "YOUR_DISCORD_WEBHOOK_URL_1",
      "authorization": "YOUR_PIXAI_AUTHORIZATION_TOKEN_1"
    },
    {
      "webhook": "YOUR_DISCORD_WEBHOOK_URL_2",
      "authorization": "YOUR_PIXAI_AUTHORIZATION_TOKEN_2"
    }
  ]
  // ... the rest
}
```

## Error Handling

The script logs errors to text files in the `error_log` directory. Each error file is named with a timestamp, making it easy to see when each error occurred.

## Disclaimer

- This script interacts with PixAI's API in a way that may not be officially supported. Use it at your own risk. Be aware that changes to the PixAI API may cause this script to stop working, and the use of automation scripts might violate PixAI's terms of service.

```plaintext
**Explanation of Changes and Improvements:**

1.  **Clearer Introduction:** The introduction now clearly states the purpose and main features of the script.
2.  **Step-by-Step Configuration:** The instructions for setting up `config.json` are broken down into smaller, more manageable steps.
3.  **Detailed Instructions:** Steps to obtain the PixAI authorization token and setting up the Discord webhook are detailed.
4.  **`config.json` Structure:** The `config.json` structure is clearly explained.
5.  **Multiple Account Support:** The instructions for configuring multiple accounts are more prominent and easier to understand.
6.  **Error Handling:** There is now a section on error handling.
7.  **Disclaimer:** Added a disclaimer about the potential risks of using automation scripts with online platforms.
8. **Installation:** Added installation instructions.
9. **Running the script** : Added running instructions.
```

- The entire `README.md` file was written with assistance from Gemini.
