from typing import List, Union

import numpy as np
from numba import jit


@jit(nopython=True)
def calculate_iou(
    gt: np.ndarray,
    pr: np.ndarray,
    form: str = 'pascal_voc'
) -> float:
    """Calculates the Intersection over Union.
    Args:
        gt: coordinates of the ground-truth box
        pr: coordinates of the predicted box
        form: gt/pred coordinates format
            - pascal_voc: [xmin, ymin, xmax, ymax]
            - coco: [xmin, ymin, w, h]
    Returns:
        Intersection over union (0.0 <= iou <= 1.0)
    """
    if form == 'coco':
        gt = gt.copy()
        pr = pr.copy()

        gt[2] = gt[0] + gt[2]
        gt[3] = gt[1] + gt[3]
        pr[2] = pr[0] + pr[2]
        pr[3] = pr[1] + pr[3]

    # Calculate overlap area
    dx = min(gt[2], pr[2]) - max(gt[0], pr[0]) + 1

    if dx < 0:
        return 0.0

    dy = min(gt[3], pr[3]) - max(gt[1], pr[1]) + 1

    if dy < 0:
        return 0.0

    overlap_area = dx * dy

    # Calculate union area
    union_area = (
            (gt[2] - gt[0] + 1) * (gt[3] - gt[1] + 1) +
            (pr[2] - pr[0] + 1) * (pr[3] - pr[1] + 1) -
            overlap_area
    )

    return overlap_area / union_area


@jit(nopython=True)
def find_best_match(
    gts: List[List[Union[int, float]]],
    pred: List[Union[int, float]],
    pred_idx: int,
    threshold: float = 0.5,
    form: str = 'pascal_voc',
    ious: np.ndarray = None
) -> int:
    """Returns the index of the 'best match' between the
    ground-truth boxes and the prediction. The 'best match'
    is the highest IoU. (0.0 IoUs are ignored).
    Args:
        gts: Coordinates of the available ground-truth boxes
        pred: Coordinates of the predicted box
        pred_idx: Index of the current predicted box
        threshold: Threshold
        form: (str) Format of the coordinates
        ious: len(gts) x len(preds) matrix for storing calculated IoUs.
    Return:
        Index of the best match GT box (-1 if no match above threshold)
    """
    best_match_iou = -np.inf
    best_match_idx = -1

    for gt_idx in range(len(gts)):

        if gts[gt_idx][0] < 0:
            # Already matched GT-box
            continue

        iou = -1 if ious is None else ious[gt_idx][pred_idx]

        if iou < 0:
            iou = calculate_iou(gts[gt_idx], pred, form=form)

            if ious is not None:
                ious[gt_idx][pred_idx] = iou

        if iou < threshold:
            continue

        if iou > best_match_iou:
            best_match_iou = iou
            best_match_idx = gt_idx

    return best_match_idx


@jit(nopython=True)
def calculate_precision(
    gts: List[List[Union[int, float]]],
    preds: List[List[Union[int, float]]],
    threshold: float = 0.5,
    form: str = 'coco',
    ious: np.ndarray = None
    ) -> float:
    """Calculates precision for GT - prediction pairs at one threshold.
    Args:
        gts: Coordinates of the available ground-truth boxes
        preds: Coordinates of the predicted boxes, sorted by confidence value
               (descending)
        threshold: Threshold
        form: Format of the coordinates
        ious: len(gts) x len(preds) matrix for storing calculated IoUs.
    Return:
        (float) Precision
    """
    n = len(preds)
    tp = 0
    fp = 0

    for pred_idx in range(n):

        best_match_gt_idx = find_best_match(gts, preds[pred_idx], pred_idx,
                                            threshold=threshold, form=form,
                                            ious=ious)

        if best_match_gt_idx >= 0:
            # True positive: The predicted box matches a gt box with an IoU
            # above the threshold.
            tp += 1
            # Remove the matched GT box
            gts[best_match_gt_idx] = -1

        else:
            # No match
            # False positive: indicates a predicted box had no associated gt
            # box.
            fp += 1

    # False negative: indicates a gt box had no associated predicted box.
    fn = (gts.sum(axis=1) > 0).sum()

    return tp / (tp + fp + fn)


@jit(nopython=True)
def calculate_image_precision(
    gts: List[List[Union[int, float]]],
    preds: List[List[Union[int, float]]],
    thresholds: List[float],
    form: str,
) -> float:
    """Calculates image precision.
    Args:
        gts: Coordinates of the available ground-truth boxes
        preds: Coordinates of the predicted boxes, sorted by confidence value
               (descending)
        thresholds: Different thresholds
        form: Format of the coordinates
    Return:
        Precision
    """
    n_threshold = len(thresholds)
    image_precision = 0.0

    ious = np.ones((len(gts), len(preds))) * -1
    # ious = None

    for threshold in thresholds:
        precision_at_threshold = calculate_precision(gts.copy(), preds,
                                                     threshold=threshold,
                                                     form=form, ious=ious)
        image_precision += precision_at_threshold / n_threshold

    return image_precision
