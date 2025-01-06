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
from tqdm import tqdm

logging.basicConfig(
    filename='bwf.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

DOWNLOAD_FOLDER = os.getenv('DOWNLOAD_FOLDER')
BASE_FILENAME = os.getenv('BASE_FILENAME')
PROCESSED_FOLDER = os.getenv('PROCESSED_FOLDER')
WEBSITE_URL = os.getenv('WEBSITE_URL')
XPATH_FILE = os.getenv('XPATH_FILE')

class FileDownloader:
    def __init__(self, download_folder, website_url, xpath_file):
        self.download_folder = download_folder
        self.website_url = website_url
        self.xpath_file = xpath_file

    def setup_webdriver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {"download.default_directory": self.download_folder})
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=chrome_options)

    def download_file(self):
        driver = self.setup_webdriver()
        try:
            logging.info("Accessing the website to download the file.")
            driver.get(self.website_url)
            time.sleep(5)
            file_element = driver.find_element(By.XPATH, self.xpath_file)
            file_element.click()
            logging.info("Download in progress...")
            download_in_progress = True
            while download_in_progress:
                time.sleep(1)
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
    
    def process_file(self, file_path):
        today_date = datetime.now().strftime('%Y%m%d')
        output_folder = os.path.join(self.processed_folder, f"WalletsBTC_{today_date}")
        os.makedirs(output_folder, exist_ok=True)

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

                prefix = '1' if address.startswith('1') else '3' if address.startswith('3') else 'bc1'
                files[f'{prefix}_no_balance'].write(f"{address}\n")
                files[f'{prefix}_with_balance'].write(f"{address}\t{balance_btc:.8f}\n")

                if balance_btc <= 0.1:
                    files[f'{prefix}_balance_0_1_no_balance'].write(f"{address}\n")
                    files[f'{prefix}_balance_0_1_with_balance'].write(f"{address}\t{balance_btc:.8f}\n")

        for f in files.values():
            f.close()

        shutil.move(file_path, os.path.join(output_folder, os.path.basename(file_path)))
        logging.info(f"File processed and moved to : {output_folder}")

def main():
    downloader = FileDownloader(DOWNLOAD_FOLDER, WEBSITE_URL, XPATH_FILE)
    processor = FileProcessor(DOWNLOAD_FOLDER, PROCESSED_FOLDER)

    try:
        downloader.download_file()
        latest_file = processor.get_latest_file(BASE_FILENAME)
        decompressed_file = processor.decompress_file(latest_file)        
        processor.process_file(decompressed_file)
    except Exception as e:
        logging.error(f"Error: {e}")


def schedule_daily_task():
    while True:
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
        main()
        logging.info("Task completed.")

        tomorrow_4am = random_time + timedelta(days=1)
        time_until_next_day = (tomorrow_4am.replace(hour=4, minute=0, second=0, microsecond=0) - datetime.now()).total_seconds()
        logging.info(f"Waiting until tomorrow 4:00 : {time_until_next_day // 3600} hours and {(time_until_next_day % 3600) // 60} minutes.")
        time.sleep(time_until_next_day)

if __name__ == "__main__":
    schedule_daily_task()
