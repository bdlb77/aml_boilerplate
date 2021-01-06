"""
Just a placeholder for a step
"""
import os
import logging
import argparse


def train():
    logging.basicConfig(level=logging.INFO)

    log: logging.Logger = logging.getLogger(__name__)

    log.info("Train Step")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--root_dir', help="datastore for input data. This is the root dir", required=True)
    parser.add_argument(
        '--data_dir', help="directory containing data", required=True)
    args, _ = parser.parse_known_args()
    data_path = os.path.join(args.input_data, args.data_dir)

    if not os.path.exists(data_path):
        raise OSError("Folder %s does not exist in path %s" %
                      args.data_dir, data_path)

    for root, _, files in os.walk(data_path):
        for filename in files:
            try:
                with open(os.path.join(root, filename), "r") as f:
                    print(f.read())
            except (OSError, Exception) as err:
                log.error("Unable to process file: %s Err: %s",
                          filename, str(err), exc_info=True)


if __name__ == '__main__':
    train()
