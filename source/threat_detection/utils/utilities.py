import os
import argparse
import yaml


def parse_args():
    parser = argparse.ArgumentParser(
        description='Provide path to config file.'
    )
    parser.add_argument(
        '--pyaml',
        type=str,
        default=['experiments', 'faster_rcnn_config.yaml'],
        help='Path to yaml config relative to base dir (project dir).'
    )
    return parser.parse_args()


def parse_yaml(path_yaml: str) -> dict:
    with open(os.path.join(os.getcwd(), *path_yaml), 'r') as f:
        configs = yaml.load(f.read(), Loader=yaml.Loader)
    return configs


def make_dir(path: str) -> None:
    """Creates a new directory at the given path, if it does not exist.

    :param path: Path identifies the directory to make.
    """
    if not os.path.isdir(path):
        os.mkdir(path)


def get_hparams_dict(hparams: dict) -> dict:
    """Creates an appropriate dictionary containing the hyper parameters in
    order to be logged to tensorboard.

    :param hparams:  Dictionary of hyper parameters
    :return: Parsed Dictionary of hyper parameters
    """
    pass