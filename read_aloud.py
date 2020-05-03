#!/usr/bin/env python3

import pychromecast
import argparse
import logging

class ReadAloud:
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--verbose', '-v', action='count')
        parser.add_argument("--device")
        parser.add_argument("--list", nargs="?", const=1)
        return parser.parse_args()

    def select_chromecast(self, device):
        chromecasts = pychromecast.get_chromecasts()
        if not chromecasts:
            logging.error("No Chromecast(s) found")
            raise RuntimeError("No Chromecast(s) found")

        if device is not None:
            for cc in chromecasts:
                if cc.device.friendly_name == device:
                    self.chromecast = cc
            if self.chromecast is None:
                logging.warn("Device '%s' not found, switch to default" % (device))

        if self.chromecast is None:
            self.chromecast = chromecasts.pop(0)

        logging.debug("Casting to %s" % self.chromecast.device.friendly_name)

    def set_loglevel(self, args):
        if args.verbose >= 1:
            logging.basicConfig(level=logging.DEBUG)

    def list_chromecasts(self):
        chromecasts = pychromecast.get_chromecasts()
        print("Found Chromecast(s):")
        for cc in chromecasts:
            print(" - %s" % (cc.device.friendly_name))

    def __init__(self):
        args = self.parse_args()

        self.set_loglevel(args)

        if args.list:
            self.list_chromecasts()
            quit(0)

        self.chromecast = self.select_chromecast(args.device)


    def run(self):
        pass


def main(args):
    ReadAloud()

if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
