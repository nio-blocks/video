import numpy
import cv2
from threading import Event
from time import sleep

from nio.block.base import Block
from nio.signal.base import Signal
from nio.util.threading import spawn
from nio.properties import StringProperty, BoolProperty, VersionProperty, \
    IntProperty


class VideoOutput(Block):
    """
    Open video source and output raw frames (numpy arrays)
    """

    source = StringProperty(title='Video Source', default='', allow_none=True)
    openOnStart = BoolProperty(title='Open source on start',
                               default=True,
                               visible=False)
    grayscale = BoolProperty(title='Convert to grayscale', default=False)
    frame_rate = IntProperty(title='Frames per second', default=0)
    version = VersionProperty('0.0.1')

    def __init__(self):
        super().__init__()
        self._is_broadcasting = Event()
        self._thread = None

    def configure(self, context):
        super().configure(context)
        self.camera = None
        if self.openOnStart():
            self._openSource()

    def start(self):
        super().start()
        if self._is_broadcasting.is_set():
            self._thread = spawn(self._run)

    def stop(self):
        try:
            self._is_broadcasting.clear()
            self.logger.debug('Halting VideoInput thread')
            self.camera.release()
            self._thread.join()
        except:
            self.logger.exception('Exception while halting VideoInput')
        # cv2.destroyAllWindows()
        super().stop()

    def _run(self):
        while self._is_broadcasting.is_set():
            (grabbed, frame) = self.camera.read()
            if self.frame_rate():
                sleep(1 / self.frame_rate())
            if not grabbed:
                self._is_broadcasting.clear()
                self.logger.exception('Failed to grab frame')
            else:
                if self.grayscale():
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                self.notify_signals([Signal({'frame': frame})])

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
        self.logger.debug('Opening source: {}'.format(
            source if source else 'Local Camera'))
