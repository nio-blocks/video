import numpy
import cv2
from nio.block.base import Block
from nio.signal.base import Signal
from nio.util.discovery import discoverable
from nio.util.threading import spawn
from nio.properties import StringProperty, BoolProperty, VersionProperty
from threading import Event

@discoverable
class VideoConvert(Block):
    '''
    Input raw CV frame (numpy arrays) and output converted frame
    '''

    extension = StringProperty(title='Image extension', default='.jpg')
    version = VersionProperty('0.0.1')

    def process_signals(self, signals):
        """Overrideable method to be called when signals are delivered.
        This method will be called by the block router whenever signals
        are sent to the block. The method should not return the modified
        signals, but rather call `notify_signals` so that the router
        can route them properly.
        Args:
            signals (list): A list of signals to be processed by the block
            input_id: The identifier of the input terminal the signals are
                being delivered to
        """
        for signal in signals:
            try:
                frameSignal = signal.to_dict()
                frame = frameSignal['frame']
                ret, image = cv2.imencode(self.extension(), frame)
                output_sig = {'image':image,'extension':self.extension()}
                self.notify_signals(Signal(output_sig))
            except:
                self.logger.exception("Failed to execute command")


