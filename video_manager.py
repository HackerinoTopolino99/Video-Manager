#!/bin/python3

import argparse
import mimetypes
import os
import sys


def __get_videos():
    videos = os.listdir()
    videos.sort()

    for v in videos:
        if os.path.isdir(v):
            videos.remove(v)
            continue
        try:
            if not mimetypes.guess_type(v)[0].startswith("video"):
                videos.remove(v)
        except AttributeError:
            videos.remove(v)

    return videos


def compression(acceleration):
    videos = __get_videos()

    if not os.path.exists("output"):
        os.mkdir("output")

    for v in videos:
        if not os.path.exists(f"output/{v}"):
            if os.system(f"ffmpeg -i '{v}' -vcodec {acceleration} -crf 30 'output/{v}'"):
                os.remove(f"output/{v}")
                return False

    return True


def conversion():
    videos = __get_videos()

    for v in videos:
        if not v.endswith("mp4"):
            e = os.system(
                f'ffmpeg -i """{v}""" -codec copy """{v[:v.rfind(".")]}.mp4"""')
            if e:
                os.remove(f"{v[:v.rfind('.')]}.mp4")
                return False

            os.remove(v)

    return True


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory",
                    help="Directory of videos", default="./", action="store")
parser.add_argument("-x", "--compress",
                    choices=["gpu", "cpu"], help="compress videos in the directory specified")
parser.add_argument(
    "-c", "--convert", help="convert videos in the directory specified", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    print(args)
    if not (args.compress != args.convert):
        parser.print_help()
        sys.exit(-1)

    try:
        os.chdir(args.directory)
    except FileNotFoundError:
        print("ERROR: Directory not found")
        sys.exit(-1)

    if args.compress:
        if args.compress == "cpu":
            ret = compression("libx264")
        elif args.compress == "gpu":
            ret = compression("h264_nvenc")

        if not ret:
            print("ERROR: Compression Failed")
            sys.exit(-1)

        sys.exit(0)

    if args.convert:
        if not conversion():
            print("ERROR: Conversion Failed")
            sys.exit(-1)
        sys.exit(0)
