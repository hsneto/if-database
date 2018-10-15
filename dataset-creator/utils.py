import os
import json
from collections import namedtuple

def load_options(**kwargs):
  """
  Load options about display output and datasets.

  Args:
    - op = options.json file path

  Returns:
    - op: options informations
     - broker_uri
     - folder_emotions
     - folder_signals

    - camera: camera informations
      - id
      - width 
      - height
  """

  op = kwargs.pop("op", "./options.json")
  with open(op) as f:
    data = json.load(f)

  op = namedtuple("op", data.keys())(*data.values())

  camera = namedtuple("op", dict(op.camera).keys())(
    *dict(op.camera).values())

  return op, camera


def load_labels(exp, **kwargs):
  """
  Load options about display output and datasets.

  Args:
    - exp: load labels from one of the experiments below:
      - "emotions"
      - "signals" 

    - op = labels.json file path

  Returns:
    - labels: labels codes from each category
  """

  op = kwargs.pop("op", "./labels.json")
  with open(op) as f:
    data = json.load(f)

  return data[exp]


def get_label_folder(folder, labels):
  """
  Get respective folder from each label

  Args:
   - folder
   - labels

  Returns:
   - folders: list of folders from each label
  """

  folders = {}

  if not os.path.exists(folder):
    os.makedirs(folder)

  for i in labels:
    label_folder = os.path.join(folder, labels[i])

    if not os.path.exists(label_folder):
      os.makedirs(label_folder)

    folders[i] = label_folder
  
  return folders

