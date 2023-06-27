import requests
import argparse

with open("D:/Code/Piton/bot_info.txt", "r") as f:
    info = f.readlines()
    TOKEN = info[0].strip()
    chat_id = info[1].strip()


def send_message(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())


def main():
    parser = argparse.ArgumentParser(description="Telegram mesaj gönderme scripti")
    parser.add_argument("message", metavar="N", type=str, help="Message to send")

    args = parser.parse_args()

    if args.message:
        send_message(args.message)


if __name__ == "__main__":
    main()
