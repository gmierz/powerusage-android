import argparse

class AndroidParser():
    def __init__(self):
        return

    def parse_args(self):
        '''Read command line arguments and return options.'''
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--output',
            help='Location to output data being saved.',
            required=True
        )

        return parser.parse_args()