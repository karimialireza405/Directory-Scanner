#Create by Alirez

import requests
import argparse
import threading
from queue import Queue
from colorama import Fore, Style, init
from tqdm import tqdm  # For progress bar
import os

# Initialize colorama
init(autoreset=True)

# Number of threads
NUM_THREADS = 10

# Timeout for requests in seconds
TIMEOUT = 5

# Logging results
def log_results(message, log_file):
    with open(log_file, 'a') as log:
        log.write(message + '\n')

# Worker function for each thread
def worker(queue, base_url, log_file, specific_files):
    while not queue.empty():
        directory = queue.get()
        url = base_url + directory + '/'
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+] Found: {url}")
                log_results(f"[+] Found: {url}", log_file)
                # Check for specific files in the directory
                for file in specific_files:
                    file_url = url + file
                    file_response = requests.get(file_url, timeout=TIMEOUT)
                    if file_response.status_code == 200:
                        print(f"{Fore.CYAN}[+] Found file: {file_url}")
                        log_results(f"[+] Found file: {file_url}", log_file)
            else:
                print(f"{Fore.YELLOW}[-] Not Found: {url} (Status Code: {response.status_code})")
                log_results(f"[-] Not Found: {url} (Status Code: {response.status_code})", log_file)
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Error accessing {url}: {e}")
            log_results(f"[!] Error accessing {url}: {e}", log_file)
        finally:
            queue.task_done()

def scan_directory(base_url, wordlist_path, log_file, specific_files):
    # Ensure the base URL ends with a slash
    if not base_url.endswith('/'):
        base_url += '/'
    
    # Open the wordlist file
    try:
        with open(wordlist_path, 'r') as wordlist:
            directories = wordlist.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Wordlist file {wordlist_path} not found.")
        return
    
    # Initialize the queue and threads
    queue = Queue()
    for directory in directories:
        queue.put(directory.strip())

    # Set up progress bar
    progress = tqdm(total=len(directories), desc="Scanning directories", ncols=100, unit=" directory")

    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(queue, base_url, log_file, specific_files))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    queue.join()
    progress.close()

    # Ensure all threads are completed
    for thread in threads:
        thread.join()

    print(f"{Fore.BLUE}[*] Scanning complete. Results are logged in {log_file}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Advanced Directory Scanner with Multithreading, Logging, and File Checking.")
    parser.add_argument('url', type=str, help="The base URL of the website to scan (e.g., http://example.com)")
    parser.add_argument('wordlist', type=str, help="The path to the wordlist file (e.g., directories.txt)")
    parser.add_argument('--log', type=str, default="scan_results.log", help="File to log the results (default: scan_results.log)")
    parser.add_argument('--files', type=str, nargs='*', default=[], help="Specific files to check within each directory (e.g., index.php, admin.php)")

    # Parse arguments
    args = parser.parse_args()

    # Run the directory scan with provided arguments
    scan_directory(args.url, args.wordlist, args.log, args.files)
