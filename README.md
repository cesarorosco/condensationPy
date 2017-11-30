# condensationPy - Condensation Tracking in Python

Condensation Tracking algorithm in Python - a version based on the original OpenCV code

### Background

- Based on the Legacy version on OpenCV and the Android version available here:
https://android.googlesource.com/platform/external/opencv/+/android-5.1.1_r6/cv/src/cvcondens.cpp

- For the GUI example it's based on the example:
http://www.morethantechnical.com/2011/06/17/simple-kalman-filter-for-tracking-using-opencv-2-2-w-code/

- For an introduction to particle filters read these before:
http://www.anuncommonlab.com/articles/how-kalman-filters-work/

### Code Details:

- _Condensation.py_: main tracking object for Condensation approach
- _live_\__tracking.py_: live tracking of objects from webcam
- _mouseCondensation.py_: tracking of mouse pointer (original)

---

### How to download and run:

Download each file as needed or to download the entire repository and run each try:

```
git clone https://github.com/tobybreckon/condensationPy.git
cd condensationPy
python3 ./live_tracking.py [optional video file]
```

Demo source code is provided _"as is"_ to aid learning and understanding of topics on the course and beyond.

_live_\__tracking.py_ runs with a webcam connected or from a command line supplied video file of a format OpenCV supports on your system (otherwise edit the script to provide your own image source).

N.B. you may need to change the line near the top that specifies the camera device to use on some examples below - change "0" if you have one webcam, I have it set to "1" to skip my built-in laptop webcam and use the connected USB camera.

---

If you find any bugs raise an issue (or much better still submit a git pull request with a fix) - toby.breckon@durham.ac.uk

_"may the source be with you"_ - anon.
