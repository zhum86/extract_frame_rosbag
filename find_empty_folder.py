import argparse
from os import listdir
from os.path import join, isdir
import logging

def main():
    logging.basicConfig(level=logging.WARN)

    parser = argparse.ArgumentParser(description="Look for empty folder")
    parser.add_argument("-d", "--dir", default="/data/filtered_output", type=str, help="directory")

    args = parser.parse_args()

    bag_list = [
        bag_dir for bag_dir in listdir(args.dir) if isdir(bag_dir)
    ]

    for bag in bag_list:
        current_dir = join(args.dir, bag)
        topic_list = [
            topic_dir for topic_dir in listdir(current_dir) if isdir(topic_dir)
        ]
        for topic in topic_list:
            current_dir = join(args.dir, bag, topic)
            img_list = [
                img_file for img_file in listdir(current_dir)
            ]
            if len(img_list) == 0:
                logging.warn(f'Emty directory: {current_dir}')
    

if __name__ == '__main__':
    main()