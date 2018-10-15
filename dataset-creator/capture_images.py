import re
import os
import sys
import cv2
import json
import utils
import shutil
import argparse
import numpy as np
from is_msgs.image_pb2 import Image
from datetime import datetime as DT
from collections import defaultdict
from is_wire.core import Channel, Subscription, Message, Logger


def get_id(topic):
  match_id = re.compile(r'CameraGateway.(\d+).Frame')
  match = match_id.search(msg.topic)
  if not match:
    return None
  else:
    return int(match.group(1))


def place_images(output_image, images):
  w, h = images[0].shape[1], images[0].shape[0]
  output_image[0:h, 0:w, :] = images[0]
  output_image[0:h, w:2 * w, :] = images[1]
  output_image[h:2 * h, 0:w, :] = images[2]
  output_image[h:2 * h, w:2 * w, :] = images[3]


def draw_info_bar(image, text, x, y,
                  background_color=(0, 0, 0),
                  text_color=(255, 255, 255),
                  draw_circle=False):
  
  fontFace = cv2.FONT_HERSHEY_DUPLEX
  fontScale = 1.0
  thickness = 1
  ((text_width, text_height), _) = cv2.getTextSize(
    text=text, fontFace=fontFace, fontScale=fontScale, thickness=thickness)
  
  cv2.rectangle(
    image,
    pt1=(0, y - text_height),
    pt2=(x + text_width, y),
    color=background_color,
    thickness=cv2.FILLED)

  if draw_circle:
    cv2.circle(
      image,
      center=(int(x / 2), int(y - text_height / 2)),
      radius=int(text_height / 3),
      color=(0, 0, 255),
      thickness=cv2.FILLED)
  
  cv2.putText(
    image,
    text=text,
    org=(x, y),
    fontFace=fontFace,
    fontScale=fontScale,
    color=text_color,
    thickness=thickness)

parser = argparse.ArgumentParser(
    description='Utility to capture a sequence of images a multiple cameras or webcam'
)
parser.add_argument(
    '--exp', '-e', type=str, required=True, help='Experiment tag')
parser.add_argument(
    '--subject', '-s', type=str, required=True, help='ID to identity subject')
parser.add_argument(
    '--label', '-l', type=str, required=True, help='ID to identity label category')
parser.add_argument(
    '--foldername', '-f', type=str, required=False, help='Add an extra folder to organize the data')
parser.add_argument(
    '--device', '-d', type=str, required=False, default="cameras", help='Device use to collect data. It can be either "webcam" or "cameras"')    
args = parser.parse_args()

# pass args
exp = args.exp
subject_id = args.subject
label_id = args.label
device = args.device

# load camera info --> options.json
op, cam = utils.load_options(device)
# load experiment labels --> labels.json
labels = utils.load_labels(exp)

log = Logger(name="Capture")

# get folder to store the collected data
if exp == "emotions":
  folder = op.folder_emotions
elif exp == "signals":
  folder = op.folder_signals
elif exp == "gestures":
  folder = op.folder_gestures
elif exp == "adl":
  folder = op.folder_adl
elif exp == "falls":
  folder = op.folder_falls
else:
  log.error("Invalid experiment!")
  sys.exit(-1)

# add new folder
if args.foldername is not None:
  folder = os.path.join(folder, args.foldername)

# get folder from each possible label
labels_folders = utils.get_label_folder(folder, labels)

# create a folder to store timestamps
timestamps_folder = os.path.join(labels_folders[label_id], "timestamps")
if not os.path.exists(timestamps_folder):
  os.makedirs(timestamps_folder)

sequence = "{:03d}".format(int(subject_id))
sequence_folder = os.path.join(labels_folders[label_id], sequence)

if os.path.exists(sequence_folder):
  log.warn(
      'Path to SUBJECT_ID={} LABEL={} ({}) already exists.\n \
      Would you like to proceed? All data will be deleted! [y/n]',
      subject_id, label_id, labels[label_id])
  key = input()
  if key == 'y':
      shutil.rmtree(sequence_folder)
  elif key == 'n':
      sys.exit(0)
  else:
      log.critical('Invalid command \'{}\', exiting.', key)
      sys.exit(-1)

