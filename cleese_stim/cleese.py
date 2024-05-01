#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CLEESE toolbox v2.0
jan 2022, Lara Kermarec <lara.git@kermarec.bzh> for CNRS

External API for CLEESE
'''

import tomli
import os
import shutil
import time
import sys


def log(*args):
    print(*args, file=sys.stderr)


def process_file(engine, filename, config_file, **kwargs):
    data, attr = engine.load_file(filename)
    return process_data(engine, data, config_file, **attr, **kwargs)


def process_data(engine, data, config_file, **kwargs):
    conf = load_config(config_file)
    return engine.process(data, conf, **kwargs)


def generate_stimuli(engine, filename, config_file, **kwargs):
    conf = load_config(config_file)

    # Check all the needed user-provided config values are here
    try:
        OUT_PATH = conf["main"]["outPath"]
    except KeyError as e:
        log("ERROR: missing config element: {}".format(e))
        return

    # generate experiment name and folder
    main = conf["main"]
    if "generateExpFolder" in main and main["generateExpFolder"]:
        base_dir = os.path.join(OUT_PATH, "[{}]_{}".format(
                engine.name(), time.strftime("%Y-%m-%d_%H-%M-%S")))
    else:
        base_dir = OUT_PATH

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    conf["main"]["expBaseDir"] = base_dir
    conf["main"]["filename"] = filename

    # copy original data to experiment folder
    shutil.copy2(filename, base_dir)

    # copy configuration file to experiment folder
    shutil.copy2(config_file, base_dir)

    data, attr = engine.load_file(filename)
    return engine.generate_stimuli(data, conf, **attr, **kwargs)


def load_config(filename):
    conf = None
    with open(filename, "rb") as f:
        try:
            conf = tomli.load(f)
        except tomli.TOMLDecodeError as e:
            log("Could not load configuration from '{}':\n  {}"
                .format(filename, e))
    return conf


if __name__ == "__main__":
    config_file = "./cleese-vanilla.toml"
    load_config(config_file)
