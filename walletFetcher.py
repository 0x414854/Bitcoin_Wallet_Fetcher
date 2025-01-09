import csv
import gzip
import logging
import os
import random
import shutil
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from shadePy import Colors
from tqdm import tqdm

GREEN, RED, CYAN, BRIGHT_GREY, YELLOW, RESET = (
    Colors.GREEN, Colors.RED, Colors.CYAN,Colors.BRIGHTGREY, Colors.YELLOW, Colors.RESET
)

load_dotenv()

BCH_BASE_FILENAME = os.getenv('BCH_BASE_FILENAME')
BCH_WEBSITE_URL = os.getenv('BCH_WEBSITE_URL')
BTC_BASE_FILENAME = os.getenv('BTC_BASE_FILENAME')
BTC_WEBSITE_URL = os.getenv('BTC_WEBSITE_URL')
DOWNLOAD_FOLDER = os.getenv('DOWNLOAD_FOLDER')
LOG_FILE = os.getenv("LOG_FILE")
BTC_PROCESSED_FOLDER = os.getenv('BTC_PROCESSED_FOLDER')
BCH_PROCESSED_FOLDER = os.getenv('BCH_PROCESSED_FOLDER')
XPATH_FILE = os.getenv('XPATH_FILE')

logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/117.0.0.0 Mobile/15E148 Safari/604.1"
]

class FileDownloader:
    def __init__(self, download_folder, website_url, xpath_file):
        self.download_folder = download_folder
        self.website_url = website_url
        self.xpath_file = xpath_file

    def setup_webdriver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {"download.default_directory": self.download_folder})
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        user_agent = random.choice(USER_AGENTS)
        chrome_options.add_argument(f"user-agent={user_agent}")
        logging.info(f"Using User-Agent : {user_agent}")

        return webdriver.Chrome(options=chrome_options)

    def download_file(self):
        driver = self.setup_webdriver()
        try:
            logging.info("Accessing the website to download the file.")
            driver.get(self.website_url)
            time.sleep(random.uniform(3, 6))

            file_element = driver.find_element(By.XPATH, self.xpath_file)
            file_element.click()
            logging.info("Download in progress...")
            
            download_in_progress = True
            while download_in_progress:
                time.sleep(random.uniform(1, 2))
                download_in_progress = any(
                    file.endswith(".crdownload") for file in os.listdir(self.download_folder)
                )
            logging.info("File downloaded successfully.")
        finally:
            driver.quit()