os.makedirs(sequence_folder)

channel = Channel(op.broker_uri)
subscription = Subscription(channel)

if device == "webcam":
  # subscribe to one camera
  subscription.subscribe('CameraGateway.{}.Frame'.format(cam.id))

elif device == "cameras":
  # subscribe to multiple cameras
  for c in cam:
    subscription.subscribe('CameraGateway.{}.Frame'.format(c.id))
  
  # get display image size
  size = (2 * cam[0].config["image"]["resolution"]["height"],
          2 * cam[0].config["image"]["resolution"]["width"], 3)
  # create empty image do display
  full_image = np.zeros(size, dtype=np.uint8)

else:
  log.error("Invalid device option")
  sys.exit(-1)

images_data = {}
current_timestamps = {}
timestamps = defaultdict(list)
images = {}
n_sample = 0
display_rate = 2
start_save = False
sequence_saved = False
info_bar_text = "SUBJECT_ID: {} LABEL: {} ({})".format(
  subject_id, label_id, labels[label_id].upper())

while True:
  msg = channel.consume()
  topic_id = get_id(msg.topic)
  if topic_id is None:
    continue

  pb_image = msg.unpack(Image)
  if pb_image is None:
    continue
  data = np.frombuffer(pb_image.data, dtype=np.uint8)
  images_data[topic_id] = data
  current_timestamps[topic_id] = DT.utcfromtimestamp(
    msg.created_at).isoformat()

  if device == "webcam":
    # save images
    if start_save and not sequence_saved:
      filename = os.path.join(sequence_folder, "{:02d}_{:03d}_{:08d}.jpeg".format(
                              int(label_id), int(subject_id), n_sample))
      with open(filename, "wb") as f:
        f.write(images_data[topic_id])

      timestamps[topic_id].append(current_timestamps[topic_id])
      n_sample += 1
      log.info("Sample {} saves", n_sample)

    # display images
    if n_sample % display_rate == 0:
      display_image = cv2.imdecode(data, cv2.IMREAD_COLOR)
      draw_info_bar(display_image, info_bar_text, 50, 50, 
                      draw_circle=start_save and not sequence_saved)
      cv2.imshow("", display_image)

      current_timestamps = {}

    key = cv2.waitKey(1)
    if key == ord("s"):
      if start_save is False:
        start_save = True
      elif not sequence_saved:
        timestamps_filename = os.path.join(timestamps_folder, '{}_timestamps.json'.format(sequence))
        with open(timestamps_filename, 'w') as f:
          json.dump(timestamps, f, indent=2, sort_keys=True)
        sequence_saved = True
        
    if key == ord("q"):
      if not start_save or sequence_saved:
        break

  elif device == "cameras":
    if len(images_data) == len(cam):
      # save images
      if start_save and not sequence_saved:
        for c in cam:
          filename = os.path.join(sequence_folder, "{:02d}_{:03d}_c{:01d}_{:08d}.jpeg".format(
                              int(label_id), int(subject_id), c.id, n_sample))
          with open(filename, "wb") as f:
            f.write(images_data[c.id])

          timestamps[c.id].append(current_timestamps[c.id])
        n_sample += 1
        log.info('Sample {} saved', n_sample)

      # display images
      if n_sample % display_rate == 0:
        images = [
          cv2.imdecode(data, cv2.IMREAD_COLOR)
          for _, data in images_data.items()
        ]
        place_images(full_image, images)
        display_image = cv2.resize(full_image, (0, 0), fx=0.5, fy=0.5)
        draw_info_bar(display_image, info_bar_text, 50, 50, 
                      draw_circle=start_save and not sequence_saved)
        cv2.imshow("", display_image)

      images_data = {}
      current_timestamps = {}
    
      key = cv2.waitKey(1)
      if key == ord("s"):
        if start_save is False:
          start_save = True
        elif not sequence_saved:
          timestamps_filename = os.path.join(timestamps_folder, '{}_timestamps.json'.format(sequence))
          with open(timestamps_filename, 'w') as f:
            json.dump(timestamps, f, indent=2, sort_keys=True)
          sequence_saved = True

      if key == ord("q"):
        if not start_save or sequence_saved:
          break

log.info("Exiting")