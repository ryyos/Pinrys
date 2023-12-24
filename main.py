from libs import Pinterest
from libs import logger
from argparse import ArgumentParser


def list_of_strings(arg):
    return arg.split(',')

def main():
    arg = ArgumentParser()
    arg.add_argument('--search', '--sc', type=list_of_strings, help='Enter what you want to search for, if there are many, separate them with commas (,)')
    arg.add_argument('--size', '--sz', type=int, default=250, help='Enter the amount you want to search for, maximum 250')
    arg = arg.parse_args()

    size = arg.size
    search = arg.search

    if size > 250:
        logger.warning("Maximum size is only 250")
        logger.warning("The request size will automatically be set to a maximum of 250")
        size = 250

    logger.info(f"Perform a search with a query {search}")
    for name in search:
        logger.info(f"perform a search by name {name.replace('_', ' ')}")

        pin = Pinterest()
        result = pin.main(name=name.replace('_', ' '), size=size)

        if result: logger.critical("The query you entered is invalid or not found!!")

if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.error("flag not passed")
        logger.warning("Please input the flag according to the conditions")
