# -*- coding: utf-8 -*-
"""
Transcription of speech (audio .wav) to text.

Make sure you sign up for an IBM account and receive your API key and URL
before trying to use the IBM option.
Once obtained, please insert the credentials below into definitions of the
ibm_apikey and ibm_url variables within the recog_IBM() function definition.

@author: Oliver Osvald (email: oloosvald@gmail.com)
"""

# Requirements:
import argparse
import os
import pandas as pd

import speech_recognition as sr
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def recog_google(input_file, work_dir):
    """Use google API to recognise speech."""
    # Set up recogniser and process audio file into audio data:
    r = sr.Recognizer()

    with sr.AudioFile(input_file+".wav") as source:
        audio_data = r.record(source, offset=0)

    # Call Google API (uses default api key):
    text_google = r.recognize_google(audio_data)

    # Print results:
    try:
        print("text_from_speech_google: " + text_google)
        return text_google

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        raise

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition"
              + " service; {0}".format(e)
              )
        raise


def recog_IBM(input_file, work_dir):
    """Use IBM API to recognise speech."""
    ##########################################################################
    # Set up IBM credentials (have to sign up for an IBM account):
    ##########################################################################
    ibm_apikey = "7pbHP5MOctczpme24yLh0e4VUYl0o-C9z--Ikf4kXkaF"
    ##########################################################################
    ibm_url = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/3632ef59-4133-478b-aa61-b97e545b22c3"
    ##########################################################################

    # Need to use IBM authenticator with apikey and url:
    authenticator = IAMAuthenticator(ibm_apikey)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(ibm_url)

    # Recognize step using method from speech_to_text:
    with open(input_file + ".wav", 'rb') as source:
        sr_results = speech_to_text.recognize(audio=source,
                                              content_type='audio/wav'
                                              ).get_result()

    # Extract transcript only from the JSON data:
    text_ibm = sr_results["results"][0]["alternatives"][0]["transcript"]

    # Print results:
    try:
        print("text_from_speech_ibm: " + text_ibm)
        return text_ibm

    except sr.UnknownValueError:
        print("IBM could not understand audio")
        raise

    except sr.RequestError as e:
        print("IBM error; {0}".format(e))
        raise


def recog_sphinx(input_file, work_dir):
    """Use sphinx (offline) to recognise speech."""
    # Set up recogniser and process audio file into audio data:
    r = sr.Recognizer()

    with sr.AudioFile(input_file + ".wav") as source:
        audio_data = r.record(source, offset=0)

    # Call Sphinx:
    text_sphinx = r.recognize_sphinx(audio_data)

    # Print results:
    try:
        print("text_from_speech_sphinx: " + text_sphinx)
        return text_sphinx

    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        raise

    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        raise


def skill_match(skills, sr_text):
    """Match words from text on skills within provided skill list."""
    # Read csv of all skills (linkedin) and transform into a list:

    # Check if video string contains any of the skills:
    skills_matched = []

    for skill in skills:

        try:
            skill_lower = skill[0].lower()
        except Exception:
            skill_lower = "abcdefg"
            print("Issue with lower-casing skill: " + skill[0])
            raise

        if (skill in sr_text.split()) or (skill_lower in sr_text.split()):
            skills_matched.append(skill)

    return skills_matched


def run_recognition(sr_options,
                    work_dir,
                    input_files,
                    skills_matching,
                    skills_matching_file
                    ):
    """Combine APIs and write to file."""
    # Check if skills matching required - if yes, preload the skills list
    if skills_matching is True:
        skills_matching_file = skills_matching_file + ".csv"
        input_file_path = os.path.join(work_dir, skills_matching_file)

        try:
            skills = pd.read_csv(input_file_path,
                                 encoding="ISO-8859-1")
            skills = skills.values.tolist()
        except FileNotFoundError:
            print("Couldn't locate file " + skills_matching_file + "!")
            raise

    # Cycle through files and apply selected SR algorithm and SM:
    for input_file in input_files:

        # Amend file:
        Transcribe = open("Transcription.txt", "a")
        Transcribe.write("\n Transcription from file" + input_file + ":")

        # Use algorithms according to the sr_option:
        if "Google" in sr_options:
            text_google = recog_google(input_file)
            Transcribe.write("\n" + "text_from_google: " + text_google)

            # Check if skill match is required:
            if skills_matching is True:
                skills_matched = skill_match(work_dir, skills, text_google)
                Transcribe.write("\n Google transcription contains these "
                                 + "skills from the list: %s" % skills_matched)

        if "IBM" in sr_options:
            text_ibm = recog_IBM(input_file)
            Transcribe.write("\n" + "text_from_ibm: " + text_ibm)

            # Check if skill match is required:
            if skills_matching is True:
                skills_matched = skill_match(work_dir, skills, text_ibm)
                Transcribe.write("\n IBM transcription contains these skills "
                                 + "from the list: %s" % skills_matched)

        if "Sphinx" in sr_options:
            text_sphinx = recog_sphinx(input_file)
            Transcribe.write("\n" + "text_from_sphinx: " + text_sphinx)

            # Check if skill match is required:
            if skills_matching is True:
                skills_matched = skill_match(work_dir, skills, text_sphinx)
                Transcribe.write("\n Sphinx transcription contains these "
                                 + "skills from the list: %s" % skills_matched)

        Transcribe.close()


if __name__ == '__main__':

    # Set up command line argument parser and define required arguments
    PARSER = argparse.ArgumentParser("Speech recognition script.")

    PARSER.add_argument("-sr_options",
                        help="Choose from a list of SR algorithms:",
                        type=str,
                        nargs='+',
                        choices=["Google", "IBM", "Sphinx"],
                        )
    PARSER.add_argument("-input_audio_names",
                        help="Provide audio file names for transcription"
                        + " excluding extension (.wav). Example: "
                        + "-input_audio_names Audio1 Audio2 Audio3",
                        type=str,
                        nargs='+',
                        )
    PARSER.add_argument("-file_path",
                        help="Enter input file folder path (optional). "
                        + "This will also be the output directory. "
                        + "If not provided, defaults to current directory.",
                        nargs='?',
                        type=str,
                        default=os.getcwd()
                        )
    PARSER.add_argument("-skills_match",
                        help="Turn skill matching on/off (True/False).",
                        choices=[True, False],
                        type=bool,
                        nargs=1
                        )
    PARSER.add_argument("-skills_file_name",
                        help="Name of a csv file containing skills to match."
                        + " Must be a .csv file within -file_path folder.",
                        type=str,
                        nargs='?',
                        default='scraped_LI_skills.csv'
                        )

    ARGS = PARSER.parse_args()

    SR_OPTIONS = ARGS.sr_options
    FILE_PATH = ARGS.file_path
    FILE_LIST = ARGS.input_file_names
    SM_OPTION = ARGS.skills_match
    SM_file = ARGS.skills_file_name

    # run_recognition(sr_options=SR_OPTIONS,
    #                 work_dir=FILE_PATH,
    #                 input_files=FILE_LIST,
    #                 skills_matching=SM_OPTION,
    #                 skills_matching_file=SM_file
    #                 )
