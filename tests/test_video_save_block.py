import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestVideoSave(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        from ..video_save_block import VideoSave
        global VideoConvert

    def test_video_save(self):
        pass