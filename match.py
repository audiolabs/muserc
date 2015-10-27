#!/usr/bin/env python2

import argparse
import numpy as np
import os
import os.path
from os.path import join, isfile
import soundfile as sf
import sys

outdir = join(os.path.dirname(__file__), 'output')


def __exit(error_msg):
    sys.exit(os.path.basename(__file__) + ": Error: " + error_msg)


def syncronize(raw_audio, raw_sync, verbose):
    """Truncate audio and obtain index for syncing sensor data."""
    sync_index = np.argmin(raw_sync)

    if verbose:
        print 'Syncing at index: ' + str(sync_index)

    d_audio = raw_audio[sync_index:]
    d_sync = raw_sync[sync_index:]

    return sync_index, d_audio, d_sync


def truncate(d_audio, d_sensor, verbose):
    """Truncate audio or sensor data, resulting in them having equal length."""

    sensor_l = len(d_sensor)
    sensor_l64 = sensor_l * 64
    d_l = len(d_audio)

    if verbose:
        print 'Sensor data length: ' + str(sensor_l)
        print 'Sensor data length * 64: ' + str(sensor_l64)
        print 'Audio data length: ' + str(d_l)

    if sensor_l64 > d_l:
        if verbose:
            print 'Truncating sensor data...'

        sensor_l = d_l / 64
        sensor_l64 = sensor_l * 64
        d_sensor = d_sensor[:sensor_l]

    if sensor_l64 < d_l:
        if verbose:
            print 'Truncating audio data...'

        d_audio = d_audio[:sensor_l64]

    return d_audio, d_sensor


def cut_parts(cut_list, d_audio, sensor, outdir, title, verbose):
    """Cut audio into subparts as indicated by supplied cutlist."""

    if verbose:
        print "Cutting into parts using cutlist from file..."

    names = cut_list[0]
    ins = cut_list[1]
    outs = cut_list[2]

    if names.size > 1:
        newnames = []

        for i, elem in enumerate(names):
            newnames.append(title + "_" + names[i])

        names = np.asarray(newnames)

        # ensure unique names

        for elem in names:
            if sum(names == elem) > 1:
                indices = np.where(names == elem)[0]

                count = 0
                for i in indices:
                    count += 1
                    names[i] = names[i] + "_" + str(count)
    else:
        names = [title + "_" + str(names)]
        ins = [int(ins)]
        outs = [int(outs)]

    cuts = zip(names, ins, outs)

    return cut(cuts, d_audio, sensor, outdir, verbose)


def cut(cuts, audio, sensor, outdir, verbose):
    """Cut audio into subparts as indicated by passed list of cuts."""

    # choose correct poti

    data_p1 = sensor[1]
    data_p2 = sensor[2]

    if data_p1.mean() > data_p2.mean():
        data_p = data_p1

        if verbose:
            print "Picked p1 for poti data."
    else:
        data_p = data_p2

        if verbose:
            print "Picked p2 for poti data."

    for n, i, o in cuts:

        d_audio = audio[i:o]

        i64 = i / 64
        o64 = o / 64

        sensor_t = sensor[0][i64:o64]
        sensor_p = data_p[i64:o64]
        sensor_x = sensor[3][i64:o64]
        sensor_y = sensor[4][i64:o64]
        sensor_z = sensor[5][i64:o64]

        truncate(d_audio, sensor_t, False)
        truncate(d_audio, sensor_p, False)
        truncate(d_audio, sensor_x, False)
        truncate(d_audio, sensor_y, False)
        truncate(d_audio, sensor_z, False)

        n_audio = np.arange(0, len(sensor_t)) * 64

        if verbose:
            print "Exporting subpart: %d - %d" % (i, o)

        name_audio = join(outdir, n + '.wav')
        name_sensor = join(outdir, n + '_sensor.csv')

        if not isfile(name_audio):
            sf_version = int(sf.__version__.replace(".", ""))

            if sf_version < 80:
                sf.write(d_audio, name_audio, samplerate=fs)
            else:
                sf.write(name_audio, d_audio, samplerate=fs)

        data = np.column_stack((sensor_t,
                                n_audio,
                                sensor_p,
                                sensor_x,
                                sensor_y,
                                sensor_z))

        np.savetxt(name_sensor,
                   data,
                   fmt=['%3.5f',
                        '%d',
                        '%d',
                        '%d',
                        '%d',
                        '%d'],
                   header='time,n_audio,fret_pos,acc_x,acc_y,acc_z',
                   delimiter=',',
                   comments='')

    return cuts


