import os
from collections import namedtuple
from random import randint

import cv2
import numpy as np
import pandas as pd
import tqdm

from PIL import Image


def area(a, b):
    """
    Calculates the area of intersection between to Rectangles
    :param a: First Rectangle object
    :param b: Second Rectangle object
    :return:
    """
    # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx >= 0) and (dy >= 0):
        return dx * dy
    else:
        return -1


def create_collision_matrix(bounding_box_list):
    """
    Creates collision matrix for the cropping together
    :param bounding_box_list: list of bounding boxes
    :return:
    """
    collision_matrix = np.zeros((len(bounding_box_list), len(bounding_box_list)))
    for a_index, rect_a in enumerate(bounding_box_list):
        for b_index, rect_b in enumerate(bounding_box_list):
            if area(rect_a, rect_b) > 0:
                collision_matrix[a_index, b_index] = 1
    return collision_matrix


def create_rect_list(object_df):
    """
    Creates a list of Rectangle objects from the csv file for better handling
    :param object_df: list of the objects on an image
    :return:
    """
    Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax type')
    rect_list = []
    for index, row in object_df.iterrows():
        rect_r = Rectangle(int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']),
                           str(row['object_type']))
        rect_list.append(rect_r)
    return rect_list


def create_workdirs(obj_type_list, output_path):
    """
    Creates the directories for the cropping, one for every object type
    :param obj_type_list: List of the object types
    :param output_path: the base directory for the cropped objects
    """
    for obj_type in obj_type_list:
        os.makedirs(os.path.join(output_path, obj_type), exist_ok=True)


# TODO: Handle annotation if cropping objects together
def cropping_colliding_together(img_root, csv_path, output_path):
    """
    Cropping in a way that those objects whose bounding boxes are colliding are saved together
    :param img_root: root to the images (positive included)
    :param csv_path: path to the csv generated from the xml annotations
    :param output_path: path to output the images
    """
    os.makedirs(output_path, exist_ok=True)
    df = pd.read_csv(csv_path)
    img_names = sorted(list(set(df['img_name'])))
    obj_types = sorted(list(set(df['object_type'])))
    create_workdirs(obj_types, output_path)
    for name in tqdm.tqdm(img_names, 'Creating cropped objects'):
        objects = df.loc[df['img_name'] == name]
        image = cv2.imread(os.path.join(img_root, name))
        rect_list = create_rect_list(objects)

        collision_matrix = create_collision_matrix(rect_list)
        has_rectangle = True
        while has_rectangle:
            max_row = np.argmax(np.sum(collision_matrix, axis=1))
            y_min = []
            y_max = []
            x_min = []
            x_max = []
            type_list = []
            delete_list = []
            for index_obj, elem_i in enumerate(collision_matrix[max_row]):
                if elem_i == 1:
                    delete_list.append(index_obj)
                    y_min.append(rect_list[index_obj].ymin)
                    y_max.append(rect_list[index_obj].ymax)
                    x_min.append(rect_list[index_obj].xmin)
                    x_max.append(rect_list[index_obj].xmax)
                    type_list.append(rect_list[index_obj].type)

            for obj_type in list(set(type_list)):
                crop_img = image[int(np.min(np.array(y_min))):int(np.max(np.array(y_max))),
                           int(np.min(np.array(x_min))):int(np.max(np.array(x_max)))]
                im_name = name.split('.')[0] + '_' + str(max_row) + '.jpg'
                cv2.imwrite(os.path.join(output_path, obj_type, im_name), crop_img)
            collision_matrix[:, delete_list] = 0
            if np.sum(np.sum(collision_matrix, axis=1), axis=0) == 0:
                has_rectangle = False


def cropping(img_root, csv_path, output_path):
    """

    :param img_root: root to the images (positive included)
    :param csv_path: path to the csv generated from the xml annotations
    :param output_path: path to output the images
    """
    os.makedirs(output_path, exist_ok=True)
    df = pd.read_csv(csv_path)
    obj_types = sorted(list(set(df['object_type'])))
    create_workdirs(obj_types, output_path)
    img_names = sorted(list(set(df['img_name'])))

    for name in tqdm.tqdm(img_names, 'Creating cropped objects'):
        objects = df.loc[df['img_name'] == name]
        image = cv2.imread(os.path.join(img_root, name))
        for index, row in objects.iterrows():
            crop_img = image[int(row['ymin']):int(row['ymax']), int(row['xmin']):int(row['xmax'])]
            im_name = name.split('.')[0] + '_' + str(index) + '.jpg'
            cv2.imwrite(os.path.join(output_path, row['object_type'], im_name), crop_img)


