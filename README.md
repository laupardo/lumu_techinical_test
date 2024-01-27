# Lumu Technical Test

This Python script (`lumu_technical_test.py`) parses BIND 9 logs and extracts specific information and sends it to the Collectors API. It also calculates and prints statistics based on the log entries.

## Usage

### Prerequisites

- Python 3 installed

### Running the Script

1. Open a terminal or command prompt.
2. Navigate to the directory containing `lumu_technical_test.py`.
3. Run the script with the following command:

    ```bash
    python lumu_technical_test.py path/to/your/bind9.log
    ```

    Replace `path/to/your/bind9.log` with the actual path to your BIND 9 log file. In this repo you will find a file named queries which serves as a sample file.

### Required Imports

Make sure the following Python libraries are installed:

```bash
pip install requests
```
All other imports are part of the standard library.
