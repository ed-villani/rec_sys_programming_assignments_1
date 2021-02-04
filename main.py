import sys
import time

from data_readers.ratings import Ratings
from data_readers.targets import Targets
from models.entity_builder import EntityBuilder


def main(argv):
    print("Starting")
    start = time.time()
    ratings = Ratings(argv[0], 4)

    item_dict, user_dict, avg = EntityBuilder(ratings)

    targets = Targets(argv[1])
    targets.solve(item_dict, user_dict, avg)
    targets.to_csv("output.csv")
    end = time.time()
    print(f"Took: {round(end - start, 3)}s")


if __name__ == "__main__":
    main(sys.argv[1:])
