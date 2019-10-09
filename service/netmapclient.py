import os
import sys
from bin.access_report import run_report

if not os.path.exists("/usr/local/netmap/.info/"):
    os.makedirs("/usr/local/netmap/.info/")


def help():
    print("usage:\n"
          "python netmapclient.py <uuid>\n")


if __name__ == '__main__':
    try:
        uuid = sys.argv[1]
        if not uuid:
            print("缺少UUID\n")
            help()
            sys.exit(1)
        run_report(uuid)
    except IndexError as e:
        print("缺少UUID\n")
        help()
        sys.exit(1)
