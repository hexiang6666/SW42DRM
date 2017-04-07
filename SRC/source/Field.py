
###########################################################################################################################
#                                                                                                                         #
#  Generate_DRM :: Python Script to generate DRM Field Motion                                                             #
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -                                      #
#                                                                                                                         #
#                                                                                                                         #
#  GITHUB:: GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools.git                                           #
#                                                                                                                         #
#                                                                                                                         #
#  Sumeet Kumar Sinha (September,2016)                                                                                    #
#  Computational Geomechanics Group                                                                                       #
#  University of California, Davis                                                                                        #
#  s u m e e t k s i n h a . c o m                                                                                        #
########################################################################################################################### 

import math;
import numpy as np;

def getField (x,y,z,DRM_Time):

	NumTimeSteps = DRM_Time.shape[0];
	acceleration = np.zeros([3, NumTimeSteps],dtype=np.double);
	displacement = np.zeros([3, NumTimeSteps],dtype=np.double);
	time_index = 0; 


	for t in DRM_Time:
		# w = 2*math.pi*1;
		# v = 1000;
		# k = w/v
		# # displacement[0,time_index] = math.sin(w*t -k*z);
		# # acceleration[0,time_index] = -1*w*w*math.sin(w*t -k*z);
		# time_index = time_index +1;

	return displacement, acceleration;
