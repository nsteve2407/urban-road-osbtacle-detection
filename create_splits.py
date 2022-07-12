import argparse
import glob
import os
import random

import numpy as np

from utils import get_module_logger


def split(source, destination):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    # Using a 90-9-1 train-val-test split
    files = os.listdir(source)
    random.shuffle(files)
    train_nums = int(len(files)*0.9)
    val_nums = int(len(files)*0.09)
    train_files = files[:train_nums]
    val_files = files[train_nums:(train_nums+val_nums)]
    test_files = files[(train_nums+val_nums):]
    for file in train_files:
        os.rename(os.path.join(source,file),os.path.join(destination,'train',file))
    for file in val_files:
        os.rename(os.path.join(source,file),os.path.join(destination,'val',file))
    for file in test_files:
        os.rename(os.path.join(source,file),os.path.join(destination,'test',file))
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--source', required=True,
                        help='source data directory')
    parser.add_argument('--destination', required=True,
                        help='destination data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.source, args.destination)