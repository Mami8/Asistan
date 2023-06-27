from qbittorrent import client
import argparse
import telegram_bot_handler as th

with open("D:\\Code\\Piton\\torrent.txt") as f:
    global target_torrent
    target_torrent = f.read()


def boyut_formatla(b, factor=1024, suffix="B"):
    """
    byte büyüklükleri daha güzel hale getirir.
    örn:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def bagla(login="admin", passwd="313131"):
    qb = client.Client("http://127.0.0.1:8080/")
    qb.login(login, passwd)
    return qb


qb = bagla()
torrents = qb.torrents()


def torrent_listele(istenen=""):
    if istenen == "":
        for torrent in torrents:
            print("Torrent name:", torrent["name"])
            print("hash:", torrent["hash"])
            print("Seeds:", torrent["num_seeds"])
            print("File size:", boyut_formatla(torrent["total_size"]))
            print("Download speed:", boyut_formatla(torrent["dlspeed"]) + "/s")
            print("Amount left:", boyut_formatla(torrent["amount_left"]))
            print(
                "\n-----(\_O_/)-----(\_O_/)-----(\_O_/)-----(\_O_/)-----(\_O_/)-----\n"
            )
    else:
        for torrent in torrents:
            if torrent["name"] == istenen:
                print("Torrent name:", torrent["name"])
                print("hash:", torrent["hash"])
                print("Seeds:", torrent["num_seeds"])
                print("File size:", boyut_formatla(torrent["total_size"]))
                print("Download speed:", boyut_formatla(torrent["dlspeed"]) + "/s")
                print("Amount left:", boyut_formatla(torrent["amount_left"]))
                break


def torrent_devam_et():
    torrent = ""
    for i in torrents:
        if i["name"] == target_torrent:
            torrent = i["hash"]
            break
    if not torrent:
        print("Bruh, torrent is none")
    else:
        qb.resume(torrent)


def torrent_durdur(torrent_listesi=[], hepsi_mi=True):
    if hepsi_mi:
        qb.pause_all()
    else:
        torrent_hashs = []
        for i in torrents:
            if i["name"] in torrent_listesi:
                torrent_hashs.append(i["hash"])
        qb.pause_multiple(torrent_hashs)


def torrent_bitti_mi():
    for torrent in torrents:
        if torrent["name"] == target_torrent:
            if not torrent["amount_left"]:
                th.send_message(f"{target_torrent} bitti!")
            else:
                total_size = torrent["total_size"]
                remaining_size = torrent["amount_left"]
                downloaded_size = total_size - remaining_size
                progress = (downloaded_size / total_size) * 100
                th.send_message(
                    f"{target_torrent} için {boyut_formatla(torrent['amount_left'])} kaldı\nİlerleme: {progress:.2f}%"
                )


def main():
    parser = argparse.ArgumentParser(description="qBittorrent Automation Script")
    parser.add_argument(
        "-r",
        "--resume",
        action="store_true",
        help="Resume the torrent that is in the txt file. You have to manually edit it to change torrent starting.",
    )
    parser.add_argument("-p", "--pause", action="store_true", help="Pause all torrents")
    parser.add_argument(
        "-S", "--status", action="store_true", help="Hedef torrent bitmiş mi?"
    )

    args = parser.parse_args()

    if args.resume:
        torrent_devam_et()

    if args.pause:
        torrent_durdur()
        
    if args.status:
        torrent_bitti_mi()


if __name__ == "__main__":
    main()
