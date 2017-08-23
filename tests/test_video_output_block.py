import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestVideoOutput(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        from ..video_output_block import VideoOutput
        global VideoOutput

    def test_video_output(self):
        blk = VideoOutput()
        with patch(VideoOutput.__module__ + '.cv2') as patch_cv2:
            # patch Event()? (self._is_broadcasting)

            patch_cv2.VideoCapture = MagicMock()
            patch_cv2.cvtColor = MagicMock()

            mock_camera = patch_cv2.VideoCapture
            mock_grayscale = patch_cv2.cvtColor

            mock_camera.return_value.read.return_value = 'mckGrab', 'mckFrame'
            mock_grayscale.return_value = 'grayscaleFrame'

            self.configure_block(blk, {
                'grayscale': True
            })
            blk.start()
            blk.process_signals([Signal({})])  # is this necessary?

            mock_grayscale.assert_called_with(
                'mckFrame', patch_cv2.COLOR_BGR2GRAY)
            self.assert_last_signal_notified(Signal({
                'frame': 'grayscaleFrame'
            }))

            blk.stop()
