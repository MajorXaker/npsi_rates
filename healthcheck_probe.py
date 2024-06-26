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
    try:
        with urlopen("http://127.0.0.1:8000/healthcheck") as resp:
            if resp.status == 200 and resp.msg == "OK":
                exit(0)
            else:
                exit(1)
    except Exception:
        exit(1)


def test_file_alive():
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
