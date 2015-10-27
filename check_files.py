import argparse
import yaml
import os


def parse_all_takes(yamlfile, datadir):
    stream = open(yamlfile, 'r')
    y = yaml.load(stream)

    datadir = datadir

    for pitch in y[0]['Pitches']:
        for rec in pitch['recordings']:
            for per in rec['performer']:
                for take in per['takes']:
                    yield (
                        pitch['note'],
                        rec['expression'],
                        rec['vibrato'],
                        per['experience'],
                        os.path.join(datadir, take['audio']),
                        os.path.join(datadir, take['sensor'])
                    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform pitch estimation for given sensor data file.')
    parser.add_argument(dest='yamlfile', type=str, default=None,
                        help='YAML File')
    parser.add_argument(dest='muserpath', type=str, default=None,
                        help='Path to MUSERC dataset')

    args = parser.parse_args()

    for (
        pitch,
        expression,
        has_vibrato,
        experience,
        faudio,
        fsensor
    ) in parse_all_takes(
        args.yamlfile,
        args.muserpath,
    ):

        if not os.path.exists(faudio):
            print "%s is missing" % faudio
        if not os.path.exists(fsensor):
            print "%s is missing" % fsensor
