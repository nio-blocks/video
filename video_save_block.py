import ast
import cv2

from nio.block.base import Block
from nio.properties import StringProperty, IntProperty
from nio.properties import VersionProperty


class VideoSave(Block):
    """
    Take in raw frames (numpy arrays) and save video to file,
    currently in mpeg format.
    """

    filename = StringProperty(title='Filename', default='file.mpg')
    frame_size = StringProperty(
        title='Frame Size (as tuple)', default='(640,480)')
    frame_rate = IntProperty(title='Frames per second', default=30)
    version = VersionProperty('0.0.1')

    def configure(self, context):
        super().configure(context)
        # If I move this out of configure,
        # then I could include setup info in the passed signal
        self.video_file = cv2.VideoWriter(
            self.filename(),
            cv2.VideoWriter_fourcc('M', 'P', 'E', 'G'),
            self.frame_rate(),
            ast.literal_eval(self.frame_size())
        )

    def process_signals(self, signals):
        for signal in signals:
            try:
                # frame = self.frame(signal)
                frameSignal = signal.to_dict()
                rawFrame = frameSignal['frame']
                if self.frame_size():
                    resized_frame = cv2.resize(
                        rawFrame, ast.literal_eval(self.frame_size()))
                else:
                    resized_frame = rawFrame
                self.video_file.write(resized_frame)
            except:
                self.logger.exception("Failed to execute command")

    def stop(self):
        """Not sure this is completely necessary"""
        try:
            self.logger.debug('Halting VideoSave thread')
            cv2.destroyAllWindows()
        except:
            self.logger.exception('Exception while halting VideoSave')
        super().stop()
