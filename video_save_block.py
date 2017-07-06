from nio.block.base import Block
from nio.signal.base import Signal
from nio.types.dict import DictType
from nio.util.discovery import discoverable
from nio.properties import StringProperty, IntProperty, Property
from nio.properties import VersionProperty
import ast, cv2, numpy

@discoverable
class VideoSave(Block):
    '''
    Take in raw frames (numpy arrays) and save video to file, currently in mpeg format.
    '''

    filename = StringProperty(title='Filename', default='file.mpg')
    frameSize = StringProperty(title='Frame Size (as tuple)', default='(640,480)')
    fps = IntProperty(title='Frames per second', default=30)
    version = VersionProperty('0.0.1')

    def configure(self, context):
        """Overrideable method to be called when the block configures.
        The block creator should call the configure method on the parent,
        after which it can assume that any parent configuration options present
        on the block are loaded in as class variables. They can also assume
        that all functional modules in the service process are loaded and
        started.
        Args:
            context (BlockContext): The context to use to configure the block.
        Raises:
            TypeError: If the specified router is not a BlockRouter
        """
        super().configure(context)
        self.videoFile = cv2.VideoWriter(self.filename(), cv2.VideoWriter_fourcc('M','P','E','G'), self.fps(), ast.literal_eval(self.frameSize()))

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
                #frame = self.frame(signal)
                frameSignal = signal.to_dict()
                rawFrame = frameSignal['frame']
                resizedFrame = cv2.resize(rawFrame,ast.literal_eval(self.frameSize()))
                self.videoFile.write(resizedFrame)
            except:
                self.logger.exception("Failed to execute command")

    def stop(self):
        """Overrideable method to be called when the block stops.
        The block creator can assume at this point that the service and block
        router are in "stopping" state. All modules are still available for use
        in the service process.
        """
        try:      
            self.logger.debug('Halting VideoSave thread')
            cv2.destroyAllWindows()
        except:
            self.logger.exception('Exception while halting VideoSave')
        super().stop()
