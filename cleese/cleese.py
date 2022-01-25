import enum
import tomli
import os
import shutil
import time

from cleese import engines


def process_file(engine, filename, config_file, **kwargs):
    data, attr = engine.load_file(filename)
    return process_data(engine, data, config_file, **attr, **kwargs)


def process_data(engine, data, config_file, **kwargs):
    conf = load_config(config_file)
    return engine.process(data, conf, **kwargs)


def generate_stimuli(engine, filename, config_file, **kwargs):
    conf = load_config(config_file)

    if "main" not in conf:
        print("Error: missing [main] table in {}".format(config_file))
        return

    main = conf["main"]

    # generate experiment name and folder
    if "generateExpFolder" in main and main["generateExpFolder"]:
        if "outPath" not in main:
            print("ERROR: [main] outPath missing while generateExpFolder is true in {}".format(config_file))
            return

        base_dir = os.path.join(main["outPath"], "[{}]_{}".format(
                engine.name(), time.strftime("%Y-%m-%d_%H-%M-%S")))
    else:
        base_dir = main["outPath"]

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    conf["main"]["expBaseDir"] = base_dir
    conf["main"]["filename"] = filename

    # copy base audio to experiment folder
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
            print("Could not load configuration from '{}':\n  {}"
                  .format(filename, e))
    return conf


if __name__ == "__main__":
    config_file = "./cleese-vanilla.toml"
    load_config(config_file)
