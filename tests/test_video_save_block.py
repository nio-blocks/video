import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestVideoSave(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        from ..video_save_block import VideoSave
        global VideoSave

    def test_video_save(self):
        blk = VideoSave()
        with patch(VideoSave.__module__ + '.cv2') as patch_cv2, \
                patch(VideoSave.__module__ + '.ast') as patch_ast:
            patch_cv2.VideoWriter = MagicMock()
            patch_cv2.resize = MagicMock()

            mock_video_file = patch_cv2.VideoWriter
            mock_resized_frame = patch_cv2.resize
            mock_resized_frame.return_value = 'resizeReturn'

            self.configure_block(blk, {
                'filename': 'testFile',
                'frame_rate': 1,
            })
            blk.start()
            blk.process_signals([Signal({
                'frame': [[1], [2]]
            })])

            mock_video_file.assert_called_with(
                'testFile',
                patch_cv2.VideoWriter_fourcc(),
                1,
                patch_ast.literal_eval()
            )
            mock_video_file.return_value.write.assert_called_with(
                'resizeReturn')

            blk.stop()
