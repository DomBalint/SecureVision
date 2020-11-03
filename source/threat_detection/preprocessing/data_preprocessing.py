"""
Process the dataset, split it into train and test sets, and applying data augmentation.
"""

import numpy as np
import tqdm
import csv
import os


def read_labels(file):
    """
    :param file: labels csv file for the train or test data
    """

    object_labels = {}
    num_categories = 0
    print('reading_file', file)
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in tqdm.tqdm(reader):
            if num_categories == 0:
                num_categories = len(row) - 1
            name = row[0]
            labels = (np.asarray(row[1:num_categories + 1])).astype(np.float32)
            object_labels[name] = labels

    return header, object_labels


def shuffle_split_data(images_path, positive_test_split_percentage=0.2,
                       negative_test_split_percentage=0.2):
    """
   :param images_path: path to the directory containing all of the images (positive and negative).
   :param positive_test_split_percentage: percentage of positive images to keep for the test set.
   :param negative_test_split_percentage: percentage of negative images to keep for the test set.
   """

    images_names = os.listdir(images_path)
    positive_images_names = np.asarray([image for image in images_names if image.startswith('P')])
    negative_images_names = np.asarray(list(set(images_names) - set(positive_images_names)))

    positive_train_indices = np.arange(len(positive_images_names))
    np.random.shuffle(positive_train_indices)

    positive_images_names = positive_images_names[positive_train_indices]
    positive_training_samples = int(len(positive_train_indices) * (1 - positive_test_split_percentage))
    positive_x_train = positive_images_names[:positive_training_samples]
    positive_x_test = positive_images_names[positive_training_samples:]

    negative_train_indices = np.arange(len(negative_images_names))
    np.random.shuffle(negative_train_indices)

    negative_images_names = negative_images_names[negative_train_indices]
    negative_training_samples = int(len(negative_train_indices) * (1 - negative_test_split_percentage))
    negative_x_train = negative_images_names[:negative_training_samples]
    negative_x_test = negative_images_names[negative_training_samples:]

    return (positive_x_train, positive_x_test), (negative_x_train, negative_x_test)


(positive_x_train, positive_x_test), (negative_x_train, negative_x_test) = shuffle_split_data("/path/to/images")

# TODO: add data processing here


# TODO: add data augmentation code here
