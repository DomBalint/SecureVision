import os
import glob
import traceback
import random

from svlib.svtools import svtools as svt

log = svt.log


class XRayProducer:

    def __init__(
        self,
        producer_id: int,
        path_images: str,
        cron_expr: str
    ) -> None:
        self.producer_id = producer_id
        self.path_images = path_images
        self.cron_expr = cron_expr
        self.kafka_helper = svt.kafka
        self.scheduler = svt.chrono
        self.images = glob.glob(os.path.join(os.getcwd(), path_images, '*jpg'))
        self.kafka_topic = svt.conf.get('kafka', 'producer')['topic']

    def scan_image(self) -> str:
        """Picks a random image.

        :return: path of the picked image
        """
        img = random.choice(self.images).split(os.sep)[-1]
        log.info(
            f"XRayProducer - {self.producer_id} - scanned an image with ID: "
            f"{img}"
        )
        return img

    def get_xray_scan_schema(self, img: str) -> dict:
        """Returns an empty x_ray_scan schema.

        :param img: ID of the scanned image
        :return: filled xray_scan schema represented by a dictionary
        """
        xray_scan = {
            "version": "1.0.0",
            "producerID": self.producer_id,
            "createdTS": self.scheduler.now_as_str(),
            "imageID": img,
            "imagePath": self.path_images
        }
        return xray_scan

    def publish_scanned_image(self) -> None:
        """Publishes the scanned X-ray image to the configured Kafka topic.
        """
        img = self.scan_image()
        xray_scan = self.get_xray_scan_schema(img)
        self.kafka_helper.publish(self.kafka_topic, xray_scan)

    def run(self) -> None:
        """Runs the publish_scanned_image function with the configured
        schedule.
        """
        try:
            self.scheduler.schedule(
                callback_func=self.publish_scanned_image,
                cron_expression=self.cron_expr,
            )
            self.scheduler.start()
        except Exception as err:
            log.error(
                f"Unexpected event occurred! Error: {traceback.format_exc()}"
            )


if __name__ == '__main__':

    cr = svt.conf
    app_conf = cr.parse_yaml(
        os.path.join(os.getcwd(), 'configs', 'app_config.yaml')
    )['producer']
    # Not like Ripple LOL
    xrp = XRayProducer(**app_conf)
    xrp.run()