class FileProcessor:
    def __init__(self, download_folder, processed_folder):
        self.download_folder = download_folder
        self.processed_folder = processed_folder

    def get_latest_file(self, base_filename):
        files = [f for f in os.listdir(self.download_folder) if f.startswith(base_filename)]
        if not files:
            raise FileNotFoundError("No matching file found.")
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(self.download_folder, x)))
        logging.info(f"Latest file found : {latest_file}")
        return os.path.join(self.download_folder, latest_file)

    def decompress_file(self, file_path):
        if not file_path.endswith('.gz'):
            return file_path
        
        decompressed_path = file_path.rstrip('.gz')
        with gzip.open(file_path, 'rb') as f_in, open(decompressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        
        logging.info(f"File decompressed : {decompressed_path}")
        return decompressed_path
    
    def process_file(self, file_path, crypto_type):
        today_date = datetime.now().strftime('%Y%m%d')
        output_folder = os.path.join(self.processed_folder, f"Wallets{crypto_type}_{today_date}")
        os.makedirs(output_folder, exist_ok=True)

        if crypto_type == "Bitcoin (BTC)":
            files = {
                '1_no_balance': open(os.path.join(output_folder, '1_no_balance_all.txt'), 'w'),
                '3_no_balance': open(os.path.join(output_folder, '3_no_balance_all.txt'), 'w'),
                'bc1_no_balance': open(os.path.join(output_folder, 'bc1_no_balance_all.txt'), 'w'),
                '1_with_balance': open(os.path.join(output_folder, '1_with_balance_all.txt'), 'w'),
                '3_with_balance': open(os.path.join(output_folder, '3_with_balance_all.txt'), 'w'),
                'bc1_with_balance': open(os.path.join(output_folder, 'bc1_with_balance_all.txt'), 'w'),
                '1_balance_0_1_no_balance': open(os.path.join(output_folder, '1_no_balance_get_01.txt'), 'w'),
                '3_balance_0_1_no_balance': open(os.path.join(output_folder, '3_no_balance_get_01.txt'), 'w'),
                'bc1_balance_0_1_no_balance': open(os.path.join(output_folder, 'bc1_no_balance_get_01.txt'), 'w'),
                '1_balance_0_1_with_balance': open(os.path.join(output_folder, '1_with_balance_get_01.txt'), 'w'),
                '3_balance_0_1_with_balance': open(os.path.join(output_folder, '3_with_balance_get_01.txt'), 'w'),
                'bc1_balance_0_1_with_balance': open(os.path.join(output_folder, 'bc1_with_balance_get_01.txt'), 'w'),
                'all_no_balance': open(os.path.join(output_folder, 'all_no_balance.txt'), 'w'),
                'all_with_balance': open(os.path.join(output_folder, 'all_with_balance.txt'), 'w')
            }
        elif crypto_type == "Bitcoin Cash (BCH)":
            files = {
                'p_no_balance': open(os.path.join(output_folder, 'p_no_balance_all.txt'), 'w'),
                'q_no_balance': open(os.path.join(output_folder, 'q_no_balance_all.txt'), 'w'),
                'other_no_balance': open(os.path.join(output_folder, 'other_no_balance_all.txt'), 'w'),
                'p_with_balance': open(os.path.join(output_folder, 'p_with_balance_all.txt'), 'w'),
                'q_with_balance': open(os.path.join(output_folder, 'q_with_balance_all.txt'), 'w'),
                'other_with_balance': open(os.path.join(output_folder, 'other_with_balance_all.txt'), 'w'),
                'p_balance_1_no_balance': open(os.path.join(output_folder, 'p_no_balance_get_01.txt'), 'w'),
                'q_balance_1_no_balance': open(os.path.join(output_folder, 'q_no_balance_get_01.txt'), 'w'),
                'other_balance_1_no_balance': open(os.path.join(output_folder, 'other_no_balance_get_01.txt'), 'w'),
                'p_balance_1_with_balance': open(os.path.join(output_folder, 'p_with_balance_get_01.txt'), 'w'),
                'q_balance_1_with_balance': open(os.path.join(output_folder, 'q_with_balance_get_01.txt'), 'w'),
                'other_balance_1_with_balance': open(os.path.join(output_folder, 'other_with_balance_get_01.txt'), 'w'),
                'all_no_balance': open(os.path.join(output_folder, 'all_no_balance.txt'), 'w'),
                'all_with_balance': open(os.path.join(output_folder, 'all_with_balance.txt'), 'w')
            }

        with open(file_path, newline='') as f:
            total_lines = sum(1 for _ in f) - 1

        with open(file_path, newline='') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader)

            for line in tqdm(reader, total=total_lines, desc="Processing addresses "):
                address = line[0]
                balance_satoshis = int(line[1])
                balance_btc = balance_satoshis / 100000000

                files['all_no_balance'].write(f"{address}\n")
                files['all_with_balance'].write(f"{address}\t{balance_btc:.8f}\n")

                if crypto_type == "Bitcoin (BTC)":
                    prefix = '1' if address.startswith('1') else '3' if address.startswith('3') else 'bc1'
                elif crypto_type == "Bitcoin Cash (BCH)":
                    prefix = 'p' if address.startswith('p') else 'q' if address.startswith('q') else 'other'

                files[f'{prefix}_no_balance'].write(f"{address}\n")
                files[f'{prefix}_with_balance'].write(f"{address}\t{balance_btc:.8f}\n")

                if balance_btc <= 0.1:
                    files[f'{prefix}_balance_0_1_no_balance'].write(f"{address}\n")
                    files[f'{prefix}_balance_0_1_with_balance'].write(f"{address}\t{balance_btc:.8f}\n")

        for f in files.values():
            f.close()

        shutil.move(file_path, os.path.join(output_folder, os.path.basename(file_path)))
        logging.info(f"File processed and moved to : {output_folder}")

