import argparse
from wd_wowdiscord import MainClass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",default = 'wowdiscord.conf')
    args = parser.parse_args()
    wd = MainClass(args.c)
    wd.process_news()

