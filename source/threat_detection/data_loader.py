import os
import random
from typing import Callable, Tuple

from sklearn.model_selection import StratifiedKFold
import torch
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import pandas as pd
import numpy as np

from utils.config_parser import parse_args, parse_yaml
from transformations import transforms

SEED = 2020
random.seed(SEED)


class SixRayDataset(Dataset):

    def __init__(
            self,
            dataframe: pd.DataFrame,
            image_dir: str,
            to_tensor: Callable,
            transforms: Callable = None
    ):
        super().__init__()

        self.image_ids = dataframe['img_name'].unique()
        self.labels = ['Knife', 'Gun', 'Wrench', 'Pliers', 'Scissors']
        self.df = dataframe
        self.image_dir = os.path.join(os.getcwd(), *image_dir)
        self.to_tensor = to_tensor
        self.transforms = transforms

    def __getitem__(self, index: int):

        image_id = self.image_ids[index]
        records = self.df.loc[(self.df['img_name'] == image_id)]

        image = Image.open(os.path.join(self.image_dir, image_id))
        image = np.array(image)

        bboxes = records[['xmin', 'ymin', 'xmax', 'ymax']].values
        areas = torch.as_tensor(records['area'].values, dtype=torch.float32)
        # 1D tensor N length
        labels = torch.as_tensor(
            [np.argmax(i) + 1 for i in records[self.labels].values],
            dtype=torch.int64
        )
        # suppose all instances are not crowd
        iscrowd = torch.zeros((records.shape[0]), dtype=torch.int64)

        target = {}
        target['boxes'] = bboxes
        target['labels'] = labels
        target['image_id'] = torch.tensor([index])
        target['area'] = areas
        target['iscrowd'] = iscrowd

        if self.transforms:
            image, bboxes_aug = self.transforms(
                image=image,
                bounding_boxes=bboxes
            )
            target['boxes'] = bboxes_aug

        else:
            image = image.astype(np.float32)
            image /= 255.0
            sample = {
                'image': image,
                'bboxes': target['boxes'],
                'labels': labels
            }
            sample = self.to_tensor(**sample)
            image = sample['image']
            target['boxes'] = torch.stack(
                tuple(map(
                    lambda x: torch.tensor(x, dtype=torch.float32),
                    zip(*sample['bboxes'])
                ))
            ).permute(1, 0)

        if np.all(bboxes == 0):
            target = {
                'bboxes': torch.zeros((0, 4), dtype=torch.float32),
                'labels': torch.zeros(0, dtype=torch.int64),
                'image_id': torch.tensor([index]),
                'area': torch.zeros(0, dtype=torch.float32),
                'masks': torch.zeros(0, image.shape[0], image.shape[1],
                                     dtype=torch.uint8),
                'keypoints': torch.zeros((17, 0, 3), dtype=torch.float32),
                'iscrowd': torch.zeros((0,), dtype=torch.int64)
            }

        return image, target, image_id

    def __len__(self):
        return self.image_ids.shape[0]


def collate_fn(batch):
    return tuple(zip(*batch))


def transform_df(path_df: str) -> pd.DataFrame:
    """Transforms initial df.
    """
    df = pd.read_csv(path_df)
    #df = pd.concat([df, pd.get_dummies(df['object_type'])], axis=1)

    areas = (df['xmax'] - df['xmin']) * (df['ymax'] - df['ymin'])
    df['area'] = areas

    return df


def get_train_valid_data_loaders(
    config_data_loader: dict,
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    collate_fn: Callable,
    train_trf: Callable = None,
    valid_trf: Callable = None,
) -> Tuple[DataLoader, DataLoader]:
    """"""
    config_train_loader = config_data_loader['train_loader']
    config_valid_loader = config_data_loader['valid_loader']
    dir_train = config_data_loader['train_dataset']['dir_train']

    train_dataset = SixRayDataset(
        train_df,
        dir_train,
        transforms=train_trf,
        to_tensor=transforms.to_tensor(),
    )
    valid_dataset = SixRayDataset(
        valid_df,
        dir_train,
        transforms=None,
        to_tensor=valid_trf,
    )
    train_data_loader = DataLoader(
        train_dataset,
        collate_fn=collate_fn,
        **config_train_loader
    )
    valid_data_loader = DataLoader(
        valid_dataset,
        collate_fn=collate_fn,
        **config_valid_loader
    )
    return train_data_loader, valid_data_loader


def get_train_valid_df(
    path_df: str,
    valid_size: float = 0.2
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    """
    df = transform_df(path_df)

    image_ids = df['img_name'].unique()
    random.shuffle(image_ids)
    valid_size = round(len(image_ids) * valid_size)

    train_ids = image_ids[:-valid_size]
    valid_ids = image_ids[-valid_size:]

    train_df = df.loc[(df['img_name'].isin(train_ids))].copy()
    valid_df = df.loc[(df['img_name'].isin(valid_ids))].copy()

    return train_df, valid_df


if __name__ == '__main__':

    args = parse_args()
    config = parse_yaml(args.pyaml)
    config_dataloader = config['dataloader']

    path_df = os.path.join(os.getcwd(), *config_dataloader['path_df'])

    train_trf = transforms.ImgAugTrainTransform()
    valid_trf = transforms.to_tensor()

    train_df, valid_df = get_train_valid_df(path_df)

    train_data_loader, valid_data_loader = get_train_valid_data_loaders(
        config_dataloader,
        train_df,
        valid_df,
        collate_fn,
        train_trf,
        valid_trf
    )
    print(len(train_data_loader))

    images, targets, image_ids = next(iter(train_data_loader))

    print(f"Length of Train dataset: {len(train_data_loader.dataset)}")