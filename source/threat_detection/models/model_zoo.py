from torchvision.models.detection.faster_rcnn import FastRCNNPredictor


def get_model(name: str = 'fasterrcnn_resnet50_fpn'):

    if name == 'fasterrcnn_resnet50_fpn':
        from torchvision.models.detection import fasterrcnn_resnet50_fpn
        # load a model; pre-trained on COCO
        model = fasterrcnn_resnet50_fpn(pretrained=True)
    else:
        return None
    # ['Knife', 'Gun', 'Wrench', 'Pliers', 'Scissors'] + background
    num_classes = 6
    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    return model


if __name__ == '__main__':

    m = get_model()
    print(m)
