import unittest
import matplotlib.pyplot as plt

from lsv_app import core
from lsv_app.plots import curves_figure
from tests.helpers import demo_session


class PlotTests(unittest.TestCase):
    def test_metric_labels_are_separate_from_curves_and_each_other(self):
        state = demo_session()
        for curve in state['curves']:
            curve['text'] = curve['text'].replace('\t0.01\n', '\t0.001\n')
        fig, _ = curves_figure(core.process_session(state), core.ETA, core.GEO)
        fig.canvas.draw()
        self.assertEqual(len(fig.legends), 1)
        labels = fig.legends[0].get_texts()
        self.assertEqual(len(labels), 2)
        renderer = fig.canvas.get_renderer()
        boxes = [label.get_window_extent(renderer) for label in labels]
        self.assertFalse(boxes[0].overlaps(boxes[1]))
        for box in boxes:
            self.assertFalse(box.overlaps(fig.axes[0].get_window_extent(renderer)))
        plt.close(fig)

    def test_all_samples_for_each_axis_and_mode(self):
        result = core.process_session(demo_session())
        for mode in ('raw', 'mean'):
            for x in core.X_AXES:
                for y in core.Y_AXES:
                    with self.subTest(mode=mode, x=x, y=y):
                        fig, _ = curves_figure(result, x, y, mode)
                        labels = fig.axes[0].get_legend_handles_labels()[1]
                        self.assertTrue(any(label.startswith('Amostra A_') for label in labels))
                        self.assertTrue(any(label.startswith('Amostra B_') for label in labels))
                        plt.close(fig)

    def test_duplicates_and_single_electrode_are_both_shown(self):
        state = demo_session()
        state['curves'].pop()
        result = core.process_session(state)
        for mode in ('raw', 'mean'):
            for x in core.X_AXES:
                fig, _ = curves_figure(result, x, core.GEO, mode)
                labels = fig.axes[0].get_legend_handles_labels()[1]
                self.assertTrue(any(label.startswith('Amostra A_') for label in labels))
                self.assertTrue(any(label.startswith('Amostra B_') for label in labels))
                plt.close(fig)
