import os
import argparse
import yaml


def parse_args() -> str:
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