if __name__ == '__main__':

    # cmd line args
    parser = argparse.ArgumentParser(
        description='Match audio and data files from vibrato experiment.')
    parser.add_argument(dest='audio_file', type=str)
    parser.add_argument(dest='sync_file', type=str)
    parser.add_argument(dest='sensor_file', type=str)
    parser.add_argument(dest='output_title', type=str)
    parser.add_argument(dest='outdir', type=str)

    parser.add_argument('-c',
                        dest='cutlist_file',
                        action='store',
                        type=str,
                        default=None,
                        required=True,
                        help='File containing cut frames.')
    parser.add_argument('-v',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='Be verbose.')

    args = parser.parse_args()

    # audio file: contains audio data
    audio_file = args.audio_file

    # sync file: contains pulse syncronizing audio and sensor data
    sync_file = args.sync_file

    # sensor file: contains recorded data from sensor
    sensor_file = args.sensor_file

    # cutlist file: contains positions of recording subparts
    cutlist_file = args.cutlist_file

    title = args.output_title
    verbose = args.verbose

    if verbose:
        print "Starting matching with title: " + title
        print "Input audio file:   " + audio_file
        print "Input sync file:    " + sync_file
        print "Input sensor file:  " + sensor_file
        print "Input cutlist file: " + cutlist_file

    if not os.path.exists(audio_file):
        __exit("audio_file doesn't exist.")
    if not os.path.exists(sync_file):
        __exit("sync_file doesn't exist.")
    if not os.path.exists(sensor_file):
        __exit("sensor_file doesn't exist.")
    if not os.path.exists(cutlist_file):
        __exit("cutlist_file doesn't exist.")

    # create output directory if necessary

    outdir = args.outdir

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # read data

    # audio data
    raw_audio, fs = sf.read(audio_file, always_2d=False)

    # sync data
    raw_sync, fs = sf.read(sync_file, always_2d=False)

    # sensor data
    raw_sensor = np.hsplit(np.loadtxt(sensor_file), 6)
    sensor_p1 = np.ravel(raw_sensor[1])  # fretboard poti 1
    sensor_p2 = np.ravel(raw_sensor[2])  # fretboard poti 2
    sensor_x = np.ravel(raw_sensor[3])   # acceleration sensor x
    sensor_y = np.ravel(raw_sensor[4])   # acceleration sensor y
    sensor_z = np.ravel(raw_sensor[5])   # acceleration sensor z

    # syncronize audio and sensor according to sync pulse

    sync_index, d_audio, d_sync = syncronize(raw_audio, raw_sync, verbose)

    # truncate sensor or audio to obtain equal lengths

    d_audio, sensor_p1 = truncate(d_audio, sensor_p1, verbose)
    d_audio, sensor_p2 = truncate(d_audio, sensor_p2, False)
    d_audio, sensor_x = truncate(d_audio, sensor_x, False)
    d_audio, sensor_y = truncate(d_audio, sensor_y, False)
    d_audio, sensor_z = truncate(d_audio, sensor_z, False)

    d_sync = d_sync[:len(d_audio)]

    # create time vectors

    t = np.arange(0, len(d_audio))
    t = t * 1.0 / fs

    sensor_t = t[::64]

    # check lengths

    assert(len(d_audio) == len(d_sync)
           == len(t)
           == len(sensor_t) * 64
           == len(sensor_p1) * 64
           == len(sensor_p2) * 64
           == len(sensor_x) * 64
           == len(sensor_y) * 64
           == len(sensor_z) * 64)

    sensor = (sensor_t,
              sensor_p1,
              sensor_p2,
              sensor_x,
              sensor_y,
              sensor_z)

    # read cutlist from file
    cut_list = np.loadtxt(cutlist_file, comments='#', unpack=True,
                          dtype={'names': ['name', 'start', 'end'],
                                 'formats': ['|S15', np.float, np.float]})

    # cut data
    cut_list = cut_parts(
        cut_list,
        d_audio,
        sensor,
        outdir,
        title,
        verbose
    )
