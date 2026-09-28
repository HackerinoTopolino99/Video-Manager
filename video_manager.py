#!/bin/python3

import argparse
import mimetypes
import os
import sys


def __get_videos():
    files = os.listdir()
    files.sort()

    videos = []

    for f in files:
        if os.path.isdir(f):
            continue
        else:
            try:
                if mimetypes.guess_type(f)[0].startswith("video"):
                    videos.append(f)
            except AttributeError:
                pass

    return videos


def compression(acceleration):
    videos = __get_videos()

    if not os.path.exists("output"):
        os.mkdir("output")

    for v in videos:
        if not os.path.exists(f"output/{v}"):
            if acceleration == "h264_vaapi":
                cmd = f"ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -hwaccel_output_format vaapi -i '{v}' -c:v h264_vaapi -crf 30 'output/{v}'"
            else:
                cmd = f"ffmpeg -i '{v}' -vcodec {acceleration} -crf 30 'output/{v}'"

            print(cmd)
            if os.system(cmd):
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
                    choices=["gpu", "cpu"],
                    help="compress videos in the directory specified")
parser.add_argument(
    "-c", "--convert",
    help="convert videos in the directory specified", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    if not (args.compress != args.convert):
        parser.print_help()
        sys.exit(-1)

    try:
        os.chdir(args.directory)
    except FileNotFoundError:
        print("ERROR: Directory not found")
        sys.exit(-1)

    print(os.listdir())

    if args.compress:
        if args.compress == "cpu":
            ret = compression("libx264")
        elif args.compress == "gpu":
            ret = compression("h264_vaapi")

        if not ret:
            print("ERROR: Compression Failed")
            sys.exit(-1)

        sys.exit(0)

    if args.convert:
        if not conversion():
            print("ERROR: Conversion Failed")
            sys.exit(-1)
        sys.exit(0)
