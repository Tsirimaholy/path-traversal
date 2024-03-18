# Usage

```shell
git clone git@github.com:Tsirimaholy/path-traversal.git
cd path-traversal
```

## Install Requirements

Ensure you have Python 3 installed on your system. You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Run the Script

Execute the script with the required arguments:

```bash
python bruteforce.py -h
```

### List of arguments

```
usage: bruteforce.py [-h] --url URL --wordlist WORDLIST [--threads THREADS] [--verbose]

Path Traversal Tool

options:
  -h, --help           show this help message and exit
  --url URL            Target URL
  --wordlist WORDLIST  Path to wordlist file
  --threads THREADS    Number of threads (default: 5)
  --verbose            Enable verbose mode

```

***Example***

```shell
python bruteforce.py --url http://example.com --wordlist paths.txt --threads 10 --verbose
```

### Wordlist Format

The wordlist file should contain a list of paths to be checked for traversal. Each path should be on a separate line in
the file.

Example paths.txt:
```
admin/
images/
scripts/
robots.txt
backup.zip
```
### Output

The script will provide statistics on the paths checked, including the total paths checked, valid paths found, paths not
found (404 errors), and server errors encountered. Additionally, it will display the valid paths discovered during the
traversal test.