from urllib.request import urlopen


def test_api_alive():
    try:
        with urlopen("http://127.0.0.1:8000/healthcheck") as resp:
            if resp.status == 200 and resp.msg == "OK":
                exit(0)
            else:
                exit(1)
    except Exception:
        exit(1)


if __name__ == "__main__":
    test_api_alive()
