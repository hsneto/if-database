import cv2
import utils
from random import choice

dt = utils.load_datasets()
op = utils.load_options()
keys = utils.load_keymap()

datasets = list(dt.keys())
emotions = list(dt[datasets[0]]["emotions"].keys())

cv2.imshow("COMMANDS | COMANDOS", utils.init_im(keys))

while True:
  k = cv2.waitKey(1)

  if k == ord(keys["neutral"]):

    im = utils.load_image(dt[choice(datasets)], "neutral", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("NEUTRAL | NEUTRO", im)

  elif k == ord(keys["angry"]):
    
    im = utils.load_image(dt[choice(datasets)], "angry", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("ANGRY | RAIVA", im)

  elif k == ord(keys["contempt"]):
    
    im = utils.load_image(dt[choice(datasets)], "contempt", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("CONTEMPT | DESPREZO", im)

  elif k == ord(keys["disgust"]):
    
    im = utils.load_image(dt[choice(datasets)], "disgust", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("DISGUST | NOJO", im)

  elif k == ord(keys["fear"]):
    
    im = utils.load_image(dt[choice(datasets)], "fear", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("FEAR | MEDO", im)

  elif k == ord(keys["happy"]):
    
    im = utils.load_image(dt[choice(datasets)], "happy", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("HAPPY | FELIZ", im)

  elif k == ord(keys["sad"]):
    
    im = utils.load_image(dt[choice(datasets)], "sad", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("SAD | TRISTE", im)

  elif k == ord(keys["surprise"]):
    
    im = utils.load_image(dt[choice(datasets)], "surprise", op)
    utils.destroyWindows()

    if im is not None:  
      cv2.imshow("SURPRISE | SURPRESO", im)

  elif k == ord(keys["quit"]):
    break

cv2.destroyAllWindows()


