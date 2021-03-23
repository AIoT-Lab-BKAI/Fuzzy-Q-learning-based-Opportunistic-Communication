import argparse
import json
import math
import random
from dataclasses import dataclass, field


def getConfig():
    """
    Get config
    Sử dụng khi thay đổi các tham số đầu vào
    """
    # Get config path from user
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", help="Path to config.json")
    args = parser.parse_args()

    # Load config
    with open(args.config_path, "r") as f:
        config = json.load(f)

    return config


def getNext(x):
    """
    Sinh thời gian theo phân phối Poisson 
    """
    return -math.log(1.0 - random.random()) / x


@dataclass(order=True)
class PrioritizedItem:
    priority: (float, int)
    item: object = field()
