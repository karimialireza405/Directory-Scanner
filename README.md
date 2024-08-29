# Advanced Directory Scanner

This project is an advanced directory scanner for websites, built in Python. It supports multithreading, logging, specific file checks, and progress tracking.

## **Advanced Directory Scanner**

The **Advanced Directory Scanner** is a Python-based tool designed to perform efficient and robust directory scanning on websites. It is particularly useful for penetration testers, security researchers, and developers who need to identify accessible directories on a web server. The script leverages multithreading for speed, provides logging capabilities, and includes advanced features like specific file checks within directories.

### **Key Features**

- **Multithreading**: The scanner utilizes multiple threads to perform faster scans by checking multiple directories simultaneously.
- **Logging**: Results of the scan, including found directories and specific files, are logged to a specified file, making it easy to review findings later.
- **Specific File Checks**: Beyond scanning directories, the script can check for the existence of specific files (e.g., `index.php`, `admin.php`) within those directories.
- **Progress Tracking**: A progress bar is displayed during the scan, providing real-time feedback on the scanning process.
- **Timeout and Retry Mechanism**: The scanner handles slow or unresponsive servers by implementing timeouts and retries, ensuring that the scan completes efficiently.


## Installation

Install the required Python packages using pip And run script:

```bash
git clone https://github.com/karimialireza405/Directory-Scanner.git

pip install -r requirements.txt

python3 directory-scanner.py
