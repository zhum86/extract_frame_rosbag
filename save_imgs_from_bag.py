import rosbag
# from cv_bridge import CvBridge
import cv2

import argparse
import logging
from os import listdir
from os.path import join
import pathlib
from tqdm import tqdm
import numpy as np

# topics:      /dashcam/image_raw                  sensor_msgs/Image
#              /usb_cam/image_raw                  sensor_msgs/Image
#              /zed_node/left/image_rect_color     sensor_msgs/Image
#              /zed_node/right/image_rect_color    sensor_msgs/Image

# file structure
# - outdir
#     - bag1
#         - topic1
#             - img1
#             - img2
#             ...
#         - topic2
#             - img1
#             - img2
#             ...
#         ...
#     - bag2
#         - topic1
#             - img1
#             - img2
#             ...
#         - topic2
#             - img1
#             - img2
#             ...
#         ...
#     ...

color_encoding_no_cvt = ['/zed_node/left/image_rect_color', '/zed_node/right/image_rect_color']


def main(): 
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("-b", "--bagdir", type=str, help="Input ROS bag directory.")
    parser.add_argument("-t", "--imgtopic", type=str, nargs="+", help="Image topic to extract.")
    parser.add_argument("-o", "--outdir", type=str, help="Directory of output images.")

    args = parser.parse_args()

    bag_list = [
            bag_file for bag_file in listdir(args.bagdir) if bag_file[-4:] == '.bag'
        ]
    logging.debug(bag_list)

    logging.debug(args.imgtopic)
    
    topic_dir_lut = {}
    for topic in args.imgtopic:
        topic_dir = ""
        topic_split = topic.strip().split("/")
        for t in topic_split:
            if not t:
                continue
            topic_dir += t
            topic_dir += "-"
        topic_dir = topic_dir[:-1] 
        logging.debug(topic_dir)
        topic_dir_lut.update({topic:topic_dir}) 
        for bag_file in bag_list:
            pathlib.Path(join(args.outdir, bag_file, topic_dir)).mkdir(parents=True, exist_ok=True)

    for bag_file in tqdm(bag_list, desc=f"Extracting bag {bag_file}"):
        bag = rosbag.Bag(join(args.bagdir, bag_file), "r")
        for topic, msg, timestamp in bag.read_messages(topics=args.imgtopic):
            img = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
            output_file_dir = join(args.outdir, bag_file, topic_dir_lut[topic], f'{timestamp.secs}.{timestamp.nsecs:>09}.png')
            if topic not in color_encoding_no_cvt:
                cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                cv_img = img
            cv2.imwrite(output_file_dir, cv_img)


if __name__ == '__main__':
    main()
