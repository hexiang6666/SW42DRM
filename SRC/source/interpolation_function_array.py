#! /usr/bin/env python
import h5py
import scipy as sp
import time
import math
import pickle


#####################term 1: 1###########################################################
def fun_1(coordinate_x,coordinate_y,coordinate_z):
	return 1

#####################term 2: x#########################################################
def fun_2(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x

####################term 3: y##########################################################
def fun_3(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y

####################term 4: z##########################################################
def fun_4(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_z

###################term 5: x^2#########################################################
def fun_5(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x

###################term 6: y^2#########################################################
def fun_6(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_y

###################term 7: z^2#########################################################
def fun_7(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_z*coordinate_z

###################term 8: xy##########################################################
def fun_8(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x

##################term 9: yz###########################################################
def fun_9(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_z

#################term 10: xz###########################################################
def fun_10(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_z

#################term 11: xyz#########################################################
def fun_11(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_y*coordinate_z

#################term 12: x^3#########################################################
def fun_12(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_x

################term 13: y^3##########################################################
def fun_13(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_y*coordinate_y

################term 14: z^3#########################################################
def fun_14(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_z*coordinate_z*coordinate_z

################term 15: x^2y#########################################################
def fun_15(coordinate_x,coordinate_y, coordinate_z):
	return coordinate_x*coordinate_x*coordinate_y

###############term 16: xy^2#########################################################
def fun_16(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_y*coordinate_y

##############term 17: y^2z##########################################################
def fun_17(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_y*coordinate_z

##############term 18: yz^2##########################################################
def fun_18(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_z*coordinate_z

#############term 19: x^2z##########################################################
def fun_19(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_z

############term 20: xz^2###########################################################
def fun_20(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_z*coordinate_z

###########term 21: x^4#############################################################
def fun_21(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_x*coordinate_x

##########term 22: y^4#############################################################
def fun_22(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_y*coordinate_y*coordinate_y

##########term 23: z^4#############################################################
def fun_23(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_z*coordinate_z*coordinate_z*coordinate_z

#########term 24: x^3y############################################################
def fun_24(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_x*coordinate_y

#########term 25: x^3z############################################################
def fun_25(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_x*coordinate_z

########term 26: x^2y^2###########################################################
def fun_26(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_y*coordinate_y

#######term 27: x^2z^2############################################################
def fun_27(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_z*coordinate_z

######term 28: x^2yz##############################################################
def fun_28(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_x*coordinate_y*coordinate_z

######term 29: xy^3###############################################################
def fun_29(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_y*coordinate_y*coordinate_y

#######term 30:xz^3###############################################################
def fun_30(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_z*coordinate_z*coordinate_z

######term 31:xy^2z##############################################################
def fun_31(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_y*coordinate_y*coordinate_z

#####term 32:xyz^2###############################################################
def fun_32(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_x*coordinate_y*coordinate_z*coordinate_z

#####term 33:y^3z################################################################
def fun_33(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_y*coordinate_y*coordinate_z

######term 34:y^2z^2###############################################################
def fun_34(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_y*coordinate_z*coordinate_z

########term 35:yz^3##############################################################
def fun_35(coordinate_x,coordinate_y,coordinate_z):
	return coordinate_y*coordinate_z*coordinate_z*coordinate_z

fun_list=[fun_1,fun_2,fun_3,fun_4,fun_5,fun_6,fun_7,fun_8,fun_9,fun_10,fun_11,fun_12,fun_13,fun_14,fun_15,fun_16,fun_17,fun_18,fun_19,fun_20,fun_21,fun_22,fun_23,fun_24,fun_25,fun_26,fun_27,fun_28,fun_29,fun_30,fun_31,fun_32,fun_33,fun_34,fun_35]