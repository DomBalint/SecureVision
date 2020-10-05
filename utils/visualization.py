"""For everything related to visualization"""

import os

import cv2
import pandas as pd


def plot_bboxes(img_root, csv_path, output_path, plot_num):
    """

    :param img_root: root to the images (positive included)
    :param csv_path: path to the csv generated from the xml annotations
    :param output_path: path to output the images
    :param plot_num: number of images to plot
    """
    os.makedirs(output_path, exist_ok=True)
    df = pd.read_csv(csv_path)
    img_names = sorted(list(set(df['img_name'])))
    for name in img_names[:plot_num]:
        objects = df.loc[df['img_name'] == name]
        image = cv2.imread(os.path.join(img_root, name))
        for index, row in objects.iterrows():
            c1 = int(row['xmin']), int(row['ymin'])
            c2 = int(row['xmax']), int(row['ymax'])
            cv2.rectangle(image, c1, c2, (255, 0, 0), 1)

        cv2.imwrite(os.path.join(output_path, name), image)


root_path = 'Example/Path/to/Datasets/SIXRay/Images'
path_to_csv = 'Example/Path/to/Datasets/SIXRay/gt_data.csv'
out_dir = 'Example/Path/to/Softtech/Datasets/SIXRay/output'
plot_bboxes(root_path, path_to_csv, out_dir, 100)
