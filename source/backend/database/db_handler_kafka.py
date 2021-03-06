import os

from containers import Handlers
from svlib.svtools import svtools as svt
from create_db import create_db

log = svt.log


class DatabaseLoader:

    def __init__(
            self,
            kafka_input_topic: str,
            number_of_cameras: int,
    ) -> None:
        self.kafka_input_topic = kafka_input_topic
        self.num_of_cams = int(number_of_cameras)
        self.kafka_helper = svt.kafka

        self.camera_handler_instance = Handlers.cam_handler()
        self.user_handler_instance = Handlers.user_handler()
        self.ann_handler_instance = Handlers.ann_handler()
        self.img_handler_instance = Handlers.img_handler()
        self.fb_handler_instance = Handlers.fb_handler()

        create_db(self.num_of_cams)

    def upload_to_db(self, message: dict) -> None:
        """

        :param message:
        :return:
        """
        producer_id = message["producerID"]
        img_path = message["outputImagePath"] if message["outputImagePath"] else (message["imagePath"] + '/' + message["imageID"])

        img_id = message["imageID"]
        if 'P' in img_id and not message["outputImagePath"]:
            return 

        img_id = self.img_handler_instance.add_image(img_path=img_path, camera_id=producer_id)
        log.info(f"Uploaded image: {img_id} path: {str(img_path).split('/')[-1]}\n")

        if message["prediction"]:
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
