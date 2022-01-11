import numpy as np
from PIL import Image
import cv2,os,shutil

def create_rotated_images(img_small):

    if not os.path.exists('all_rotated_small_images'):
        os.makedirs('all_rotated_small_images')
    else:
        shutil.rmtree('all_rotated_small_images')
        os.makedirs('all_rotated_small_images')
    rot_vals = np.linspace(0,360,361)
    for angle in rot_vals:
        out = img_small.rotate(angle,expand=True)
        new_image = 'img_small_'+str(angle)+'_rotated.png'
        path = 'all_rotated_small_images/'+new_image
        out.save(path)

def find_matches(img_map, img_small):

    arr_h = np.asarray(img_map)
    arr_n = np.asarray(img_small)

    y_h, x_h = arr_h.shape[:2]
    y_n, x_n = arr_n.shape[:2]

    xstop = x_h - x_n + 1
    ystop = y_h - y_n + 1

    matches = []
    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            xmax = xmin + x_n
            ymax = ymin + y_n

            arr_s = arr_h[ymin:ymax, xmin:xmax]     # Extract subimage
            arr_t = (arr_s == arr_n)                # Create test matrix

            if arr_t.all():                         # Only consider exact matches
                matches.append((xmin,xmax,ymin,ymax))

            else:
                ymin +=1
    return matches

def demo(img_starmap_path,img_small_path):

    img_starmap = Image.open(img_starmap_path)
    img_small = Image.open(img_small_path)

    match = find_matches(img_starmap,img_small)
    result = []

    if len(match) == 0:
        create_rotated_images(img_small)
        counter = 0
        for img_check in sorted(os.listdir('all_rotated_small_images')):
            img_big_rot = Image.open('all_rotated_small_images/'+img_check)
            matched = find_matches(img_big_rot,img_small)
            counter+=1
            if len(matched)!= 0:
                result.append(matched)
        print(result[0][0])
        (xmin, xmax, ymin, ymax) = result[0][0]
    else:
        print(match)
        (xmin, xmax, ymin, ymax) = match[0]

    img = cv2.imread("StarMap.png")
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    cv2.imshow("Detected_Image", img)
    cv2.waitKey(0)

#demo('StarMap.png','Small_area.png')
demo('StarMap.png','Small_area_rotated.png')
