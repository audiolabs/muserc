#!/usr/bin/env python2

import argparse
import os
from os.path import isfile, join
import sys

# Field names
experiences = {
    'pro': 'professional',
    'amateur': 'amateur'
}
expressions = {
    'p': 'piano',
    'm': 'mezzoforte',
    'f': 'forte'
}
vibratos = {
    'vib': 'True',
    'novib': 'False',
}


def __exit(error_msg):
    sys.exit(os.path.basename(__file__) + ": Error: " + error_msg)


def generate_yaml_string(midis, yaml, tunings, video):
    s = "- Samplerate: 48000\n"
    s += "  Sensorrate: 750\n"

    if video:
        s += "  Framerate: 2000\n"

    s += "  Pitches:\n"

    for midi in midis:
        s += "  - note: {0:s}\n".format(midi)

        if midi in tunings:
            ptr = tunings[midi]
            s += "    tunings:\n"

            experiences = ptr.keys()
            experiences.sort(reverse=True)

            for experience in experiences:
                s += "      - experience: {0:s}\n".format(experience)
                s += "        tunings:\n"

                ptr = tunings[midi][experience]

                for tuning in ptr:
                    s += "        - {0:s}\n".format(tuning)

        s += "    recordings:\n"

        expressions = yaml[midi].keys()
        expressions.sort(reverse=True)

        for expression in expressions:
            s += "    - expression: {0:s}\n".format(expression)

            vibratos = yaml[midi][expression].keys()
            vibratos.sort(reverse=True)

            for vibrato in vibratos:
                s += "      vibrato: {0:s}\n".format(vibrato)
                s += "      performer:\n"

                experiences = yaml[midi][expression][vibrato].keys()
                experiences.sort(reverse=True)

                for experience in experiences:
                    s += "      - experience: {0:s}\n".format(experience)
                    s += "        takes:\n"

                    takes = yaml[midi][expression][vibrato][experience]

                    for index, wav in takes.iteritems():
                        base = wav[0:-4]

                        s += "        - audio: {0:s}\n".format(wav)
                        s += "          sensor: {0:s}\n".format(
                            base + "_sensor.csv"
                        )

                        if video:
                            vid_str = "_compressed.mp4"
                            s += "          video: {0:s}\n".format(
                                base + vid_str
                            )

    return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate YAML file for given matched output.'
    )
    parser.add_argument(dest='input_directory', type=str)
    parser.add_argument(
        '-v',
        dest='video',
        action='store_true',
        default=False,
        help="Generate YAML for video output."
    )
    parser.add_argument(
        '-o',
        dest='output_file',
        action='store',
        type=str,
        default=None,
        help="Target YAML file, if none, result ist printed to stdout."
    )
    args = parser.parse_args()

    indir = args.input_directory
    out = args.output_file
    video = args.video

    if not os.path.exists(indir):
        __exit("Given input directory doesn't exist.")

    files = [f for f in os.listdir(indir) if isfile(join(indir, f))]
    wavs = [w for w in files if w[-4:] == ".wav"]

    yaml = {}
    tunings = {}

    for w in wavs:
        base = w[:-4]
        parts = base.split('_')

        experience = parts[0]
        midi = parts[1]
        expression = parts[2]

        if expression == "tune":
            if midi not in tunings.keys():
                tunings.update({midi: {}})
            ptr = tunings[midi]

            if experience not in ptr.keys():
                ptr.update({experience: []})
            ptr = ptr[experience]

            ptr += [ w ]

        else:
            vibrato = parts[3]
            take = parts[4] if len(parts) > 4 else 1

            if experience not in experiences.keys():
                __exit("Bad experience found: " + experience)
            if expression not in expressions.keys():
                __exit("Bad expression found: " + expression)
            if vibrato not in vibratos.keys():
                __exit("Bad vibrato found: " + vibrato)

            experience = experiences[experience]
            expression = expressions[expression]
            vibrato = vibratos[vibrato]

            if midi not in yaml.keys():
                yaml.update({midi: {}})
            ptr = yaml[midi]

            if expression not in ptr.keys():
                ptr.update({expression: {}})
            ptr = ptr[expression]

            if vibrato not in ptr.keys():
                ptr.update({vibrato: {}})
            ptr = ptr[vibrato]

            if experience not in ptr.keys():
                ptr.update({experience: {}})
            ptr = ptr[experience]

            index = len(ptr.keys()) + 1
            ptr.update({index: w})

    # print
    midis = yaml.keys()
    midis.sort()

    s = generate_yaml_string(midis, yaml, tunings, video)

    if out is not None:
        with open(out, "w") as stream:
            stream.write(s)
    else:
        print s,
