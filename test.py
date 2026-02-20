from datetime import datetime


def current_time() -> str:
    return datetime.isoformat(datetime.now())


print(f"{current_time()} running test.py")
