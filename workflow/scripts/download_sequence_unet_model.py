#!/usr/bin/env python


import sys
import argparse

from sequence_unet import models


def get_options():
    description = 'Download Sequence Unet model'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('folder',
                        help='Output folder')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    # download a model
    try:
        model_path = models.download_trained_model("freq_classifier",
                root=options.folder, model_format="tf")
    except ConnectionError as e:
        sys.stderr.write('Could not download model through the FTP\n')
        sys.stderr.write(f'Exception was: {str(e)}\n')
        sys.stderr.write('Trying again through HTTPS\n')
        model_path = models.download_trained_model("freq_classifier",
                root=options.folder, model_format="tf",
                use_ftp=False)

