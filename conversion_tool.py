"""

Script for converting video (.mp4) to audio (.wav) using ffmpeg.

Keeps your original video (makes a copy of the audio only).
Please see package requirements below and ensure you have downloaded ffmpeg
from https://www.ffmpeg.org/download.html. Additionally, check out the comments
below for input/output specifications and the respective chosen audio options.

# Author: Oliver Osvald (oloosvald@gmail.com)
"""


# Requirements:
import argparse
import os
import subprocess as sp


def convert_file(file_list, file_path):
    """Convert files."""
    for file in file_list:

        try:
            os.chdir(file_path)
        except FileNotFoundError:
            print("Path doesn't exist.")
            break

        input_file = file + ".mp4"

        try:
            os.path.isfile(input_file)

            input_file_path = os.path.join(file_path, input_file)

            # Call ffmpeg command using a subprocess:
            command = "ffmpeg -i " + input_file_path + " -ab 32k -ac 2 -ar 44100 -vn " + file + ".wav"

            # -i input file path (e.g. Z:/.../... .mp4)
            # -ab audio bitrate (32k)
            # -ac audio channels (2 for L/R)
            # -ar audio resolution (44100 hz)
            # -vn dont use video
            # output file name and desired format (.wav)

            sp.call(command, shell=True)

        except FileNotFoundError:
            print("Couldn't locate file " + file + "!")
            break

        print("==============================================================")

        output_file = file + ".wav"
        output = "Success!"

        try:
            if os.path.isfile(output_file):
                print("Success! Video " + file + ".mp4 converted to .wav")
                return output
        except FileNotFoundError:
            print("Conversion unsuccessful. Check your inputs and try again.")
            break


if __name__ == '__main__':

    # Set up command line argument parser and define required arguments
    PARSER = argparse.ArgumentParser("Video to audio conversion script.")

    PARSER.add_argument("-input_file_names",
                        help="Provide a list of file names for conversion "
                        + "excluding extension (.mp4). Example: "
                        + "Video1 Video2 Video3",
                        type=str,
                        nargs='+',
                        )
    PARSER.add_argument("-file_path",
                        help="Enter input file folder path (optional). "
                        + "This will also be the output directory. "
                        + "If not provided, default is current directory.",
                        nargs='?',
                        type=str,
                        default=os.getcwd()
                        )

    ARGS = PARSER.parse_args()
    FILE_LIST = ARGS.input_file_names
    FILE_PATH = ARGS.file_path

    convert_file(file_list=FILE_LIST,
                 file_path=FILE_PATH)
