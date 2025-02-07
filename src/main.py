from bot import Bot
import pathlib
import sys


def read_api_token(token_path: str):
    return pathlib.Path(token_path).read_text()

def main():
    if len(sys.argv) < 3:
        print("token or calendar path not specified", file=sys.stderr)
        print("usage: main.py <TOKEN> <CALENDAR_PATH>", file=sys.stderr)
        sys.exit(1)
    token = str(sys.argv[1])
    calendar_path = str(sys.argv[2])

    bot = Bot(token=token, calendar_link=calendar_path)
    bot.run()

if __name__ == "__main__":
    main()
