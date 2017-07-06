import numpy
import cv2
from nio.block.base import Block
from nio.signal.base import Signal
from nio.util.discovery import discoverable
from nio.util.threading import spawn
from nio.properties import StringProperty, BoolProperty, VersionProperty
from threading import Event

@discoverable
class VideoOutput(Block):
    '''
    Open video source and output raw frames (numpy arrays)
    '''

    source = StringProperty(title='Video Source', default='')
    openOnStart = BoolProperty(default=True, title='Open source on start')
    version = VersionProperty('0.0.1')

    def __init__(self):
        """ Create a new block instance.
        Take care of setting up instance variables in your block's constructor.
        Note that the properties of the block are not available when the block
        is created. Those will be available when the block is configured.
        It is normally meaningless to pass variables to the constructor of the
        block. Any data the block requires will be passed through the
        BlockContext when the block is configured.
        """
        super().__init__()
        self._is_broadcasting = Event()

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
        self.camera = None
        self.frame = None
        if self.openOnStart():
        	self._openSource()

    def start(self):
        """Overrideable method to be called when the block starts.
        The block creator can assume at this point that the block's
        initialization is complete and that the service and block router
        are in "starting" state.
        """
        #super.start()
        if self._is_broadcasting.is_set():
            spawn(self.run)

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
                pass
            except:
                self.logger.exception("Failed to execute command")
        

    def run(self):
        while self._is_broadcasting.is_set():
            (grabbed, frame) = self.camera.read()
            if not grabbed:
                self._is_broadcasting.clear()
                self.logger.exception('Failed to grab frame')
            else:
                self.frame = frame
                pass_frame = {'frame' : frame}
                self.notify_signals([Signal(pass_frame)])

    def _openSource(self):
        """ With no source, use attached camera """
        source = self.source()
        try:
            if not source:
                self.camera = cv2.VideoCapture(0)
            else:
                self.camera = cv2.VideoCapture(source)
            self._is_broadcasting.set()
        except:
        	self._is_broadcasting.clear()
        self.logger.debug('Opening source: {}'.format((source if source else 'Local Camera')))

    ''' Camera seems to close itself and this fails
    def _closeSource(self):
        try:
            self.camera.release()
            self.logger.debug('VideoInput halted')
        except:
            self.logger.exception('Something went terribly wrong')
    '''

    def stop(self):
        """Overrideable method to be called when the block stops.
        The block creator can assume at this point that the service and block
        router are in "stopping" state. All modules are still available for use
        in the service process.
        """
        try:
            self._is_broadcasting.clear()
            self.logger.debug('Halting VideoInput thread')
            #self._closeSource()
        except:
            self.logger.exception('Exception while halting VideoInput')
        super().stop()
