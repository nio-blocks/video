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
        pass
