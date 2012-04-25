import sys, os
import opencv
from util import *
from opencv.cv import *
from opencv.highgui import *
from PIL import Image

def detectObjects(image):
  """Converts an image to grayscale and prints the locations of any 
     faces found"""
  grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
  cvCvtColor(image, grayscale, CV_BGR2GRAY)
  
  storage = cvCreateMemStorage(0)
  cvClearMemStorage(storage)
  cvEqualizeHist(grayscale, grayscale)

  cascade = cvLoadHaarClassifierCascade(
    'haarcascade_frontalface_default.xml',
    cvSize(1,1))

  faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2,
                             CV_HAAR_DO_CANNY_PRUNING, cvSize(50,50))

  positions = []

  if faces:
    positions = [(f.x, f.y, f.width, f.height) for f in faces]
  
  return positions

def find_faces_and_replace(in_file, replace_file, out_file):
  
  # Load image
  main_image = cvLoadImage(in_file);

  # Get the positions of the faces
  positions = detectObjects(main_image)  
  
  # Open main image
  image = Image.open(in_file)

  # Get the replace face
  face_replace = Image.open(replace_file)

  fs = out_file.rsplit("/", 1)
  
  # make sure directory exists
  ensure_dir(fs[0]+ "/")

  # Cover every face with the TROLL
  for face in positions:
        
    # Get size and position
    position_xy = (face[0],face[1])
    size = (face[2],face[3])

    # Resize overlay
    f = face_replace.resize(size)

    # Paste
    image.paste(f, position_xy, f)

  image.save(out_file)

if __name__ == "__main__":
  in_file = sys.argv[1]
  replace_file = sys.argv[2]
  out_file = sys.argv[3]
  find_faces_and_replace(in_file, replace_file, out_file)