# TODO: Fine tune segmentation
def segmentation(img, low_hsv, high_hsv, negate):
    """
    This is just a proof of concept function for the segmentation, should be refined
    Segmentation type based on: https://medium.com/srm-mic/color-segmentation-using-opencv-93efa7ac93e2
    :param low_hsv: segmentation rule based: specifying color boundaries
    :param img: image that needs to be segmented
    :param high_hsv: segmentation rule based: specifying color boundaries
    :param negate: specify if return the negate of the mask
    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, low_hsv, high_hsv)
    if negate:
        mask = ~mask
    result = cv2.bitwise_and(np.array(img), np.array(img), mask=mask)
    return result, mask


def remove_small(base_dir, object_type, min_dim):
    """
    Remove the unnecessarily small images
    :param min_dim: remove images that are smaller than this dimension
    :param base_dir: Base dir of the segmentation, like the cropped "Gun" folder
    :param object_type: Specifying the type of the object
    """
    images = os.listdir(os.path.join(base_dir, object_type))
    for image in tqdm.tqdm(images, 'Removing small images'):
        if image.endswith('.png') or image.endswith('.jpg'):
            img_path = os.path.join(base_dir, object_type, image)
            img = cv2.imread(img_path)
            if min_dim[0] > img.shape[0] or min_dim[1] > img.shape[1]:
                os.remove(img_path)


def rescale(img, negative_img):
    """
    :param img: The image of the object that needs to be segmented
    :param negative_img: negative image as an numpy array
    :return:
    """

    threat_w, threat_h = img.size
    negative_img_w, negative_img_h = negative_img.size
    max_resize = np.max(np.array([negative_img_w, negative_img_h] / np.array([threat_w, threat_h])))
    resize_lin = np.linspace(1, max_resize / 3, num=10)
    random_index = randint(0, len(resize_lin) - 1)
    img = img.resize(
        (round(img.size[0] * (resize_lin[random_index])), round(img.size[1] * resize_lin[random_index])))
    return img


def area_of_interest(base_img, inv_mask, obj_width, obj_height):
    """
    Selects the area of interest from the negative image, basically the background for the segmented object
    :param base_img: Negative image
    :param inv_mask: negated mask of the object segmentation
    :param obj_width: width of the object
    :param obj_height: height of the object
    :return:
    """
    # Select the area to insert the segmented gun with a negative mask, and returns its surroundings
    aoi = cv2.bitwise_and(np.array(base_img[250:250 + obj_width, 250:250 + obj_height]),
                          np.array(base_img[250:250 + obj_width, 250:250 + obj_height]),
                          mask=inv_mask)
    return aoi


@ DeprecationWarning
def run_segmentation(base_dir, object_type, path_to_negatives):
    """
    Run the different segmentations and compare them
    :param path_to_negatives: path to the negative images that need augmentation
    :param base_dir: Base dir of the segmentation, like the cropped "Gun" folder
    :param object_type: Specifying the type of the object
    """
    images = os.listdir(os.path.join(base_dir, object_type))
    negatives = os.listdir(path_to_negatives)

    # TODO: Find the boundaries of the luggage
    for image in images:
        if image.endswith('.png') or image.endswith('.jpg'):
            img_path = os.path.join(base_dir, object_type, image)
            rand_path = os.path.join(path_to_negatives, negatives[randint(0, len(negatives))])
            random_negative = Image.open(rand_path).convert('RGB')

            threat_obj = Image.open(img_path).convert('RGB')
            # Random resize
            threat_obj = rescale(threat_obj, random_negative)
            # Random rotation
            threat_obj = threat_obj.rotate(randint(0, 360), expand=True)
            threat_obj_cv = np.array(threat_obj)
            threat_obj_cv = threat_obj_cv[:, :, ::-1].copy()

            random_negative_cv = np.array(random_negative)
            random_negative_cv = random_negative_cv[:, :, ::-1].copy()

            # TODO: Handle bounding box and annotation generation
            low_blue = np.array([55, 0, 0])
            high_blue = np.array([118, 255, 255])
            result, mask = segmentation(threat_obj_cv, low_blue, high_blue, False)
            aoi_background = area_of_interest(random_negative_cv, ~mask, result.shape[0], result.shape[1])
            # TODO: FIND BETTER POSITIONING
            # Add together to object and the surrounding from the other image and overwrite the part of the negative img
            random_negative_cv[250:250 + result.shape[0], 250:250 + result.shape[1]] = (aoi_background + result)
            cv2.imshow('F', np.array(result))
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def threshold_image(image, verbose):
    """
    Threshold the image using otsu algorithm, to separate the foreground from the background.
    This works as (foreground-background segmentation)
    :param verbose: Show image or not
    :param image: image
    :return: the image, and the thresholded image
    """

    if verbose:
        print('Showing image before segmentation')
        cv2.imshow("image", cv2.resize(image, (960, 540)))
        cv2.waitKey(0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_value, threshold_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    max_threshold_indices = threshold_image >= threshold_value
    min_threshold_indices = threshold_image < threshold_value
    threshold_image[max_threshold_indices] = 1
    threshold_image[min_threshold_indices] = 0

    return image, threshold_image


def remove_small_regions(threshold_image_input):
    """
    Keep only the largest connected object in the image (this is a great way to remove noise)

    :param threshold_image_input: numpy array containing the values of the threshold image,
    :return: a processed image with only the largest element in the threshold_image.
    """
    processed_image = np.zeros_like(threshold_image_input)

    for val in np.unique(threshold_image_input)[1:]:
        mask = np.uint8(threshold_image_input == val)
        labels, stats = cv2.connectedComponentsWithStats(mask, 4)[1:3]
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        processed_image[labels == largest_label] = val

    return processed_image

def get_boundaries(img):
    height = img.height
    width = img.width
    top_boundaries = []
    bottom_boundaries = []
    left_boundaries = []
    right_boundaries = []
    # Top down search
    for j in range(width):
        i = 0
        while(i < height and img.getpixel((j, i)) == (255, 255, 255)):
            i += 1
        top_boundaries.append(i)
    # Bottom up search
    for j in range(width):
        i = height - 1
        while(i >= 0 and img.getpixel((j, i)) == (255, 255, 255)):
            i -= 1
        bottom_boundaries.append(i)
    # Left search
    for i in range(height):
        j = 0
        while(j < width and img.getpixel((j, i)) == (255, 255, 255)):
            j += 1
        left_boundaries.append(j)
    # Right search
    for i in range(height):
        j = width - 1
        while(j >= 0 and img.getpixel((j, i)) == (255, 255, 255)):
            j -= 1
        right_boundaries.append(j)

    return top_boundaries, bottom_boundaries, left_boundaries, right_boundaries


def check_if_inside(pos_r, pos_c, width, height, top_bounds, bottom_bounds, left_bounds, right_bounds):
    for j in range(pos_c, pos_c + width):
        if pos_r < top_bounds[j] or pos_r + height - 1 > bottom_bounds[j]:
            return False
    for i in range(pos_r, pos_r + height):
        if pos_c < left_bounds[i] or pos_c + width - 1 > right_bounds[i]:
            return False

    return True

def otsu_segmentation(base_dir, object_type, path_to_negatives, saved_images, verbose=False):
    """
    Run the otsu algorithm for background-foreground  segmentation
    :param verbose: Show every step of the segmentation or not
    :param saved_images: Save the images to this folder
    :param path_to_negatives: path to the negative images that need augmentation
    :param base_dir: Base dir of the segmentation, like the cropped "Gun" folder
    :param object_type: Specifying the type of the object
    """

    images = os.listdir(os.path.join(base_dir, object_type))
    negatives = os.listdir(path_to_negatives)
    counter = 0
    os.makedirs(saved_images, exist_ok=True)
    annotation_list = []
    for image in tqdm.tqdm(images, 'Otsu segmentation'):
        if image.endswith('.png') or image.endswith('.jpg'):
            img_path = os.path.join(base_dir, object_type, image)
            rand_path = os.path.join(path_to_negatives, negatives[randint(0, len(negatives))])
            random_positive = Image.open(rand_path)
            random_negative =  random_positive.convert('RGB')
            if random_negative is None:
                continue

            threat_obj = cv2.imread(img_path)

            if verbose:
                print('Showing random negative')
                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                cv2.imshow("image", cv2.resize(random_negative, (960, 540)))
                cv2.waitKey(0)

            threat_image, threshold_threat_image = threshold_image(threat_obj, verbose)

            if verbose:
                print('Showing segmentation results')
                cv2.imshow("image", cv2.resize(threshold_threat_image * 255, (960, 540)))
                cv2.waitKey(0)

            threshold_threat_image = remove_small_regions(threshold_threat_image)

            if verbose:
                print('Cleaning segmentation results')
                cv2.imshow("image", cv2.resize(threshold_threat_image * 255, (960, 540)))
                cv2.waitKey(0)

            # TODO: do some morphological operations to fix the image

            clean_threat_object = np.expand_dims(threshold_threat_image, axis=2).repeat(3, axis=2)
            clean_threat_object *= threat_image
            # Format here, when rotating the background has to be filled instead it distorts the image
            # Converting to Pillow Image and resizing
            clean_threat_object = cv2.cvtColor(clean_threat_object, cv2.COLOR_BGR2RGB)
            clean_threat_object = Image.fromarray(clean_threat_object)
            clean_threat_object = rescale(clean_threat_object, random_negative)
            # Random rotation
            clean_threat_object = clean_threat_object.rotate(randint(0, 360), expand=True, fillcolor='black')
            clean_threat_object = np.array(clean_threat_object)
            clean_threat_object = clean_threat_object[:, :, ::-1]

            random_negative = np.array(random_negative)
            random_negative = random_negative[:, :, ::-1]

            if verbose:
                print('Showing resized')
                cv2.imshow("image", clean_threat_object)
                cv2.waitKey(0)

            top, bottom, left, right = get_boundaries(random_positive)
            try:
                # Add the threat object in a random position to the negative example
                neg_r, neg_c = random_negative.shape[:2]
                threat_r, threat_c = clean_threat_object.shape[:2]
                a = randint(0, neg_r - threat_r)
                b = randint(0, neg_c - threat_c)
                while(not check_if_inside(a, b, threat_r, threat_c, top, bottom, left, right)):
                    a = randint(0, neg_r - threat_r)
                    b = randint(0, neg_c - threat_c)

                for i, ii in zip(range(a, a + threat_r), range(threat_r)):
                    for j, jj in zip(range(b, b + threat_c), range(threat_c)):
                        for k in range(3):
                            if clean_threat_object[ii, jj, k] > 0:
                                random_negative[i, j, k] = round(random_negative[i, j, k]*0.1 + clean_threat_object[ii, jj, k]*0.9)

                # To be used in the annotation creation process (after the method has been evaluated)
                # print(f"Threat place: xmin={a}, xmax={a + threat_r}, ymin={b}, ymax={b + threat_c}")

                cv2.imshow("Press s to save", cv2.resize(random_negative, (960, 540)))
                key = cv2.waitKey(0)

                # if key == 's'
                if key == 115:
                    # TODO: add to the annotations file (figure out what to do for multiple objects)
                    filename, extension = image.split(".")
                    filename_rand = rand_path.split(".")[0].split('/')[-1].split('\\')[-1]
                    cv2.imwrite(os.path.join(saved_images, f"{filename}_{filename_rand}_{str(counter)}.{extension}"),
                                random_negative)

                    new_annotation = {
                        'img_name': f"{filename}_{filename_rand}_{str(counter)}.{extension}",
                        'width': random_negative.shape[0],
                        'height': random_negative.shape[1],
                        'object_type': object_type,
                        'xmin': a,
                        'ymin': b,
                        'xmax': a + threat_r,
                        'ymax': b + threat_c,
                        'generated': True
                    }
                    annotation_list.append(new_annotation)

                    counter += 1
                    print('Image saved')
                cv2.destroyAllWindows()

            # The shape of the threat is larger than the image itself
            except ValueError as ve:
                print(clean_threat_object.shape)
                print(random_negative.shape)
                print(str(ve))
            except IndexError as ie:
                print(str(ie))
            except Exception as e:
                print(str(e))
    df = pd.DataFrame(annotation_list)
    df.to_csv(os.path.join(out_dir, 'generated.csv'), index=False)


if __name__ == '__main__':

    root_path_pos = '../datasets/SIXRay/Positive'
    root_path_neg = '../datasets/SIXRay/Negative'
    path_to_csv = '../datasets/SIXRay/gt_data.csv'
    out_dir = '../datasets/SIXRay/output'
    saved_to = '../datasets/SIXRay/Generated'

    # 1. Crops out the area of interest from the positive images, like guns, knives, etc..
    # cropping(root_path_pos, path_to_csv, out_dir)
    # 1.5. Instead of the basic cropping it is also possible to crop the colliding bounding boxes together
    # cropping_colliding_together(root_path_pos, path_to_csv, out_dir)

    # 2. Removes the small objects, that are useless for augmentation
    # remove_small(out_dir, 'Gun', (99, 50))

    # 3. Runs the segmentation
    otsu_segmentation(out_dir, 'Gun', root_path_neg, saved_images)

    print("done...")
