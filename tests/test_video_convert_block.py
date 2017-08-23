import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestVideoConvert(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        from ..video_convert_block import VideoConvert
        global VideoConvert

    def test_video_convert(self):
        blk = VideoConvert()
        with patch(VideoConvert.__module__ + '.cv2.imencode') as \
                mock_cv2_imencode,\
                patch(VideoConvert.__module__ + '.io.BytesIO') as mock_bytesIO:
            mock_temp_image = MagicMock()
            mock_cv2_imencode.return_value = 'mockRet', mock_temp_image

            self.configure_block(blk, {
                'extension': '.jpg'
            })
            blk.start()
            blk.process_signals([Signal({
                'frame': [[1], [2]]
            })])
            mock_cv2_imencode.assert_called_with('.jpg', [[1], [2]])
            mock_bytesIO.return_value.write.assert_called_once_with(
                mock_temp_image.tobytes())
            self.assert_num_signals_notified(1)
            self.assert_last_signal_notified(Signal({
                'image': mock_bytesIO.return_value,
                'extension': '.jpg'
            }))
            blk.stop()
