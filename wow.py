import argparse
import wd_wowdiscord

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",default = 'wowdiscord.conf')
    args = parser.parse_args()
    wd = wd_wowdiscord.process_news(args.c)

