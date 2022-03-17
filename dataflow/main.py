import logging

from retailapiloader import loader


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    loader.run()
