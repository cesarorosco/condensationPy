"""

Based on the OpenCV Version of the Condensation Algorithm and the
Android Version available here:
https://android.googlesource.com/platform/external/opencv/+/android-5.1.1_r6/cv/src/cvcondens.cpp

Read before:
http://www.anuncommonlab.com/articles/how-kalman-filters-work/

/*M///////////////////////////////////////////////////////////////////////////////////////
//
//  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.
//
//  By downloading, copying, installing or using the software you agree to this license.
//  If you do not agree to this license, do not download, install,
//  copy or use the software.
//
//
//                        Intel License Agreement
//                For Open Source Computer Vision Library
//
// Copyright (C) 2000, Intel Corporation, all rights reserved.
// Third party copyrights are property of their respective owners.
//
// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
//   * Redistribution's of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//   * Redistribution's in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//
//   * The name of Intel Corporation may not be used to endorse or promote products
//     derived from this software without specific prior written permission.
//
// This software is provided by the copyright holders and contributors "as is" and
// any express or implied warranties, including, but not limited to, the implied
// warranties of merchantability and fitness for a particular purpose are disclaimed.
// In no event shall the Intel Corporation or contributors be liable for any direct,
// indirect, incidental, special, exemplary, or consequential damages
// (including, but not limited to, procurement of substitute goods or services;
// loss of use, data, or profits; or business interruption) however caused
// and on any theory of liability, whether in contract, strict liability,
// or tort (including negligence or otherwise) arising in any way out of
// the use of this software, even if advised of the possibility of such damage.
//
"""
import numpy as np

# Condensation Algorithm.
# Python version based on the original OpenCv Version and the
# Android version
# Requires the initialization of DynamMatr
# Example: DynamMatr = [[1.0, 0.0], [0.0, 1.0]]
# The confidence must be defined
# Example:
# a = (PositionX - sample[i][0])/650
# b = (PositionY - sample[i][1])/650
# flConfidence[i]=1.0/(sqrt(a*a + b*b))
class Condensation():

    # Name: __init__
    # Creating variables
    # Parameters:
    #   DP         - dimension of the dynamical vector
    #   MP         - dimension of the measurement vector
    #   SamplesNum - number of samples in sample set used in algorithm
    def __init__(self, dimDP, dimMP, samplesNum):

        if(dimDP < 0 or dimMP < 0 or samplesNum < 0):
            raise ValueError("Parameters out of range")

        self.SamplesNum = samplesNum
        self.DP = dimDP
        self.MP = dimMP
        self.flSamples =[]
        self.flNewSamples = np.empty([self.SamplesNum, self.DP], dtype=float)
        self.flConfidence = []
        self.flCumulative = np.zeros(self.SamplesNum, dtype=float)
        self.DynamMatr = []
        self.State = np.zeros(self.DP, dtype=float)
        self.lowBound=np.empty(self.DP, dtype=float)
        self.uppBound=np.empty(self.DP, dtype=float)


    # Name: cvConDensInitSampleSet
    # Initializing for the Condensation algorithm
    # Parameters:
    #   conDens     - pointer to CvConDensation structure
    #   lowerBound  - vector of lower bounds used to random update
    #                   of sample set
    #   upperBound  - vector of upper bounds used to random update
    #                   of sample set
    #
    def cvConDensInitSampleSet(self, lowerBound, upperBound):
        prob = 1.0/self.SamplesNum

        if((lowerBound is None) or (upperBound is None)):
            raise ValueError("Lower/Upper Bound")

        self.lowBound = lowerBound
        self.uppBound = upperBound

        # Generating the samples
        for j in range(self.SamplesNum):
            valTmp = np.zeros(self.DP, dtype=float)
            for i in range(self.DP):
                valTmp[i] = np.random \
                    .uniform(lowerBound[i],upperBound[i])
            self.flSamples.append(valTmp)
            self.flConfidence.append(prob)

    # Name:    cvConDensUpdateByTime
    # Performing Time Update routine for ConDensation algorithm
    # Parameters:
    def cvConDensUpdateByTime(self):
        valSum  = 0
        #Sets Temp To Zero
        self.Temp = np.zeros(self.DP, dtype=float)

        #Calculating the Mean
        for i in range(self.SamplesNum):
            self.State = np.multiply(self.flSamples[i], self.flConfidence[i])
            self.Temp = np.add(self.Temp, self.State)
            valSum += self.flConfidence[i]
            self.flCumulative[i] = valSum

        #Taking the new vector from transformation of mean by dynamics matrix
        self.Temp = np.multiply(self.Temp, (1.0/valSum))
        for i in range(self.DP):
            self.State[i] = np.sum(np.multiply(self.DynamMatr[i],
                                               self.Temp[i]))

        valSum = valSum / float(self.SamplesNum)

        #Updating the set of random samples
        for i in range(self.SamplesNum):
            j = 0
            while (self.flCumulative[j] <= float(i)*valSum and
                j < self.SamplesNum -1):
                j += 1
            self.flNewSamples[i] = self.flSamples[j]

        lowerBound = np.empty(self.DP, dtype=float)
        upperBound = np.empty(self.DP, dtype=float)
        for j in range(self.DP):
            lowerBound[j] = (self.lowBound[j] - self.uppBound[j])/5.0
            upperBound[j] = (self.uppBound[j] - self.lowBound[j])/5.0

        #Adding the random-generated vector to every vector in sample set

        # which assumes a moiton model of equal likely motion in all directions

        RandomSample = np.empty(self.DP, dtype=float)
        for i in range(self.SamplesNum):
            for j in range(self.DP):
                RandomSample[j] = np.random.uniform(lowerBound[j],
                                                    upperBound[j])
                self.flSamples[i][j] = np.sum(np.multiply(self.DynamMatr[j],
                                               self.flNewSamples[i][j]))

            self.flSamples[i] = np.add(self.flSamples[i], RandomSample)
