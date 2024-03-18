import argparse
import requests
import threading
import os


class Stats:
    def __init__(self):
        self.total_checked = 0
        self.valid_found = 0
        self.not_found = 0
        self.server_errors = 0

    def increment_total_checked(self):
        self.total_checked += 1

    def increment_valid_found(self):
        self.valid_found += 1

    def increment_not_found(self):
        self.not_found += 1

    def increment_server_errors(self):
        self.server_errors += 1


def path_traversal(url, wordlist, num_threads, verbose):
    if not os.path.exists(wordlist):
        print("Error: Wordlist file does not exist.")
        return

    valid_paths = []
    stats = Stats()

    with open(wordlist, 'r') as f:
        paths = f.readlines()

    # Calculate number of paths per thread
    paths_per_thread = len(paths) // num_threads

    # Slice paths list based on the number of threads
    sliced_paths = [paths[i:i + paths_per_thread] for i in range(0, len(paths), paths_per_thread)]

    def check_paths(sub_paths):
        nonlocal valid_paths
        for path in sub_paths:
            path = path.strip()
            target_url = f"{url}{path}"
            try:
                response = requests.get(target_url)
                stats.increment_total_checked()
                if response.status_code == 200:
                    valid_paths.append(target_url)
                    stats.increment_valid_found()
                    if verbose:
                        print("[+] Found:", target_url)
                elif response.status_code == 404:
                    stats.increment_not_found()
                    if verbose:
                        print("[-] Not Found:", target_url)
                else:
                    stats.increment_server_errors()
                    if verbose:
                        print("[!] Server Error:", target_url, "- Status Code:", response.status_code)
            except Exception as e:
                if verbose:
                    print("[!] Error accessing:", target_url, "- Reason:", e)

    threads = []
    for i, sub_paths in enumerate(sliced_paths):
        thread = threading.Thread(target=check_paths, args=(sub_paths,))
        threads.append(thread)
        thread.start()
        if verbose:
            print(f"Thread {i + 1} started")

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        if verbose:
            print(f"Thread {thread.ident} finished")

    # Print statistics
    print("\nStatistics:")
    print("Total paths checked:", stats.total_checked)
    print("Valid paths found:", stats.valid_found)
    print("Paths not found:", stats.not_found)
    print("Server errors:", stats.server_errors)

    # Print valid paths
    print("\nValid Paths:")
    for path in valid_paths:
        print(path)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Path Traversal Tool")
    parser.add_argument("--url", help="Target URL", required=True)
    parser.add_argument("--wordlist", help="Path to wordlist file", required=True)
    parser.add_argument("--threads", help="Number of threads (default: 5)", type=int, default=5)
    parser.add_argument("--verbose", help="Enable verbose mode", action="store_true")
    return parser.parse_args()


def main():
    args = parse_arguments()
    path_traversal(args.url, args.wordlist, args.threads, args.verbose)


if __name__ == "__main__":
    main()
