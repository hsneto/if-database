import os
import re
import cv2
import json
from random import choice
from numpy import zeros, uint8


def load_datasets(**kwargs):
  """
  Load dataset info:
    - name
      - directory
      - data in multiple folders (bool)
      - emotions_marker:
        - neutral
        - angry 
        - contempt
        - disgust
        - fear
        - happy 
        - sad 
        - surprise
  """
  dt = kwargs.pop("dt", "./datasets.json")
  with open(dt) as f:
    data = json.load(f)

    return data


def load_keymap(**kwargs):
  """
  Load keymap controls
  """

  keys = kwargs.pop("keys", "./keymap.json")
  with open(keys) as f:
    data = json.load(f)

    return data


def load_options(**kwargs):
  """
  Load options
  """

  op = kwargs.pop("op", "./options.json")
  with open(op) as f:
    data = json.load(f)

    return data


def load_image(dataset, emotion, op=None):
  """
  Load image from dataset
  """
  data_dir = dataset["dir"]
  pattern = dataset["emotions"][emotion]

  if pattern is None:
    return

  files = []
  if dataset["multiple_folder"]:
    folders = [os.path.join(data_dir,f) for f in os.listdir(data_dir) if os.path.isdir(
      os.path.join(data_dir,f))]

    for folder in folders:
      files.extend([os.path.join(folder, f) for f in os.listdir(folder) if re.search(
        pattern, f)])
  
  else:
    folder = data_dir
    files.extend([os.path.join(folder, f) for f in os.listdir(folder) if re.search(
      pattern, f)])

  im = cv2.imread(choice(files))  

  if op["output_width"] is not None:
    im = resize(im, op["output_width"])

  return im


def resize(im, width):
  """
  Resize image according with the new width
  """

  (h, w) = im.shape[:2]
  r = width / float(w)
  dim = (width, int(h * r))

  return cv2.resize(im, dim, interpolation=cv2.INTER_AREA)


def init_im(keymap):
  """
  Load initial screen
  """

  im = zeros((280,240), dtype=uint8)
  y = 40
  x = 40

  cv2.rectangle(im, (20, 5), (220, 260), color=255, thickness=2)

  cv2.putText(im, "Commands:", 
    (30, y), cv2.FONT_HERSHEY_SIMPLEX, 
    0.75, 255, 2)

  y +=10

  for k in keymap.keys():
    msg = "{} : {}".format(keymap[k], k)
    y += 20

    cv2.putText(im, msg, 
    (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
    0.75, 255, 1)

  return im


def destroyWindows():
  """
  Destroy all windows, except Commands
  """

  try:
    cv2.destroyWindow("NEUTRAL | NEUTRO")
  except:
    pass
  try:
    cv2.destroyWindow("ANGRY | RAIVA")
  except:
    pass
  try:
    cv2.destroyWindow("CONTEMPT | DESPREZO")
  except:
    pass
  try:
    cv2.destroyWindow("DISGUST | NOJO")
  except:
    pass
  try:
    cv2.destroyWindow("FEAR | MEDO")
  except:
    pass
  try:
    cv2.destroyWindow("HAPPY | FELIZ")
  except:
    pass
  try:
    cv2.destroyWindow("SAD | TRISTE")
  except:
    pass
  try:
    cv2.destroyWindow("SURPRISE | SURPRESO")
  except:
    pass