def choose_crypto():
    logging.info("Starting the cryptocurrency choice process.")

    print(f"\n{BRIGHT_GREY}Which crypto wallet addresses would you like to process ?{RESET}\n")
    print(f"{YELLOW}[1]{RESET} Bitcoin ({CYAN}BTC{RESET})")
    print(f"{YELLOW}[2]{RESET} Bitcoin Cash ({CYAN}BCH{RESET})")
    print(f"{YELLOW}[0]{RESET} Exit")

    while True:
        try:
            choice = int(input(f"\n{BRIGHT_GREY}Enter the number of your choice : {RESET}"))
            logging.info(f"User entered choice : {choice}")

            if choice == 1:
                logging.info("User chose Bitcoin (BTC).")
                return 'Bitcoin (BTC)'
            elif choice == 2:
                logging.info("User chose Bitcoin Cash (BCH).")
                return 'Bitcoin Cash (BCH)'
            elif choice == 0:
                logging.info("User chose to exit the program.")
                print("Exiting the program.")
                exit()
            else:
                logging.warning(f"Invalid option entered : {choice}. Prompting user again.")
                print(f"\n{RED}ERROR: Invalid option, please choose a valid number (1, 2, or 0 to exit).{RESET}")
        except ValueError:
            logging.error("Invalid input entered. Expected an integer.")
            print(f"\n{RED}ERROR: Invalid input, please enter a number.{RESET}")

def main(crypto_choice):
    if crypto_choice == "Bitcoin (BTC)":
        downloader = FileDownloader(DOWNLOAD_FOLDER, BTC_WEBSITE_URL, XPATH_FILE)
        processor = FileProcessor(DOWNLOAD_FOLDER, BTC_PROCESSED_FOLDER)
    else:
        downloader = FileDownloader(DOWNLOAD_FOLDER, BCH_WEBSITE_URL, XPATH_FILE)
        processor = FileProcessor(DOWNLOAD_FOLDER, BCH_PROCESSED_FOLDER)

    try:
        downloader.download_file()
        base_filename = BTC_BASE_FILENAME if crypto_choice == "Bitcoin (BTC)" else BCH_BASE_FILENAME
        latest_file = processor.get_latest_file(base_filename)
        decompressed_file = processor.decompress_file(latest_file)        
        processor.process_file(decompressed_file, crypto_choice)
    except Exception as e:
        logging.error(f"Error: {e}")

def schedule_daily_task():
    while True:
        crypto_choice = choose_crypto()
        now = datetime.now()
        target_day = now
        if now.hour >= 6:
            target_day += timedelta(days=1)
        
        random_time = target_day.replace(hour=4, minute=0, second=0, microsecond=0) + timedelta(
            minutes=random.randint(0, 120)
        )
        
        logging.info(f"Next execution time : {random_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        time_until_execution = (random_time - now).total_seconds()
        if time_until_execution > 0:
            hours = int(time_until_execution // 3600)
            minutes = int((time_until_execution % 3600) // 60)
            logging.info(f"Waiting {hours} hours and {minutes} minutes before execution.")
            time.sleep(time_until_execution)
        
        logging.info("Starting the scheduled task.")
        main(crypto_choice)
        logging.info("Task completed.")

        tomorrow_4am = random_time + timedelta(days=1)
        time_until_next_day = (tomorrow_4am.replace(hour=4, minute=0, second=0, microsecond=0) - datetime.now()).total_seconds()
        logging.info(f"Waiting until tomorrow 4:00 : {time_until_next_day // 3600} hours and {(time_until_next_day % 3600) // 60} minutes.\n")
        time.sleep(time_until_next_day)

if __name__ == "__main__":
    schedule_daily_task()
