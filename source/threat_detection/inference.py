import os

import cv2
import pandas as pd
import torch

import data_loader as dl
from models.model_zoo import get_model
from train import get_empty_scores_dict
from transformations import transforms as trfs
from utils.utilities import parse_args, parse_yaml


def predict_data_set(
        model,
        data_loader,
        device,
        cpu_device,
        output_path
):
    # Don't need to keep track of gradients
    with torch.no_grad():

        if model.training:
            # Set to evaluation mode (BatchNorm and Dropout works differently)
            model.eval()

        # Validation loop
        for ii, (images, targets, image_ids) in enumerate(data_loader):

            # Tensors to device
            images = list(image.to(device) for image in images)

            outputs = model(images)
            outputs = [
                {
                    k: v.to(cpu_device).numpy() for k, v in t.items()
                } for t in outputs
            ]
            # TODO: Add NMS
            for idx, (image, image_id) in enumerate(zip(images, image_ids)):

                preds = outputs[idx]['boxes']
                image_vis = cv2.imread(os.path.join(os.getcwd(), 'datasets', 'train', 'Positive', image_id))
                for row in preds:
                    c1 = int(row[0]), int(row[1])
                    c2 = int(row[2]), int(row[3])

                    cv2.rectangle(image_vis, c1, c2, (0, 0, 255), 3)

                cv2.imwrite(os.path.join(output_path, image_id), image_vis)


def predict_model(
        valid_data_loader,
        model,
        path_save_model,
        output_path
):
    """
    """
    scores_dict_valid = get_empty_scores_dict(valid_data_loader)

    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    cpu_device = torch.device('cpu')

    model.to(device)
    model.load_state_dict(torch.load(path_save_model, map_location=torch.device('cpu')))

    predict_data_set(
        model, valid_data_loader, device,
        cpu_device,
        output_path
    )

    df_scores_valid = pd.DataFrame(scores_dict_valid)

    return df_scores_valid


def set_up_evaluation(config: dict, weights_path, output_path):
    cwd = os.getcwd()

    config_dataloader = config['dataloader']
    path_df = os.path.join(cwd, *config_dataloader['path_df'])

    train_df, valid_df = dl.get_train_valid_df(path_df, valid_size=0.1)
    valid_trf = trfs.to_tensor()
    _, valid_data_loader = dl.get_train_valid_data_loaders(
        config_dataloader, train_df, valid_df, dl.collate_fn, valid_trf=valid_trf)

    model = get_model()
    predict_model(valid_data_loader, model, weights_path, output_path)


if __name__ == "__main__":
    args = parse_args()
    config = parse_yaml(args.pyaml)
    weights_path_global = '/Datasets/SIXRay/fasterrcnn_test.pth'
    output_path_global = '/Datasets/SIXRay/output/inference'
    set_up_evaluation(config, weights_path_global, output_path_global)
