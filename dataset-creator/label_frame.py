import cv2
import os
import re
import json
import argparse
from sys import exit
from collections import namedtuple

# argparse label
parser = argparse.ArgumentParser(
    description='Utility to label a single frame')
parser.add_argument(
    '--label', '-l', type=str, required=True, help='Label to the frame')
parser.add_argument(
    '--options', '-o', type=str, required=False, default="./options-label.json", help='options file')
args = parser.parse_args()

# pass label
label = args.label

# load options
with open(args.options) as f:
    data = json.load(f)

op = namedtuple("op", data.keys())(*data.values())

# create root folder 
if not os.path.exists(op.dst_dir):
    os.makedirs(op.dst_dir)

# create sub-folder
if not os.path.exists(os.path.join(op.dst_dir, label)):
    os.makedirs(os.path.join(op.dst_dir, label))

subjects_folders = [os.path.join(op.src_dir, label, f) 
                    for f in os.listdir(os.path.join(op.src_dir, label)) 
                    if f not in op.ignore_folders]

# get subjects folders
for subject in subjects_folders:

    # get filenames in subject folder
    img_dirs = [os.path.join(subject, f) for f in os.listdir(subject)]
    ii = 0

    while True:
        img = cv2.imread(img_dirs[ii])
        cv2.imshow(label, img)
        
        k = cv2.waitKey(1)
        
        # save image in op.dst_dir 
        if k == ord("s"):
            filename = re.sub(subject, os.path.join(op.dst_dir, label), 
                       img_dirs[ii])[:-11] + ".jpeg"
            cv2.imwrite(filename, img)
        
        # previous frame
        if k == ord("a"):
            ii -= 1
            if ii <= 0:
                ii = 0

        # next frame
        if k == ord("d"):
            ii += 1
            if ii >= len(img_dirs) - 1:
                ii = len(img_dirs) - 1

        # next subject
        if k == ord("n"):
            break

        # quit
        if k == ord("q"):
            exit(0)

cv2.destroyAllWindows()

