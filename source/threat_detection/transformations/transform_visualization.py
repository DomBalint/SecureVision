import numpy as np
import torch

from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import os

import cv2
import pandas as pd

transforms = iaa.Sequential(
    [
        iaa.Sometimes(0.5,
                      iaa.SomeOf((1, 2), [
                          iaa.Fliplr(1.0),
                          iaa.Flipud(1.0),
                      ])
                      ),
        iaa.OneOf([
            iaa.Sometimes(0.4, [
                iaa.OneOf([
                    iaa.Multiply((0.7, 1.1)),
                    iaa.MultiplyElementwise((0.7, 1.1)),
                ]),
                iaa.OneOf([
                    iaa.MultiplySaturation((0.6, 1.5)),
                    iaa.MultiplyHue((0.6, 1.1)),
                    iaa.LinearContrast((0.8, 1.6)),
                    iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
                ]),
            ]),
            iaa.Sometimes(0.5, [
                iaa.SomeOf((1, 2), [
                    iaa.pillike.EnhanceColor((0.8, 1.2)),
                    iaa.pillike.EnhanceSharpness((0.7, 1.6)),
                    iaa.pillike.Autocontrast(cutoff=(2, 5)),
                ])
            ])
        ]),
        iaa.Sometimes(0.5, [
            iaa.Dropout(p=(0.01, 0.05)),
            iaa.GaussianBlur((0.4, 1.2)),
        ]),
    ],
    random_order=True  # apply the augmentations in random order
)
GREEN = [0, 255, 0]
ORANGE = [255, 140, 0]
RED = [255, 0, 0]


def draw_bbs(image, bbs):
    for bb in bbs.bounding_boxes:
        if bb.is_fully_within_image(image.shape):
            color = ORANGE
        elif bb.is_partly_within_image(image.shape):
            color = GREEN
        else:
            color = RED
        image = bb.draw_on_image(image, size=2, color=color)

    return image


def transforms_visualization(img_root, csv_path, plot_num):
    """

    :param img_root: root to the images (positive included)
    :param csv_path: path to the csv generated from the xml annotations
    :param plot_num: number of images to plot
    """
    df = pd.read_csv(csv_path)
    img_names = sorted(list(set(df['img_name'])))
    for name in img_names[:plot_num]:
        objects = df.loc[df['img_name'] == name]
        image = cv2.imread(os.path.join(img_root, name))
        bboxes_list = []
        for index, row in objects.iterrows():
            bboxes_list.append(BoundingBox(x1=row['xmin'], x2=row['xmax'], y1=row['ymin'], y2=row['ymax']))

        bbs = BoundingBoxesOnImage(bboxes_list, shape=image.shape)
        img_aug, bbs_aug = transforms(image=image, bounding_boxes=bbs)
        image_before = draw_bbs(image, bbs)
        cv2.imshow('Before', image_before)
        cv2.waitKey(0)
        image_after = draw_bbs(img_aug, bbs_aug)
        cv2.imshow('After', np.array(image_after))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


root_path = '/Datasets/SIXRay/tar/Positive'
path_to_csv = '/Datasets/SIXRay/gt_data.csv'
transforms_visualization(root_path, path_to_csv, 100)
