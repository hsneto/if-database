import os
import re
import cv2
import ck
import utils
from random import choice
from numpy import zeros, uint8

delete_ck_file = True

def do_not_delete_ck_file():
  global delete_ck_file
  delete_ck_file = False

def command_screen(keymap):
  """
  Load initial screen with commands
  """

  im = zeros((280,240), dtype=uint8)
  y = 40
  x = 40

  cv2.rectangle(im, (20, 5), (220, 260), color=255, thickness=2)

  cv2.putText(im, "Commands:", 
    (30, y), cv2.FONT_HERSHEY_SIMPLEX, 
    0.75, 255, 2)

  y +=10

  for i, k in enumerate(keymap._fields):
    msg = "{} : {}".format(k, keymap[i])
    y += 20

    cv2.putText(im, msg, 
    (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
    0.75, 255, 1)

  return im


def destroyWindows():
  """
  Destroy all windows, except Command Screen
  """

  try:
    cv2.destroyWindow("NEUTRAL")
  except:
    pass
  try:
    cv2.destroyWindow("ANGRY")
  except:
    pass
  try:
    cv2.destroyWindow("CONTEMPT")
  except:
    pass
  try:
    cv2.destroyWindow("DISGUST")
  except:
    pass
  try:
    cv2.destroyWindow("FEAR")
  except:
    pass
  try:
    cv2.destroyWindow("HAPPY")
  except:
    pass
  try:
    cv2.destroyWindow("SAD")
  except:
    pass
  try:
    cv2.destroyWindow("SURPRISE")
  except:
    pass


def resize(im, config):
  """
  Resize image according with the new width or height
  """

  width = config.output_width 
  height = config.output_height
  (h, w) = im.shape[:2]

  if width is None and height is None:
    return im

  elif height is None:
    r = width / float(w)
    dim = (width, int(h * r))

  elif width is None:
    r = height / float(h)
    dim = (int(w * r), height)

  else:
    dim = (width, height)

  return cv2.resize(im, dim, interpolation=cv2.INTER_AREA)


def get_image(dataset, emotion, config=None):
  """
  Load image from dataset
  """

  data_dir = dataset["dir"]
  pattern = dataset["emotions"][emotion]

  if pattern is None:
    return

  files = []

  if dataset["is_ck"] is True:
    all_files = ck.get_json(dataset, delete_ck_file)

    files = all_files[pattern]
    do_not_delete_ck_file()

  elif dataset["multiple_folder"]:
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

  return resize(im, config)


def show_image(dataset, emotion, config=None):
  """
  Display an image from an emotion given a dataset
  """

  im = get_image(dataset, emotion, config)
    
  if im is not None:
    destroyWindows()
    cv2.imshow(emotion.upper(), im)

dt, config = utils.load_options()
keys = utils.load_keymap()

# show command screen
cv2.imshow("COMMANDS", command_screen(keys))

while True:
  k = cv2.waitKey(1)

  if k == ord(keys.neutral):
    show_image(choice(dt), "neutral", config)

  elif k == ord(keys.angry):
    show_image(choice(dt), "angry", config)

  elif k == ord(keys.contempt):
    # because contempt is only in ck+ dataset
    show_image(dt.ck, "contempt", config)

  elif k == ord(keys.disgust):
    show_image(choice(dt), "disgust", config)

  elif k == ord(keys.fear):
    show_image(choice(dt), "fear", config)

  elif k == ord(keys.happy):
    show_image(choice(dt), "happy", config)

  elif k == ord(keys.sad):
    show_image(choice(dt), "sad", config)

  elif k == ord(keys.surprise):
    show_image(choice(dt), "surprise", config)

  elif k == ord(keys.quit):
    break

cv2.destroyAllWindows()


