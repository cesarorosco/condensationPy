# condensationPy - Condensation Tracking in Python

Condensation Tracking algorithm in Python - a version based on the original OpenCV code

### Background

Forked from https://github.com/cesarorosco/condensationPy for use in teaching within the undergraduate Computer Science programme
at [Durham University](http://www.durham.ac.uk) (UK) by [Prof. Toby Breckon](https://breckon.org/toby/).

- Based on the Legacy version on OpenCV and the Android version available here:
https://android.googlesource.com/platform/external/opencv/+/android-5.1.1_r6/cv/src/cvcondens.cpp

- For the GUI example it's based on the example:
http://www.morethantechnical.com/2011/06/17/simple-kalman-filter-for-tracking-using-opencv-2-2-w-code/

- For an introduction to particle filters read these before:
http://www.anuncommonlab.com/articles/how-kalman-filters-work/


### Code Details:

- _live_\__tracking.py_: live tracking of selected objects from webcam / video file
- _Condensation.py_: main tracking object for Condensation approach
- _camera_stream.py_: threaded camera capture interface

_live_\__tracking.py_ runs with a webcam connected or from a command line supplied video
file of a format OpenCV supports on your system (otherwise edit the script to provide your own image source).

Tested with [OpenCV](http://www.opencv.org) 3.x / 4.x and Python 3.x.

---

### How to download and run:

Download each file as needed or to clone the entire repository as follows:

```
git clone https://github.com/tobybreckon/condensationPy.git
cd condensationPy
python3 ./live_tracking.py [optional video file]
```

Command line usage of the main tracking demo is as follows:

```
$ python3 ./live_tracking.py -h
usage: live_tracking.py [-h] [-c CAMERA_TO_USE] [-r RESCALE] [video_file]

Perform Condensation (particle filter) tracking on an incoming camera image

positional arguments:
  video_file            specify optional video file

optional arguments:
  -h, --help            show this help message and exit
  -c CAMERA_TO_USE, --camera_to_use CAMERA_TO_USE
                        specify camera to use
  -r RESCALE, --rescale RESCALE
                        rescale image by this factor

```

Once the tracking script is running perform the following steps

- use the sliders in the "Hue Histogram Back projection" to **isolate (in white) the colours of the object** you want to track.
- **click and drag in the main colour image window** to select an object to track.
- ...
- press 'x' to exit

Demo source code is provided _"as is"_ to aid learning and understanding of topics on the course and beyond.

---

If you find any bugs raise an issue (or much better still submit a git pull request with a fix) - toby.breckon@durham.ac.uk

_"may the source be with you"_ - anon.
