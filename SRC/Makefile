#*******************************************************************************************************#
# File:              ShellScript.tmpl                                              
# Author:            hexiang6666                                 | Boris Jeremic,                       #
# Date:              2017-04-05 19:57:43                         | University of California, Davis,95616#
# Description:       #############                               | California                           #
# Rev:               Version 1                                   | jeremic@ucdavis.edu                  #
# Email:             hexwang@ucdavis.edu                         | Computational Geomechanics Group     #
# * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  # 
#                           Last Modified time: 2017-04-07 14:25:11                                     #              
#  * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #         
# The copyright to the computer program(s) herein is the property of Hexiang Wang and Boris Jeremic     #
# The program(s) may be used and/or copied only with written permission of Hexiang Wang or in accordance# 
# with the terms and conditions stipulated in the agreement/contract under which the program have been  #
# supplied.                                                                                             #
#*******************************************************************************************************#
BUILD_DIR = $(realpath $(CURDIR))/../build
SOURCE_DIR= $(realpath $(CURDIR))

all: DRM_pre station_generation location_transformation SW42DRM
DRM_pre:
	@cp DRM_preprocess_reserved DRM_preprocess
	@echo export INSTALL_DIR=$(PWD) | cat - DRM_preprocess > temp && mv temp DRM_preprocess
	@echo "#!/bin/bash" | cat - DRM_preprocess > temp && mv temp DRM_preprocess
	@sudo ln -sf $(SOURCE_DIR)/DRM_preprocess /usr/local/bin
	@cd /usr/local/bin ; sudo chmod +x DRM_preprocess
station_generation:
	@sudo chmod +x $(SOURCE_DIR)/station_generator.py 
	@sudo ln -sf $(SOURCE_DIR)/station_generator.py /usr/local/bin

location_transformation:
	@sudo chmod +x $(SOURCE_DIR)/ESSI_location.py
	@sudo ln -sf $(SOURCE_DIR)/ESSI_location.py /usr/local/bin

SW42DRM:
	@cp SW42DRM.py_reserved SW42DRM.py
	@echo 'SOURCE_DIR='"'"'$(SOURCE_DIR)'"'" | cat - SW42DRM.py > temp && mv temp SW42DRM.py
	@echo "#! /usr/bin/env python" | cat - SW42DRM.py > temp && mv temp SW42DRM.py
	@sudo chmod +x $(SOURCE_DIR)/SW42DRM.py
	@sudo ln -sf $(SOURCE_DIR)/SW42DRM.py /usr/local/bin/SW42DRM
