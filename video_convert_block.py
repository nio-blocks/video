import cv2
import io
from enum import Enum

from nio.block.base import Block
from nio.signal.base import Signal
from nio.properties import VersionProperty, SelectProperty


class Extension(Enum):
    jpg = '.jpg'
    bmp = '.bmp'
    jpeg2000 = '.jp2'
    png = '.png'
    tiff = '.tif'


class VideoConvert(Block):
    """
    Input raw CV frame (numpy arrays) and output converted frame
    """

    extension = SelectProperty(
        Extension, title='Image Extension', default=Extension.jpg)
    version = VersionProperty('0.0.1')

    def process_signals(self, signals):
        for signal in signals:
            try:
                image = io.BytesIO()
                frame = signal.frame
                ret, temp_image = cv2.imencode(self.extension().value, frame)
                image.write(temp_image.tobytes())
                output_sig = {
                    'image': image,
                    'extension': self.extension().value
                }
                self.notify_signals(Signal(output_sig))
            except:
                self.logger.exception("Failed to execute command")
