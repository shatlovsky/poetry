#!/usr/bin/env python3

from firebase import firebase
from google.cloud import storage
import argparse
import logging
import pychromecast

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
            print(self.chromecast)

        if self.chromecast is None:
            self.chromecast = chromecasts.pop(0)

        logging.debug("Casting to %s" % self.chromecast.device.friendly_name)

    def set_loglevel(self, args):
        if args.verbose and args.verbose >= 1:
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

        self.select_chromecast(args.device)

        self.run()

    def run(self):
        media = "https://firebasestorage.googleapis.com/v0/b/poetry-f6e45.appspot.com/o/verse%2F23%20%D0%9D%D0%B5%20%D0%B2%D1%8B%D1%85%D0%BE%D0%B4%D0%B8%20%D0%B8%D0%B7%20%D0%BA%D0%BE%D0%BC%D0%BD%D0%B0%D1%82%D1%8B%201970.mp3?alt=media&token=fd05f55d-381e-48a1-86bf-b097b6c58b46"
        logging.debug("Casting %s" % (media))
        cc = self.chromecast
        cc.wait()
        mc = self.chromecast.media_controller
        mc.play_media(media, content_type='audio/mpeg')
        mc.block_until_active()
        print(mc.status)


def main(args):
    ReadAloud()

if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
