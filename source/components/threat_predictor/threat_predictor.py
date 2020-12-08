import os

import numpy as np
from PIL import Image
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

from svlib.svtools import svtools as svt

log = svt.log


class ThreatPredictor:

    def __init__(
        self,
        path_model: str,
        model_name: str,
        kafka_input_topic: str,
        kafka_output_topic: str
    ) -> None:
        self.path_model = path_model
        self.model_name = model_name
        self.kafka_input_topic = kafka_input_topic
        self.kafka_output_topic = kafka_output_topic
        self.kafka_helper = svt.kafka
        self.device = torch.device('cpu')
        self.model = self.load_model()
        self.classes = {
            0: 'backGround',
            1: 'Knife',
            2: 'Gun',
            3: 'Wrench',
            4: 'Pliers',
            5: 'Scissors'
        }

    def load_model(self):
        """"""
        model = fasterrcnn_resnet50_fpn(pretrained=False,
                                        pretrained_backbone=False)
        # ['Knife', 'Gun', 'Wrench', 'Pliers', 'Scissors'] + background
        num_classes = 6
        # get number of input features for the classifier
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        # replace the pre-trained head with a new one
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features,
                                                          num_classes)
        # Load the trained weights
        path_model = os.path.join(os.getcwd(), self.path_model,
                                  self.model_name)
        model.load_state_dict(torch.load(
            path_model, map_location=self.device
        ))
        model.eval()
        model.to(self.device)

        return model

    def detect_threat(self, message: dict) -> None:
        """

        :param message:
        :return:
        """
        path_image = os.path.join(message['imagePath'], message['imageID'])
        log.info(f"Received a scanned X-ray image at path: {path_image}")

        image = Image.open(path_image)
        image = np.array(image).astype(np.float32)
        image /= 255.0
        sample = A.Compose([ToTensorV2(p=1.0)])(**{'image': image})
        image = sample['image']
        image.to(self.device)
        # add a batch a dimension
        image = image.unsqueeze(0)

        output = self.model(image)

        # get all predicted class names
        pred_classes = set([
            self.classes[i] for i in output[0]['labels'].cpu().numpy()
        ])
        # get scores and bounding boxes for all predicted objects
        boxes = output[0]['boxes'].data.cpu().numpy()
        scores = output[0]['scores'].data.cpu().numpy()

        detection_threshold = 0.5
        boxes = boxes[scores >= detection_threshold].astype(np.int32)
        scores = scores[scores >= detection_threshold]

        boxes[:, 2] = boxes[:, 2] - boxes[:, 0]
        boxes[:, 3] = boxes[:, 3] - boxes[:, 1]

        log.info(f"Detected classes: {pred_classes}\n")
        log.info(f"Predicted scores: {scores}\n")
        log.info(f"Predicted bounding boxes: {boxes}\n")

    def get_scanned_images(self) -> None:
        """"""
        self.kafka_helper.consume_forever(
            group_id='threat_predictor',
            topics=[self.kafka_input_topic],
            callback_functions=[self.detect_threat]
        )



if __name__ == '__main__':

    cr = svt.conf
    app_conf = cr.parse_yaml(
        os.path.join(os.getcwd(), 'configs', 'app_config.yaml')
    )['threat_predictor']

    tp = ThreatPredictor(**app_conf)

    tp.get_scanned_images()

