import json
from collections import namedtuple

def load_options(**kwargs):
  """
  Load options about display output and datasets.

  Args:
    - op = options.json file path

  Returns:
    - datasets: dataset informations
      - name
        - directory
        - is data in multiple folders (bool)
        - emotions_labels_marker:
          - neutral
          - angry 
          - contempt
          - disgust
          - fear
          - happy 
          - sad 
          - surprise

    - config: op object with display output configurations
      - output_width 
      - output_height
  """

  op = kwargs.pop("op", "./options.json")
  with open(op) as f:
    data = json.load(f)

  op = namedtuple("op", data.keys())(*data.values())

  config = namedtuple("op", dict(op.config).keys())(
    *dict(op.config).values())
  datasets = namedtuple("op", dict(op.datasets).keys())(
    *dict(op.datasets).values())

  return datasets, config


def load_keymap(**kwargs):
  """
  Load keymap controls

  Args:
    - keys = keymap.json file path

  Returns:
    - keymap_commands:
      - neutral 
      - angry   
      - contempt
      - disgust 
      - fear    
      - happy   
      - sad  
      - surprise
      - quit    
  """

  keys = kwargs.pop("keys", "./keymap.json")
  with open(keys) as f:
    data = json.load(f)

  return namedtuple("op", data.keys())(*data.values())


