#********************************************************************************************************
# File:              station_generator.py                                              
# Author:            hexiang6666                                     | Boris Jeremic,                       
# Date:              2017-04-06 19:27:23                         | University of California, Davis,95616*
# Description:       #############                               | California                           #
# Rev:               Version 1                                   | jeremic@ucdavis.edu                  #
# Email:             hexwang@ucdavis.edu                         | Computational Geomechanics Group     #
# * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  # 
#                           Last Modified time: 2017-03-16 22:29:55                                     #              
#  * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #        
# The copyright to the computer program(s) herein is the property of Hexiang Wang and Boris Jeremic     #
# The program(s) may be used and/or copied only with written permission of Hexiang Wang or in accordance#
# with the terms and conditions stipulated in the agreement/contract under which the program have been  #
# supplied.                                                                                             #
#*******************************************************************************************************#

#! /usr/bin/env python
import scipy as sp

############################ Usr input variables ###################################################################
##### Aligned ESSI nodes configuration is assumed here ######################################################

Reference_station_x= input('Enter the x coordinate of reference station, whose station ID=(0 0 0): ');

Reference_station_y= input('Enter the y coordinate of reference station, whose station ID=(0 0 0): ');

Reference_station_z= input('Enter the y coordinate of reference station, whose station ID=(0 0 0): ');

ESSI_nodes_x_spacing= input('Enter the spacing of ESSI nodes in x direction: ');  

ESSI_nodes_y_spacing= input('Enter the spacing of ESSI nodes in y direction: ');

ESSI_nodes_z_spacing= input('Enter the spacing of ESSI nodes in z direction: ');

ESSI_Box_length= input('Enter the length (x direction) of ESSI Box: ');

ESSI_Box_width= input('Enter the width (y direction) of ESSI Box: ');

ESSI_Box_height= input('Enter the height (z direction) of ESSI Box: ');

########################## Ending usr input part #########################################################

No_ESSI_nodes= (1+ESSI_Box_length/ESSI_nodes_x_spacing)*(1+ESSI_Box_width/ESSI_nodes_y_spacing)*(1+ESSI_Box_height/ESSI_nodes_z_spacing);

station=sp.zeros((No_ESSI_nodes,6));

for x1 in xrange(0,ESSI_Box_length/ESSI_nodes_x_spacing):
	for x2 in xrange(0,ESSI_Box_width/ESSI_nodes_y_spacing):
		for x3 in xrange(0,ESSI_Box_height/ESSI_Box_height):
			station

