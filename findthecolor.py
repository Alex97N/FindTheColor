# -*- coding: utf-8 -*-
"""FindTheColor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H-_KqLiqBKmxcT-eBcO7xBs9aO28Gmc0
"""

import numpy as np
import PIL
from PIL import Image
import csv
from csv import DictReader

colors_dictionary = [];
max_initial_difference = 2

with open('dataset/colors.csv', 'r') as read_obj:
  dict_reader = DictReader(read_obj)
  colors_dictionary_aux = list(dict_reader)
  colors_dictionary = colors_dictionary_aux

colors_dictionary_size = len(colors_dictionary);

# Open an Image
def open_image(path):
  newImage = Image.open(path)
  return newImage

# Save Image
def save_image(image, path):
  image.save(path, 'png')

# Create a new image with the given size
def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image

# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > height or j > width:
      return None

    # Get Pixel
    pixel = image.getpixel((j, i))
    return pixel

def find_pixel_color_in_csv_increasing_interval(i, j, max_difference, red, green, blue):
  #pixel_color_found = False;
  for k in range(colors_dictionary_size):
         if red >= int(colors_dictionary[k]['red']) - max_difference and red <= int(colors_dictionary[k]['red']) + max_difference and green >= int(colors_dictionary[k]['green']) - max_difference and green <= int(colors_dictionary[k]['green']) + max_difference and blue >= int(colors_dictionary[k]['blue']) - max_difference and blue <= int(colors_dictionary[k]['blue']) + max_difference:
           #print(colors_dictionary[k]['name'])     
           return colors_dictionary[k]['name'] 
           #pixel_color_found = True
           #break
  #if pixel_color_found == False:
  return find_pixel_color_in_csv_increasing_interval(i, j, max_difference + max_initial_difference, red, green, blue)

def find_pixel_color_in_csv_smallest_grade(i, j, red, green, blue):
  color_grades_for_pixel = ['none'] * colors_dictionary_size
  for k in range(colors_dictionary_size):
    color_grades_for_pixel[k] = abs(red - int(colors_dictionary[k]['red'])) + abs(green - int(colors_dictionary[k]['green'])) + abs(blue - int(colors_dictionary[k]['blue']))
  
  smallest_grade_for_pixel = 257;
  color_with_smallest_grade = 'none';
  for k in range(colors_dictionary_size):
    if (color_grades_for_pixel[k] < smallest_grade_for_pixel):
      color_with_smallest_grade = colors_dictionary[k]['name'] 
      smallest_grade_for_pixel = color_grades_for_pixel[k]
    
  #print(color_with_smallest_grade)
  return color_with_smallest_grade

def distance(r1, g1 ,b1, r2, g2, b2):
  r = (r1-r2)**2;
  g = (g1-g2)**2;
  b = (b1-b2)**2;
  rgbSum = r+g+b;
  return np.sqrt(rgbSum);

def find_pixel_color_Distance(red,green,blue):
  color_distance_for_pixel = ['none'] * colors_dictionary_size;
  for k in range(colors_dictionary_size):
    color_distance_for_pixel[k] = distance(int(red),int(green),int(blue),int(colors_dictionary[k]['red']),int(colors_dictionary[k]['green']),int(colors_dictionary[k]['blue']));
  smallest_distance = 450.0;
  color_with_smallest_distance = 'none';
  for k in range(colors_dictionary_size):
    if(color_distance_for_pixel[k] < smallest_distance):
      color_with_smallest_distance = colors_dictionary[k]['name'];
      smallest_distance = color_distance_for_pixel[k];
  
  return color_with_smallest_distance;

def find_rgb_of_color(color_name):

  k = int(find_nmb_of_color(color_name));

  red = colors_dictionary[k]['red'];
  green = colors_dictionary[k]['green'];
  blue = colors_dictionary[k]['blue'];
  
  rgb = '('+str(red)+','+str(green)+','+str(blue)+')';
  return rgb;

def find_nmb_of_color(color_name):
  for k in range(colors_dictionary_size):
    if( colors_dictionary[k]['name'] == str(color_name) ):
      return k;
  return 0;

def explain(color_found, red, green, blue):
  k = int(find_nmb_of_color(color_found))
  rc = colors_dictionary[k]['red'];
  gc = colors_dictionary[k]['green'];
  bc = colors_dictionary[k]['blue'];

  d = distance(int(rc),int(gc),int(bc),int(red),int(green),int(blue));
  return d;

def analyze_color_of_image_pixels(image):
  # Get size
  height = image.height
  width = image.width
  
  for i in range(height):
    for j in range(width):
      # Get Pixel
      pixel = get_pixel(image, i, j)

      # Get R, G, B values (This are int from 0 to 255)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      print("\nPixel", i, j, "with", "red", red, "green", green, "blue", blue, sep=" ")
      print("Increasing interval method:")
      print(find_pixel_color_in_csv_increasing_interval(i, j, max_initial_difference, red, green, blue));
      print("Smallest grade method:")
      print (find_pixel_color_in_csv_smallest_grade(i, j, red, green, blue))

image = open_image("image/image.png")
#image

def writeCSVofImage(iamge):
  with open('imageColors.csv','w', newline='') as csvOut:
    header = ['imageX','imageY','pixel RGB','Increasing Interval M','Smallest Grade M','Closest Color','Explanation(Distance)']
    w = csv.DictWriter(csvOut,fieldnames=header)
    w.writeheader();

    height = image.height
    width = image.width

    for i in range(height):
      for j in range(width):
        pixel = get_pixel(image, i, j)

        red =   pixel[0]
        green = pixel[1]
        blue =  pixel[2]

        iim = find_pixel_color_in_csv_increasing_interval(i, j, max_initial_difference, red, green, blue);
        sgm = find_pixel_color_in_csv_smallest_grade(i, j, red, green, blue);
        cc = find_pixel_color_Distance(red,green,blue);
        cc_explain = float(explain(cc,red,green,blue));

        w.writerow({
            'imageX' : i,
            'imageY' : j,
            'pixel RGB' : '('+str(red)+','+str(green)+','+str(blue)+')',
            'Increasing Interval M' : iim + str(find_rgb_of_color(str(iim))),
            'Smallest Grade M' : sgm + str(find_rgb_of_color(str(sgm))),
            'Closest Color' : cc + str(find_rgb_of_color(str(cc))),
            'Explanation(Distance)': "{:.3f}".format(cc_explain)
        })

# analyze_color_of_image_pixels(image)
writeCSVofImage(image)