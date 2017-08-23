VideoConvert
============
Convert individual frames to images.  Input raw CV frame (numpy arrays) and output converted frame.

Properties
----------
- **extension**: Type of image file to output.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A signal containing the resulting image and the extension type.

Commands
--------

VideoOutput
===========
Captures video stream from specified source and notifies the frames as signals.

Properties
----------
- **frame_rate**: Frame rate of video stream.
- **grayscale**: Convert colored video stream to grayscale.
- **openOnStart**: Start capturing video stream when block starts (hidden property).
- **source**: Where to find the streaming camera.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A signal with the individual captured frames.

Commands
--------

VideoSave
=========
Save a video stream to a specified file.

Properties
----------
- **filename**: File name to save video stream to.
- **frame_rate**: Frame rate of video stream.
- **frame_size**: Pixel size of the frame.

Inputs
------
- **default**: Any list of signals.

Outputs
-------

Commands
--------

