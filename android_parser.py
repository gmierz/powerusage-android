import argparse

from test_list import TESTS


class AndroidParser():
    def __init__(self):
        return

    def parse_args(self, require_tests=False):
        '''Read command line arguments and return options.'''
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--output',
            help='Location to output data being saved.',
            required=True
        )


        teststring = ' '.join(
            ['({}) {}'.format(str(i), name) for i, name in enumerate(TESTS)]
        )
        args = {
            'help': 'Test to run. '
                'These options are curently available: %s' % teststring,
        }
        if require_tests:
            args['required'] = True
        else:
            args['default'] = None

        parser.add_argument(
            '--test',
            **args
        )

        return parser.parse_args()