import metrics


class TestMetrics:

    def test_calculate_precision(self, precision_data):
        """"""
        # Setup
        gt_boxes, preds_sorted, thr_prec = precision_data
        threshold, desired_precision = thr_prec
        # Exercise
        actual_precision = metrics.calculate_precision(
            gt_boxes.copy(),
            preds_sorted,
            threshold=threshold,
            form='coco'
        )
        # Verify
        assert desired_precision == round(actual_precision, 4)