import sys
import argparse
from wd_wowdiscord import WowDiscord

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",default = 'wowdiscord.conf')
    args = parser.parse_args()
    wd = WowDiscord(args.c)
    wd.read_news()
