import os

import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tqdm
from random import randint


def cropping(img_root, csv_path, output_path):
    """

    :param img_root: root to the images (positive included)
    :param csv_path: path to the csv generated from the xml annotations
    :param output_path: path to output the images
    """
    os.makedirs(output_path, exist_ok=True)
    df = pd.read_csv(csv_path)
    img_names = sorted(list(set(df['img_name'])))
    for name in tqdm.tqdm(img_names, 'Creating cropped objects'):
        objects = df.loc[df['img_name'] == name]
        image = cv2.imread(os.path.join(img_root, name))
        for index, row in objects.iterrows():
            os.makedirs(os.path.join(output_path, row['object_type']), exist_ok=True)

            crop_img = image[int(row['ymin']):int(row['ymax']), int(row['xmin']):int(row['xmax'])]
            im_name = name.split('.')[0] + '_' + str(index) + '.jpg'
            cv2.imwrite(os.path.join(output_path, row['object_type'], im_name), crop_img)


# TODO: Fine tune segmentation
def segmentation(img_path):
    """
    This is just a proof of concept function for the segmentation, should be refined
    Segmentation type based on: https://medium.com/srm-mic/color-segmentation-using-opencv-93efa7ac93e2
    :param img_path: path to the image
    """
    img = cv2.imread(img_path)
    print(img.shape)
    blur = cv2.blur(np.array(img), (5, 5))
    blur0 = cv2.medianBlur(blur, 5)
    blur1 = cv2.GaussianBlur(blur0, (5, 5), 0)
    blur2 = cv2.bilateralFilter(blur1, 9, 75, 75)
    hsv = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    low_blue = np.array([55, 0, 0])
    high_blue = np.array([118, 255, 255])
    mask = cv2.inRange(hsv, low_blue, high_blue)
    result = cv2.bitwise_and(np.array(img), np.array(img), mask=mask)
    return result, mask


def remove_small(base_dir, object_type, min_dim):
    """
    Remove the unnecessarily small images
    :param min_dim:
    :param base_dir: Base dir of the segmentation, like the cropped "Gun" folder
    :param object_type: Specifying the type of the object
    """
    images = os.listdir(os.path.join(base_dir, object_type))
    for image in tqdm.tqdm(images, 'Removing small images'):
        img_path = os.path.join(base_dir, object_type, image)
        img = cv2.imread(img_path)
        if min_dim[0] > img.shape[0] or min_dim[1] > img.shape[1]:
            os.remove(img_path)


def get_random_image(path_to_negatives):
    images = os.listdir(path_to_negatives)
    return images[randint(0, 10)]


def compare_results_run(base_dir, object_type, path_to_negatives):
    """
    Run the different segmentations and compare them
    :param path_to_negatives: path to the negative images that need augmentation
    :param base_dir: Base dir of the segmentation, like the cropped "Gun" folder
    :param object_type: Specifying the type of the object
    """
    images = os.listdir(os.path.join(base_dir, object_type))
    neg_images = os.listdir(path_to_negatives)
    # TODO: Find the boundaries of the luggage
    for image in images:
        img_path = os.path.join(base_dir, object_type, image)
        # TODO: Add rescaling to the object
        # TODO: Handle bounding box and annotation generation
        result, mask = segmentation(img_path)
        inverse_mask = 255 - mask
        random_img = cv2.imread(os.path.join(path_to_negatives, neg_images[randint(0, 10)]))
        width_res, height_res, _ = result.shape
        # TODO: FIND BETTER POSITIONING
        region_of_interest = cv2.bitwise_and(np.array( random_img[500:500 + width_res, 500:500 + height_res]), np.array( random_img[500:500 + width_res, 500:500 + height_res]), mask=inverse_mask)
        random_img[500:500 + width_res, 500:500 + height_res] = (region_of_interest + result)
        cv2.imshow('Test seg1', random_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


root_path_pos = 'Path/To/Datasets/SIXRay/tar/Positive'
root_path_neg = 'Path/To/Datasets/SIXRay/tar/Negative_reduced'
path_to_csv = 'Path/To/Datasets/SIXRay/gt_data.csv'
out_dir = 'Path/To/Datasets/SIXRay/output'
# cropping(root_path, path_to_csv, out_dir)
remove_small(out_dir, 'Gun', (99, 50))
compare_results_run(out_dir, 'Gun', root_path_neg)
