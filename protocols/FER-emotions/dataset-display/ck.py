import re
import os
import json

def get_json(dataset, delete_file=False):
  """
  Handle the multi-folders and labels in separete files
  """

  if os.path.exists("ck.json"):
    if delete_file:
      os.remove("ck.json")
      
    else:
      with open("ck.json") as f:
        data = json.load(f)
      return data

  data_dir = dataset["dir"]
  label_dir = dataset["label_dir"]

  re_topic = re.compile("Emotion_labels/Emotion")

  labels = {
    "0":[], "1":[], "2":[], "3":[],
    "4":[], "5":[], "6":[], "7":[]  
  }

  data = {
    "0":[], "1":[], "2":[], "3":[],
    "4":[], "5":[], "6":[], "7":[]  
  }

  # reading labels
  label_dir2 = []
  label_dir3 = []  
  label_dir1 = [os.path.join(label_dir, f) for f in os.listdir(label_dir)]

  for i in label_dir1:
    label_dir2.extend([os.path.join(i,f) for f in os.listdir(i)])
  for i in label_dir2:
    label_dir3.extend([os.path.join(i,f) for f in os.listdir(i)])

  for file in label_dir3:
    with open(file) as f:
      text = f.read()

      label = int(text.split(".")[0])

      if label == 0:
        labels["0"].append(file)

      if label == 1:
        labels["1"].append(file)

      if label == 2:
        labels["2"].append(file)

      if label == 3:
        labels["3"].append(file)

      if label == 4:
        labels["4"].append(file)

      if label == 5:
        labels["5"].append(file)

      if label == 6:
        labels["6"].append(file)

      if label == 7:
        labels["7"].append(file)

  # get filenames from known labels
  for i in labels:
    for file_dir in labels[i]:
      file_dir = re_topic.sub(r'extended-cohn-kanade-images/cohn-kanade-images', file_dir)
      file_dir = file_dir.rsplit('/', 1)[:-1][0]

      filename = os.path.join(file_dir, sorted(os.listdir(file_dir))[-1])
      neutral_file = os.path.join(file_dir, sorted(os.listdir(file_dir))[0])

      data["0"].append(neutral_file)
      data[i].append(filename)

  with open("ck.json", "w") as f:
    json.dump(data, f)

  return data
 

