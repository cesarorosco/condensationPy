"""
Condensation Algorithm - Example
Based on the example provided here
http://www.morethantechnical.com/2011/06/17/simple-kalman-filter-for-tracking-using-opencv-2-2-w-code/

"""


# Libraries
import numpy as np
import cv2
import Condensation as cons


class MouseGUI():

    def __init__(self, parent):

        self.mouse_info = (-1, -1)

        self.mouseV = []
        self.calculated = []

        self.counter = -1

        self.initialize()

    def initialise_defaults(self):
        """ This routine fills in the data structures with default constant
        values. It could be enhanced by reading informatino from the
        command line to allow e.g. """

        dim = 2
        nParticles = 100
        self.xRange = 650.0
        self.yRange = 650.0
        LB = [0.0, 0.0]
        UB = [self.xRange, self.yRange]
        self.model = cons.Condensation(dim, dim, nParticles)
        self.model.cvConDensInitSampleSet(LB, UB)
        self.model.DynamMatr = [[1.0, 0.0],
                                [0.0, 1.0]]

    def initialize(self):

        # Initialize model specific conditions
        self.initialise_defaults()

        # Windows Init
        cv2.namedWindow('Mouse Particle')
        cv2.setMouseCallback('Mouse Particle', self.on_mouse)

        img = np.zeros((650, 650, 3), np.uint8)

        countPts = 0

        while True:

            # Clear all
            img[:, :] = (0, 0, 0)

            sizeVec = len(self.mouseV) - 1

            if(sizeVec == -1):
                cv2.imshow('Mouse Particle', img)
                cv2.waitKey(30)
                continue

            for i in range(sizeVec):
                cv2.line(img, self.mouseV[i], self.mouseV[i + 1],
                         (255, 255, 0), 1)

            if int(self.counter) == int(0):
                pts = self.mouseV[sizeVec]
                for z in range(self.model.SamplesNum):

                    # Calculate the confidence based on the observations
                    diffX = (pts[0] - self.model.flSamples[z][0]) / self.xRange
                    diffY = (pts[1] - self.model.flSamples[z][1]) / self.yRange
                    self.model.flConfidence[z] = 1.0 / (np.sqrt(np.power(diffX, 2) +
                                                                np.power(diffY, 2)))

                # Updates
                self.model.cvConDensUpdateByTime()
                self.update_after_iterating(img)

                # Not required, (max n points)
                if countPts > 50:
                    break

            countPts += 1

            self.counter += 1

            cv2.imshow('Mouse Particle', img)

            key = cv2.waitKey(100)

            if key == ord('q'):
                break

        cv2.destroyAllWindows()

    def on_mouse(self, event, x, y, flags, param):

        if event == cv2.EVENT_MOUSEMOVE:
            self.last_mouse = self.mouse_info
            self.mouse_info = (x, y)
            self.counter = 0
            self.mouseV.append((x, y))

    def drawCross(self, img, center, color, d):
        # On error change cv2.CV_AA for cv2.LINE_AA
        # (for differents versions of OpenCV)
        cv2.line(img, (center[0] - d, center[1] - d),
                 (center[0] + d, center[1] + d), color, 2, cv2.LINE_AA, 0)
        cv2.line(img, (center[0] + d, center[1] - d),
                 (center[0] - d, center[1] + d), color, 2, cv2.LINE_AA, 0)

    def update_after_iterating(self, img):

        mean = self.model.State
        meanInt = [int(s) for s in mean]

        for j in range(len(self.model.flSamples)):
            posNew = [int(s) for s in self.model.flSamples[j]]
            self.drawCross(img, posNew, (255, 255, 0), 2)

        self.calculated.append(meanInt)

        for z in range(len(self.calculated) - 1):
            p1 = (self.calculated[z][0], self.calculated[z][1])
            p2 = (self.calculated[z + 1][0], self.calculated[z + 1][1])
            cv2.line(img, p1, p2, (255, 255, 255), 1)

        sizeVec = len(self.mouseV) - 1
        print("Mean: %d %d" % (meanInt[0], meanInt[1]))
        print(
            "Real: %d %d" %
            (self.mouseV[sizeVec][0],
             self.mouseV[sizeVec][1]))
        print('+++++++++++++++')
        self.drawCross(img, meanInt, (255, 0, 255), 2)


if __name__ == "__main__":
    app = MouseGUI(None)
