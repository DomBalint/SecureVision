import os
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.ops import nms
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
        self.tp_schema_helper = svt.schema.create_helper('ThreatPrediction')

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

    def predict_image(self, path_image: str) -> Tuple:
        """

        :param path_image:
        :return:
        """
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

        # CODE FOR THE NMS COMMENT OUT IF NOT NEEDED
        new_output = []

        for idx, output_ in enumerate(output):
            preds = output[idx]['boxes']
            scores = output[idx]['scores']
            keep = nms(preds, scores, 0.5)
            new_dict = {'boxes': output[idx]['boxes'][keep],
                        'scores': output[idx]['scores'][keep],
                        'labels': output[idx]['labels'][keep],
                        }
            new_output.append(new_dict)
        output = new_output
        # CODE FOR THE NMS

        # get all predicted class names
        pred_classes = np.array([
            self.classes[i] for i in output[0]['labels'].cpu().numpy()
        ])
        detection_threshold = 0.5
        # get scores and bounding boxes for all predicted objects
        boxes = output[0]['boxes'].data.cpu().numpy()
        scores = output[0]['scores'].data.cpu().numpy()
        # x, y, w, h
        boxes[:, 2] = boxes[:, 2] - boxes[:, 0]
        boxes[:, 3] = boxes[:, 3] - boxes[:, 1]

        pred_classes = pred_classes[scores >= detection_threshold].tolist()
        boxes = boxes[scores >= detection_threshold].astype(np.int32).tolist()
        scores = scores[scores >= detection_threshold].tolist()

        return pred_classes, boxes, scores

    def draw_bounding_boxes(
            self,
            path_image: str,
            boxes: list,
            output_image_path: str
    ) -> None:
        """

        :param path_image:
        :param boxes:
        :param output_image_path:
        :return:
        """
        image = cv2.imread(path_image)
        # convert back to numpy
        boxes = np.array(boxes)
        # x1, y1, x2, y2
        boxes[:, 2] = boxes[:, 2] + boxes[:, 0]
        boxes[:, 3] = boxes[:, 3] + boxes[:, 1]

        for box in boxes:
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]),
                          (0, 0, 255), 3)

        cv2.imwrite(output_image_path, image)

    def get_threat_prediction_schema(
            self,
            message: dict,
            predictions: dict
    ) -> dict:
        """

        :param message:
        :param predictions:
        :return:
        """
        threat_prediction = {
            "version": "1.0.0",
            "producerID": message["producerID"],
            "modelName": self.model_name.split(".pth")[0],
            "imageID": message["imageID"],
            "imagePath": message["imagePath"],
            "predictionTS": svt.chrono.now_as_str(),
        }
        threat_prediction.update(predictions)

        return threat_prediction

    def detect_threat(self, message: dict) -> None:
        """

        :param message:
        :return:
        """
        path_image = os.path.join(message['imagePath'], message['imageID'])

        pred_classes, boxes, scores = self.predict_image(path_image)

        # log.info(f"Detected classes: {pred_classes}\n")
        # log.info(f"Predicted scores: {scores}\n")
        # log.info(f"Predicted bounding boxes: {boxes}\n")
        # No drawing of bounding boxes on the image if there is no threat
        if pred_classes:
            parts = message["imageID"].split('.')
            oip = os.path.join("predictions", parts[0] + '_bbox.' + parts[1])
            self.draw_bounding_boxes(path_image, boxes, oip)
        else:
            oip = ""

        predictions = {
            "prediction": True if pred_classes else False,
            "numberOfThreats": len(pred_classes),
            "outputImagePath": oip,
            "predictedObjects": pred_classes,
            "boundingBoxes": boxes,
            "confidenceScores": scores
        }
        threat_prediction = self.get_threat_prediction_schema(message,
                                                              predictions)
        log.info(threat_prediction)
        self.tp_schema_helper.validate(threat_prediction)
        self.kafka_helper.publish(self.kafka_output_topic, threat_prediction)

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
