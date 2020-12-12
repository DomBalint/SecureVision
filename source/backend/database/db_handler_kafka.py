import os

from containers import Handlers
from svlib.svtools import svtools as svt
from create_db import create_db

log = svt.log


class DatabaseLoader:

    def __init__(
            self,
            kafka_input_topic: str,
    ) -> None:
        self.kafka_input_topic = kafka_input_topic
        self.kafka_helper = svt.kafka

        self.camera_handler_instance = Handlers.cam_handler()
        self.user_handler_instance = Handlers.user_handler()
        self.ann_handler_instance = Handlers.ann_handler()
        self.img_handler_instance = Handlers.img_handler()
        self.fb_handler_instance = Handlers.fb_handler()

        create_db()

    def upload_to_db(self, message: dict) -> None:
        """

        :param message:
        :return:
        """
        path_image = message["outputImagePath"]
        producer_id = message["producerID"] + 1
        img_id = self.img_handler_instance.add_image(img_path=path_image, camera_id=producer_id)

        if message["prediction"]:
            assert len(message["confidenceScores"]) == len(message["predictedObjects"]) == len(message["boundingBoxes"])
            for confidence, obj_type, bbox in zip(message["confidenceScores"], message["predictedObjects"],
                                                  message["boundingBoxes"]):
                X, Y, W, H = bbox
                self.ann_handler_instance.add_annotations_from_manual(img_id=img_id, obj_type=obj_type,
                                                                      obj_conf=confidence, left_x=X, left_y=Y,
                                                                      length=W,
                                                                      width=H)
                log.info(f"Uploaded object: {obj_type}\n")
                log.info(f"Confidence score: {confidence}\n")

    def get_predicted_images(self) -> None:
        """"""
        self.kafka_helper.consume_forever(
            group_id='db_uploader',
            topics=[self.kafka_input_topic],
            callback_functions=[self.upload_to_db]
        )


if __name__ == '__main__':
    cr = svt.conf
    app_conf = cr.parse_yaml(
        os.path.join(os.getcwd(), 'configs', 'app_config.yaml')
    )['database_loader']

    db = DatabaseLoader(**app_conf)

    db.get_predicted_images()
