import argparse
import logging
from os import listdir
from os.path import join
import pathlib
from tqdm import tqdm
import shutil
import numpy as np


def process_timestamp(timestamp : str) -> str:
    timestamp_len = len(timestamp)
    timestamp_split = timestamp.split('.')
    for _ in range(20 - timestamp_len):
        timestamp_split[-1] = '0' + timestamp_split[-1]
    timestamp = timestamp_split[0] + '.' + timestamp_split[-1]
    return timestamp

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="get frames [x] seconds before timestamp [y]")
    parser.add_argument("-t", "--endtime", type=str, help="ending timestamp")
    parser.add_argument("-i", "--imgdir", type=str, help="image directory")
    parser.add_argument("-d", "--duration", type=float, help="duration in seconds")
    parser.add_argument("-o", "--outdir", default="/data/filtered_output", type=str, help="output directory")

    args = parser.parse_args()

    endtime = float(process_timestamp(str(args.endtime)))

    # file structure
    # -imgdir
    #     - topic1
    #         - img1
    #         - img2
    #         ...
    #     - topic2
    #         - img1
    #         - img2
    #         ...
    #     ...
    topic_list = [
        topic_dir for topic_dir in listdir(join(args.imgdir))
    ]
    # logging.debug(topic_list)
    for topic_dir in topic_list:
        img_list = [
            img_file for img_file in listdir(join(args.imgdir, topic_dir)) if img_file[-4:] == '.png'
        ]
        assert len(img_list) != 0
        # logging.debug(img_list)
        current_dir = join(args.imgdir, topic_dir)
        filtered_output_dir = join(args.outdir, args.imgdir.strip().split("/")[-1], topic_dir)
        pathlib.Path(filtered_output_dir).mkdir(parents=True, exist_ok=True)

        start_timestamp = endtime - args.duration
        for img in img_list:
            timestamp_str = process_timestamp(img.strip()[:-4])
            timestamp = float(timestamp_str)
            if timestamp <= endtime and timestamp >= start_timestamp:
                shutil.copyfile(join(current_dir, img), join(filtered_output_dir, f"{timestamp_str}.png"))
            
    
if __name__ == '__main__':
    main()
