from flask import Flask, render_template_string, request, redirect, url_for
import shutil
import os
import subprocess
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask server configuration
FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")

# Paths
tg_portable_path = os.getenv("TG_PORTABLE_PATH")
tdata_accounts_path = os.getenv("TDATA_ACCOUNTS_PATH")
tg_symlink_path = os.getenv("TG_SYMLINK_PATH")
proxy_accounts_path = os.getenv("PROXY_ACCOUNTS_PATH")

# Telegram process configuration
telegram_command = os.getenv("TELEGRAM_COMMAND")
telegram_workdir = os.getenv("TELEGRAM_WORKDIR")

# Create Flask instance
app = Flask(__name__)

# HTML template for the web interface
html_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Telegram Account Switcher</title>
    <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600&display=swap" rel="stylesheet">
    <style>
      body {
        font-family: 'SF Pro Display', sans-serif;
        background-color: #282828;
        color: #ffffff;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        -webkit-font-smoothing: antialiased;
      }
      .container {
        background-color: #333333;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        max-width: 420px;
        text-align: center;
      }
      h2 {
        font-weight: 600;
        margin-bottom: 25px;
        color: #A2EC25;
        font-size: 24px;
      }
      select, input[type="text"] {
        width: 100%;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #444;
        margin-bottom: 20px;
        font-size: 16px;
        background-color: #444;
        color: #ffffff;
        outline: none;
        transition: border-color 0.3s;
      }
      select:focus, input[type="text"]:focus {
        border-color: #A2EC25;
      }
      button {
        background-color: #A2EC25;
        color: #282828;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        margin-bottom: 20px;
      }
      button:hover {
        background-color: #8ccf1d;
        transform: translateY(-2px);
      }
      button:active {
        transform: translateY(0);
      }
      p {
        margin-top: 20px;
        font-size: 14px;
        color: #b0b0b0;
      }
      .footer {
        margin-top: 30px;
        font-size: 14px;
        color: #b0b0b0;
      }
      .footer a {
        color: #A2EC25;
        text-decoration: none;
        transition: color 0.3s;
      }
      .footer a:hover {
        color: #8ccf1d;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h2>Telegram Account Switcher</h2>
      <form method="POST" action="/switch">
        <label for="account">Select an Account:</label>
        <select name="account" id="account">
          {% for account in accounts %}
            <option value="{{ account }}" {% if account == current_account %}selected{% endif %}>{{ account }}</option>
          {% endfor %}
        </select>
        <button type="submit">Switch Account</button>
        <label for="proxy" style="margin-top: 20px; display: block;">Proxy Settings (Optional):</label>
        <input type="text" name="proxy" id="proxy" value="{{ current_proxy }}" placeholder="http://username:password@host:port">
      </form>
      <p>{{ message }}</p>
      <div class="footer">
        <a href="https://t.me/MainMask" target="_blank">Developed by MainMask</a>
      </div>
    </div>
  </body>
</html>
'''

# HTML template for account switching success notification
success_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Success</title>
    <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600&display=swap" rel="stylesheet">
    <style>
      body {
        font-family: 'SF Pro Display', sans-serif;
        background-color: #282828;
        color: #ffffff;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        -webkit-font-smoothing: antialiased;
      }
      .container {
        background-color: #333333;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        max-width: 420px;
        text-align: center;
      }
      h2 {
        font-weight: 600;
        margin-bottom: 25px;
        color: #A2EC25;
        font-size: 18px;
      }
      button {
        background-color: #A2EC25;
        color: #282828;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        margin-top: 20px;
      }
      button:hover {
        background-color: #8ccf1d;
        transform: translateY(-2px);
      }
      button:active {
        transform: translateY(0);
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h2>{{ message }}</h2>
      <form method="GET" action="/">
        <input type="hidden" name="current_account" value="{{ current_account }}">
        <button type="submit">OK</button>
      </form>
    </div>
  </body>
</html>
'''

# Function to get the list of tdata accounts
def get_tdata_accounts():
    accounts = [f for f in os.listdir(tdata_accounts_path) if os.path.isdir(os.path.join(tdata_accounts_path, f)) and f.startswith('Account_')]
    accounts.sort(key=lambda x: int(x.split('_')[1]))  # Sort by Account_1, Account_2, etc.
    return accounts

# Function to get proxy information for the selected account
def get_proxy_for_account(account_name):
    proxy_file_path = os.path.join(proxy_accounts_path, f"{account_name}_proxy.txt")
    if os.path.exists(proxy_file_path):
        with open(proxy_file_path, 'r') as proxy_file:
            return proxy_file.read().strip()
    return None

# Function to save proxy information for the selected account
def save_proxy_for_account(account_name, proxy):
    proxy_file_path = os.path.join(proxy_accounts_path, f"{account_name}_proxy.txt")
    os.makedirs(os.path.dirname(proxy_file_path), exist_ok=True)
    with open(proxy_file_path, 'w') as proxy_file:
        proxy_file.write(proxy)

# Main page with a dropdown list of accounts
@app.route('/')
def index():
    accounts = get_tdata_accounts()
    current_account = request.args.get('current_account', '')
    current_proxy = get_proxy_for_account(current_account) if current_account else ''
    return render_template_string(html_template, accounts=accounts, message='', current_account=current_account, current_proxy=current_proxy)

# Handler to switch accounts
@app.route('/switch', methods=['POST'])
def switch_account():
    selected_account = request.form['account']
    selected_tdata_path = os.path.join(tdata_accounts_path, selected_account, 'tdata')
    proxy = request.form.get('proxy', '')

    # Save proxy for the selected account
    if proxy:
        save_proxy_for_account(selected_account, proxy)

    try:
        # Log the process of switching accounts
        print(f"[INFO] Attempting to close Telegram...")
        # Close all Telegram processes
        subprocess.call(["pkill", "-f", "Telegram"])
        print(f"[INFO] Telegram has been closed successfully.")

        # Log the process of switching accounts
        print(f"[INFO] Switching to account: {selected_account}")
        print(f"[INFO] Using tdata from: {selected_tdata_path}")
        if proxy:
            print(f"[INFO] Using proxy: {proxy}")

        # Ensure the tdata path exists before creating a symbolic link
        if not os.path.exists(selected_tdata_path):
            raise FileNotFoundError(f"The selected tdata path does not exist: {selected_tdata_path}")

        # Check if the symbolic link tdata already exists
        if os.path.islink(tg_symlink_path):
            current_link = os.readlink(tg_symlink_path)
            if current_link == selected_tdata_path:
                print(f"[INFO] The existing symbolic link already points to the correct tdata folder.")
            else:
                os.remove(tg_symlink_path)
                os.symlink(selected_tdata_path, tg_symlink_path)
                print(f"[INFO] Updated symbolic link for tdata at {tg_symlink_path}")
        else:
            # Remove existing folder if it's not a symlink
            if os.path.exists(tg_symlink_path):
                shutil.rmtree(tg_symlink_path)
                print(f"[INFO] Removed existing folder at {tg_symlink_path}")
            # Create a new symbolic link
            os.symlink(selected_tdata_path, tg_symlink_path)
            print(f"[INFO] Created new symbolic link for tdata at {tg_symlink_path}")

        # Form the command to start Telegram with proxy settings if applicable
        telegram_command_list = [telegram_command, '-workdir', telegram_workdir]
        if proxy:
            telegram_command_list.extend(['--proxy-server', proxy])
            print(f"[INFO] Proxy settings applied: {proxy}")

        # Restart Telegram
        subprocess.Popen(telegram_command_list)
        time.sleep(2)  # Wait for Telegram to restart

        # Log success and notify about account switching
        message = f"Account switched to: {selected_account}. Telegram has been restarted."
        print(f"[SUCCESS] {message}")
        return render_template_string(success_template, message=message, current_account=selected_account)
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        print(f"[ERROR] {message}")
        return render_template_string(success_template, message=message, current_account=selected_account)

# Start Flask server
if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("FLASK_RUN_PORT", 5000)))
