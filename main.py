import os
import telegram
import asyncio
import schedule
import time
from rstr import xeger
from datetime import datetime
from colorama import Fore, init
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize colorama
init(autoreset=True)

# =========================================================================================
# === Telegram Bot Information - Fill this section with your credentials =========================
# =========================================================================================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHANNEL_ID = "@YOUR_CHANNEL_USERNAME"
# =========================================================================================

class AvastKeyGenerator:
    def __init__(self):
        self.key_pattern = (
            r"MCT[79RBYN2GKZ][XK37BM4FP8Y]-[DZCXBY9NMKJ][NKZBQXR9M27P][HP8DMJRF6XB24][3826MX9K7]"
            r"[BD3FKH2GX8Q7]-[73K28GRN6QJ][6HMG3Y82WCK][HCWFKJ7432D9][D9YXRGPHJK2][6ZT4FNBWQHXD2G]"
            r"-[Y89G2Z3M7FQ][427P8ZNQ93X6][JE7KVDUWGQTZYC][KGUD6HFR98Y][NEP4UDBSVXQ]"
        )
        self.keys_per_run = 10

    def generate_keys(self):
        """Generates a list of 10 keys."""
        return [xeger(self.key_pattern) for _ in range(self.keys_per_run)]

    async def send_to_telegram(self, keys):
        """Formats and sends the keys to the Telegram channel with download buttons."""
        if not keys:
            print("No keys generated to send.")
            return

        keys_formatted = "\n".join(f"> `{key}`" for key in keys)
        message = f"Avast secureline vpn codes:\n\n{keys_formatted}"

        # Create inline keyboard buttons with the new order
        keyboard = [
            [
                InlineKeyboardButton("Android", url="https://play.google.com/store/apps/details?id=com.avast.android.vpn"),
                InlineKeyboardButton("iOS", url="https://apps.apple.com/app/avast-secureline-vpn-proxy/id793096595")
            ],
            [
                InlineKeyboardButton("Windows PC", url="https://www.avast.com/secureline-vpn#pc"),
                InlineKeyboardButton("macOS", url="https://www.avast.com/secureline-vpn#mac")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            await bot.send_message(
                chat_id=TELEGRAM_CHANNEL_ID,
                text=message,
                parse_mode='MarkdownV2',
                reply_markup=reply_markup
            )
            print(f"[{datetime.now()}] Successfully sent {len(keys)} keys to Telegram.")
        except Exception as e:
            error_message = str(e).replace('-', r'\-').replace('.', r'\.')
            print(f"[{datetime.now()}] Failed to send keys to Telegram. Error: {error_message}")


async def job():
    """The main job to be scheduled."""
    print(f"[{datetime.now()}] Running the job to generate and send keys...")
    generator = AvastKeyGenerator()
    keys = generator.generate_keys()
    await generator.send_to_telegram(keys)


def main():
    """Schedules and runs the job."""
    print(Fore.LIGHTCYAN_EX + "made with ❤️ by @mehdiasmart")
    
    print("Script started. Scheduling the job every 8 hours.")
    schedule.every(8).hours.do(lambda: asyncio.run(job()))

    print("Running the job for the first time...")
    asyncio.run(job())

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN" or TELEGRAM_CHANNEL_ID == "@YOUR_CHANNEL_USERNAME":
        print(Fore.RED + "Error: Please set your TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in the script.")
    else:
        main()
