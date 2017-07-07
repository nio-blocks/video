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
        super().__init__()
        self._is_broadcasting = Event()

    def configure(self, context):
        super().configure(context)
        self.camera = None
        self.frame = None
        if self.openOnStart():
        	self._openSource()

    def start(self):
        #super.start()
        if self._is_broadcasting.is_set():
            spawn(self.run)

    def process_signals(self, signals):
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
        try:
            self._is_broadcasting.clear()
            self.logger.debug('Halting VideoInput thread')
            #self._closeSource()
        except:
            self.logger.exception('Exception while halting VideoInput')
        super().stop()
