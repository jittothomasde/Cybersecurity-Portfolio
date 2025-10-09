## 💻 Custom Tool: Multi-threaded Port Scanner

### 📌 Executive Summary

This project involved the development of a custom, multi-threaded `TCP` port scanner written in Python 3. The objective was to demonstrate foundational skills in network socket programming, concurrency management, and scripting complex reconnaissance tasks.

The tool was successfully executed against the target Metasploitable 2 VM, rapidly identifying all open ports (21, 22, 80, 8180, etc.) significantly faster than a single-threaded implementation. This validates the ability to develop custom, efficient tools for the initial stages of a penetration test.

**Key Technologies:** Python 3, `socket` module, `threading` module, `Queue` module.

-----

### 🔬 Technical Details and Implementation

#### 1\. Core Concepts

  * **Socket Programming (`socket` module):** The script uses the `socket` module to initiate `TCP` connection attempts `SOCK\STREAM` to a specific IP address and port number. The `connect\ex()` function is used because it returns an error code `( for success, meaning the port is open` instead of raising an exception, which is faster and cleaner for scanning.
  * **Concurrency ($\text{threading}$ module):** Network operations are I/O-bound (the computer spends most of its time waiting for a response). To overcome this performance bottleneck, the script utilizes $\text{threading}$ to execute multiple port checks simultaneously, dramatically reducing the overall scan time.
  * **Job Queue ($\text{Queue}$ module):** The range of ports to be scanned is loaded into a $\text{Queue}$. Multiple worker threads then constantly pull new ports (jobs) from the queue until it is empty, ensuring efficient job distribution.
  * **Output Management ($\text{threading.Lock}$):** A lock is used when printing to the console to ensure that multiple threads writing at the same time do not corrupt the terminal output.

#### 2\. Python Source Code

This script is available in the $\text{/Scripts}$ directory as `fast_scanner.py`.

#### 3\. Demonstration

The script was executed on the Kali VM against the Metasploitable 2 target. The concurrent threading approach significantly reduced the total scan time compared to sequential methods.

  * **Execution Command:** `python3 fast_scanner.py [TARGET_IP] 1 10000`
  * **Result Snapshot:** `./Images/fast_scanner_result.png`.

-----