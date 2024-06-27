import argparse
import os
from urllib.request import urlopen

from config import settings as s

my_parser = argparse.ArgumentParser(
    description="Print a greeting based on the provided argument."
)
my_parser.add_argument(
    "-f",
    "--file_healthcheck",
    action="store_true",
    help="the type of healthcheck",
    required=False,
)
args = my_parser.parse_args()


def test_api_alive():
    """
    A function to test the API's liveliness by making a request to http://127.0.0.1:8000/healthcheck,
    and exiting with status code 0 if the response status is 200 and message is "OK"; otherwise, exiting with status code 1.
    """
    try:
        with urlopen("http://127.0.0.1:8000/healthcheck") as resp:
            if resp.status == 200 and resp.msg == "OK":
                exit(0)
            else:
                exit(1)
    except Exception:
        exit(1)


def test_file_alive():
    """
    This function tests the existence and deletion of a file specified by the `CORE_ALIVE_FILE_PATH` setting.

    This function attempts to open the file specified by `CORE_ALIVE_FILE_PATH` in read mode.
    If the file exists and can be opened, the function exits with a status code of 1.
    If the file does not exist or cannot be opened, the function exits with a status code of 1.
    After successfully opening the file, the function deletes the file and exits with a status code of 0.

    Parameters:
        None

    Returns:
        None
    """
    try:
        with open(s.CORE_ALIVE_FILE_PATH, "r") as f:
            pass
        os.remove(s.CORE_ALIVE_FILE_PATH)
        exit(0)
    except Exception:
        exit(1)


if __name__ == "__main__":
    if args.file_healthcheck:
        test_file_alive()
    else:
        test_api_alive()
