# -*- coding: utf-8 -*-
# @Author: hexiang
# @Date:   2017-11-11 17:02:03
# @Last Modified by:   hexiang6666
# @Last Modified time: 2017-12-03 02:30:29


#! /usr/bin/env python

import h5py
import scipy as sp
import time
import pickle
import sys
import math

from obspy import read

######################### usr input variable ###################################################################
if len(sys.argv)<2:
	print "Please specify DRM input file...";
	sys.exit();

if len(sys.argv)>2:
	print "Too many input argument..."; 
	sys.exit();

if len(sys.argv)==2:
	meta_info = str(sys.argv[1]);

DRM_input_tag = False; 

sw4_motion_path_tag = False; 

reference_station_tag = False; 

ESSI_box_size_tag = False; 

ESSI_nodes_spacing_tag = False; 

sample_time_step_interval_tag = False; 

base_point_ESSI_tag = False; 

base_point_sw4_translation_tag = False; 

base_point_sw4_rotation_tag = False; 

rotation_degree_tag = False; 

NO = 'NO'; 

no = 'no';

No = 'No'; 

n = 'n'; 

N = 'N'; 

yes = 'yes'; 

with open(meta_info) as f_in:
    lines = (line.rstrip() for line in f_in) # All lines including the blank ones
    lines = list(line for line in lines if line) # Non-blank lines


for x in xrange(0,len(lines)):
	
	if not lines[x].startswith('#'):

		data = lines[x].split('::')

		if data[0] == 'DRM input':
			
			DRM_input = data[1]; 

			DRM_input = DRM_input.strip();  

			DRM_input_tag = True; 

		elif data[0] == 'SW4 motion directory':
			
			sw4_motion_path = data[1]; 

			sw4_motion_path = sw4_motion_path.strip(); 

			sw4_motion_path_tag = True; 

		elif data[0] == 'origin coordinates of ESSI box (x, y, z)': 

			Reference_station = eval(data[1]);

			if len(Reference_station) != 3:

				print "Input format error! Please follow the format (x, y, z).\n";

				sys.exit(); 

			Reference_station_x = Reference_station[0];

			Reference_station_y = Reference_station[1]; 

			Reference_station_z = Reference_station[2];

			reference_station_tag = True; 

		elif data[0] == 'dimensions of ESSI Box (length, width, height)':

			ESSI_Box_size = eval(data[1]);

			if len(ESSI_Box_size) != 3:

				print "Input format error! Please follow the format (length, width, height). \n";

				sys.exit(); 

			ESSI_Box_length = ESSI_Box_size[0]; 

			ESSI_Box_width = ESSI_Box_size[1]; 

			ESSI_Box_height = ESSI_Box_size[2]; 

			ESSI_box_size_tag = True; 

		elif data[0] == 'spacing of ESSI nodes':

			ESSI_nodes_x_spacing = eval(data[1]);

			ESSI_nodes_y_spacing = ESSI_nodes_x_spacing; 

			ESSI_nodes_z_spacing = ESSI_nodes_x_spacing; 

			ESSI_nodes_spacing_tag = True; 

		elif data[0] == 'interval of time steps for sampling':

			sample_time_step_interval = eval(data[1]); 

			sample_time_step_interval_tag = True; 

		elif data[0] == 'reference point in ESSI model for translational transformation (x, y, z)': 

			Base_point_ESSI = eval(data[1]); 

			if len(Base_point_ESSI) != 3:

				print "Input format error! Please follow the format (x, y, z). \n";

				sys.exit(); 

			base_point_x = Base_point_ESSI[0]; 

			base_point_y = Base_point_ESSI[1]; 

			base_point_z = Base_point_ESSI[2];

			base_point_ESSI_tag = True; 

		elif data[0] == 'reference point in SW4 model for translational transformation (x, y, z)': 

			Base_point_SW4_translation = eval(data[1]); 

			if len(Base_point_SW4_translation) != 3 :

				print "Input format error! Please follow the format (x, y, z). \n";

				sys.exit(); 

			translation_base_station_x = Base_point_SW4_translation[0]; 

			translation_base_station_y = Base_point_SW4_translation[1]; 

			translation_base_station_z = Base_point_SW4_translation[2]

			base_point_sw4_translation_tag = True; 

		elif data[0] == 'conduct rotational transformation (yes/no)': 

			Base_point_SW4_rotation = eval(data[1])

			if ( (Base_point_SW4_rotation == NO ) or (Base_point_SW4_rotation == No) or (Base_point_SW4_rotation == no) or (Base_point_SW4_rotation == n) or (Base_point_SW4_rotation == N)):
				
				rotation_base_station_x = translation_base_station_x; 

				rotation_base_station_y = translation_base_station_y; 

				rotation_base_station_z = translation_base_station_z; 

				x_rotation = 0;

				y_rotation = 0; 

				z_rotation = 0; 

				base_point_sw4_rotation_tag = True; 

				rotation_degree_tag = True; 

			else: 

				base_point_sw4_rotation_tag = False;

				rotation_degree_tag = False; 

		elif ((data[0] == 'reference point in SW4 model for rotational transformation (x, y, z)') and (base_point_sw4_rotation_tag == False)):

			rotation_base = eval(data[1]); 

			if len(rotation_base) != 3:
			
				print "Input format error! Please follow the format (x, y, z). \n";

				sys.exit(); 

			rotation_base_station_x = rotation_base[0];

			rotation_base_station_y = rotation_base[1]; 

			rotation_base_station_z = rotation_base[2]; 

			base_point_sw4_rotation_tag = True; 

		elif ((data[0] == 'degrees of rotation along three axes (x, y, z)' ) and (rotation_degree_tag == False) ):

			rotation = eval(data[1]);  

			if len(rotation_base) != 3:
			
				print "Input format error! Please follow the format (x, y, z). \n";

				sys.exit(); 

			x_rotation = rotation[0]; 

			y_rotation = rotation[1]; 

			z_rotation = rotation[2]; 

			rotation_degree_tag = True; 

		else: 

			print "Unknown parameters ", data[0], ". Check your input file!\n"; 

if not (DRM_input_tag and sw4_motion_path_tag and reference_station_tag and ESSI_box_size_tag and ESSI_nodes_spacing_tag and sample_time_step_interval_tag and base_point_ESSI_tag and base_point_sw4_translation_tag and rotation_degree_tag): 

	print "Input arguments are not initialized properly, check inout files. \n"



# print "Verification:\n DRM_input::", DRM_input, "\n SW4 motion::", sw4_motion_path, "\n Reference_station_x::", Reference_station_x, "\n Reference_station_y::", Reference_station_y, "\n Reference_station_z::", Reference_station_z, "\n";

# print "ESSI_Box_length::", ESSI_Box_length, "\n ESSI_Box_width::", ESSI_Box_width, "\n ESSI_Box_height", ESSI_Box_height, "\n"; 

# print "ESSI_nodes_x_spacing::", ESSI_nodes_x_spacing, "\n ESSI_nodes_y_spacing::", ESSI_nodes_y_spacing, "\n ESSI_nodes_z_spacing", ESSI_nodes_z_spacing, "\n";  

# print "sample_time_step_interval::", sample_time_step_interval, "\n"; 

# print "ESSI_base_point_x::", base_point_x, "\n ESSI_base_point_y::", base_point_y, "\n ESSI_base_point_z::", base_point_z, "\n"; 

# print "translation_base_station_x::", translation_base_station_x, "\n translation_base_station_y::", translation_base_station_y, "\n translation_base_station_z::", translation_base_station_z, "\n"; 

# print "rotation_base_station_x::", rotation_base_station_x, "\n rotation_base_station_y::", rotation_base_station_y, "\n rotation_base_station_z::", rotation_base_station_z; 

# print "x_rotation::", x_rotation, "\n y_rotation::", y_rotation, "\n z_rotation::", z_rotation; 



############# Take information of SW4 motion ###########################################################

# sw4_motion_path=raw_input('\nSpecify the sw4 motion directory: '); 


########## Take information of origin of ESSI box #######################################################

##### Type 1: terminal input for individial component  

# Reference_station_x= input('Enter the x coordinate of reference station, whose station ID=(0 0 0): ');

# Reference_station_y= input('Enter the y coordinate of reference station, whose station ID=(0 0 0): ');

# Reference_station_z= input('Enter the z coordinate of reference station, whose station ID=(0 0 0): ');

##### Type 2: terminal input for whole location vector 

# Reference_station = input('Specify the origin coordinates of ESSI box (x, y, z):  ');

# if len(Reference_station) != 3:

# 	print "Input format error! Please follow the format (x, y, z). \n";

# 	sys.exit(); 

# Reference_station_x = Reference_station[0];

# Reference_station_y = Reference_station[1]; 

# Reference_station_z = Reference_station[2]; 


##### Type 3: file input for whole location vector  




################### Take information of dimension information of ESSI box #########################

###### Type 1: terminal input for individual dimension component 

# ESSI_Box_length= input('Enter the length (x direction) of ESSI Box: ');

# ESSI_Box_width= input('Enter the width (y direction) of ESSI Box: ');

# ESSI_Box_height= input('Enter the height (z direction) of ESSI Box: ');

##### Type 2: terminal input for whole dimension vector 

# ESSI_Box_size = input('Specify the dimensions of ESSI Box (length, width, height):  ');

# if len(ESSI_Box_size) != 3:

# 	print "Input format error! Please follow the format (length, width, height). \n";

# 	sys.exit(); 

# ESSI_Box_length = ESSI_Box_size[0]; 

# ESSI_Box_width = ESSI_Box_size[1]; 

# ESSI_Box_height = ESSI_Box_size[2]; 

##### Type 3: file input for the whole dimension vector


################### Take information of spacing information of ESSI nodes #########################

###### Type 1: terminal input for individual dimension component

# ESSI_nodes_x_spacing= input('Enter the spacing of ESSI nodes in x direction: ');  

# ESSI_nodes_y_spacing= input('Enter the spacing of ESSI nodes in y direction: ');

# ESSI_nodes_z_spacing= input('Enter the spacing of ESSI nodes in z direction: ');


###### Type 2: terminal input for whole vector dimension component

# ESSI_nodes_x_spacing= input('Enter the spacing of ESSI nodes:  ');

# ESSI_nodes_y_spacing = ESSI_nodes_x_spacing; 

# ESSI_nodes_z_spacing = ESSI_nodes_x_spacing; 

###### Type 3: file input for whole vector dimension component


#################### Take information of time steps interval samping #############################

###### Type 1: terminal input for sample time step interval 

# sample_time_step_interval=input('Specify the interval of time steps for sampling:  ');

###### Type 2: file input for sample time step interval 



# ################### Take information of ESSI reference point ######################################

###### Type 1: terminal input for individual component ESSI reference point 

# base_point_x=input('Specify the x coordinate of the base point in ESSI model: ');
# base_point_y=input('Specify the y coordinate of the base point in ESSI model: ');
# base_point_z=input('Specify the z coordinate of the base point in ESSI model: ');

###### Type 2: terminal input for the whole vector dimension component 

# Base_point_ESSI = input('Specify reference point in ESSI model for translational transformation (x, y, z):  ');

# if len(Base_point_ESSI) != 3:

# 	print "Input format error! Please follow the format (x, y, z). \n";

# 	sys.exit(); 

# base_point_x = Base_point_ESSI[0]; 

# base_point_y = Base_point_ESSI[1]; 

# base_point_z = Base_point_ESSI[2]; 

###### Type 3: file input for whole vector dimension component

################# Take information of SW4 translational reference point ################################################################

#### Type 1: terminal input for the whole vector dimension component 

# Base_point_SW4_translation = input('Specify reference point in SW4 model for translational transformation (x, y, z):  ');

# if len(Base_point_SW4_translation) != 3:

# 	print "Input format error! Please follow the format (x, y, z). \n";

# 	sys.exit(); 

# translation_base_station_x = Base_point_SW4_translation[0]; 

# translation_base_station_y = Base_point_SW4_translation[1]; 

# translation_base_station_z = Base_point_SW4_translation[2]; 


#### Type 2: file input for whole vector dimension component 


################# Take information of SW4 rotational reference point ################################################################

###### Type 1: terminal input for the whole vector dimension component  

# NO = 'NO'; 

# no = 'no';

# No = 'No'; 

# Base_point_SW4_rotation = input('Specify reference point in SW4 model for rotational transformation: (x, y, z), type NO for no rotational transformation:  ');

# if (len(Base_point_SW4_rotation) != 2) and (len(Base_point_SW4_rotation)!= 3) :

# 	print "Input format error! \n";

# 	sys.exit(); 

# if (len(Base_point_SW4_rotation) == 2) : 

# 	if ( (Base_point_SW4_rotation == NO ) or (Base_point_SW4_rotation == No) or (Base_point_SW4_rotation == no) ):
	
# 		rotation_base_station_x = translation_base_station_x; 

# 		rotation_base_station_y = translation_base_station_y; 

# 		rotation_base_station_z = translation_base_station_z; 

# 		x_rotation = 0;

# 		y_rotation = 0; 

# 		z_rotation = 0; 

# 	else: 

# 		print "Input format error! \n";

# 		sys.exit(); 

# if len(Base_point_SW4_rotation) == 3:
	
# 	rotation_base_station_x = Base_point_SW4_rotation[0]; 

# 	rotation_base_station_y = Base_point_SW4_rotation[1];

# 	rotation_base_station_z = Base_point_SW4_rotation[2];

# 	Rotation = input('Specify the degrees of rotation along three axies (x, y, z):  ');

# 	if len(Rotation) != 3:

# 		print "Input format error! Please follow the format (x, y, z). \n";

# 		sys.exit(); 

# 	x_rotation = Rotation[0]; 

# 	y_rotation = Rotation[1]; 

# 	z_rotation = Rotation[2]; 


##### Type 2: file input for whole vector dimension output 





#################### Ending usr input part ####################################################################################


################################################################################################################################
############# Definition of intermediate function ##############################################################################
################################################################################################################################

######  Definition of getField function ##################################

def getField (new_node_x,new_node_y,new_node_z,new_node_index,sample_time_step_interval):

	original_velocity=sp.zeros((No_time_step,3));
	original_acceleration=sp.zeros((3,No_time_step));
	original_displacement=sp.zeros((3,No_time_step));
	sampled_displacement_component=sp.zeros((3,sampled_No_time_step));
	sampled_acceleration_component=sp.zeros((3,sampled_No_time_step));

	x_pos_id=int(sp.floor(abs(new_node_x-Reference_station_x)/ESSI_nodes_x_spacing))+1;
	x_neg_id=int(sp.floor(abs(new_node_x-Reference_station_x)/ESSI_nodes_x_spacing));
	y_pos_id=int(sp.floor(abs(new_node_y-Reference_station_y)/ESSI_nodes_y_spacing))+1;
	y_neg_id=int(sp.floor(abs(new_node_y-Reference_station_y)/ESSI_nodes_y_spacing));
	z_pos_id=int(sp.floor(abs(new_node_z-Reference_station_z)/ESSI_nodes_z_spacing))+1;
	z_neg_id=int(sp.floor(abs(new_node_z-Reference_station_z)/ESSI_nodes_z_spacing));

	u1=readstation(sw4_motion_path,x_pos_id,y_pos_id,z_pos_id);
	u2=readstation(sw4_motion_path,x_neg_id,y_pos_id,z_pos_id);
	u3=readstation(sw4_motion_path,x_pos_id,y_neg_id,z_pos_id);
	u4=readstation(sw4_motion_path,x_neg_id,y_neg_id,z_pos_id);
	u5=readstation(sw4_motion_path,x_pos_id,y_pos_id,z_neg_id);
	u6=readstation(sw4_motion_path,x_neg_id,y_pos_id,z_neg_id);
	u7=readstation(sw4_motion_path,x_pos_id,y_neg_id,z_neg_id);
	u8=readstation(sw4_motion_path,x_neg_id,y_neg_id,z_neg_id);



	u1=sp.array(u1);
	u2=sp.array(u2);
	u3=sp.array(u3);
	u4=sp.array(u4);
	u5=sp.array(u5);
	u6=sp.array(u6);	
	u7=sp.array(u7);
	u8=sp.array(u8);

	###### for 8 node brick, some notation is listed here: node 1 (+1, +1, +1); node 2 (-1,+1,+1); node 3 (+1, -1, +1); node 4 (-1, -1, +1); node 5 (+1, +1, -1); node 6 (-1, +1, -1); node 7(+1, -1, -1); node 8 (-1,-1,-1)
	x1=x_pos_id*ESSI_nodes_x_spacing+Reference_station_x;

	y1=y_pos_id*ESSI_nodes_y_spacing+Reference_station_y;
	
	z1=z_pos_id*ESSI_nodes_z_spacing+Reference_station_z;

	x2=x_neg_id*ESSI_nodes_x_spacing+Reference_station_x;

	y4=y_neg_id*ESSI_nodes_y_spacing+Reference_station_y;

	z5=z_neg_id*ESSI_nodes_z_spacing+Reference_station_z;

	kexi=(2*new_node_x-(x1+x2))/(x1-x2);   ### local coordinate in x direction
	yita=(2*new_node_y-(y1+y4))/(y1-y4);   ### local coordinate in y direction
	zeta=(2*new_node_z-(z1+z5))/(z1-z5);   ### local coordinate in z direction


	N1=1.0/8.0*(1+kexi)*(1+yita)*(1+zeta);  ### be careful that by 1/8 will be evaulated as 0 not 0.125
	N2=1.0/8.0*(1-kexi)*(1+yita)*(1+zeta);
	N3=1.0/8.0*(1+kexi)*(1-yita)*(1+zeta);
	N4=1.0/8.0*(1-kexi)*(1-yita)*(1+zeta);
	N5=1.0/8.0*(1+kexi)*(1+yita)*(1-zeta);
	N6=1.0/8.0*(1-kexi)*(1+yita)*(1-zeta);
	N7=1.0/8.0*(1+kexi)*(1-yita)*(1-zeta);
	N8=1.0/8.0*(1-kexi)*(1-yita)*(1-zeta);

	# print "Immediate result",N1, N2, N3, N4, N5, N6, N7, N8;


	original_velocity=N1*u1+N2*u2+N3*u3+N4*u4+N5*u5+N6*u6+N7*u7+N8*u8;



	# print "original_velocity", original_velocity;

	original_velocity=sp.array(original_velocity);

	original_velocity=original_velocity.transpose();

	# print original_velocity[0,4500]

	# print "shape is: ", original_velocity.shape

	for x10 in xrange(1,No_time_step):
		original_displacement[:,x10]=original_displacement[:,x10-1]+original_velocity[:,x10]*original_time_step;
		original_acceleration[:,x10]=(original_velocity[:,x10]-original_velocity[:,x10-1])/original_time_step;

	# print "original_dis", original_displacement;
	# print "original_acc", original_acceleration;

	for x11 in xrange(0,sampled_No_time_step):
		sampled_displacement_component[:,x11]=original_displacement[:,x11*sample_time_step_interval];
		sampled_acceleration_component[:,x11]=original_acceleration[:,x11*sample_time_step_interval];



	print "Done with ground motion interpolation for node # ", new_node_index, "!!";

	# print "sampled_dis","sampled_acc",sampled_displacement_component, sampled_acceleration_component

	return sampled_displacement_component,sampled_acceleration_component;


###############################################################################################################################################################

def readstation(sw4_motion_path, x_id, y_id, z_id):   ### return the velocity (with three columns, three directions x, y and z)
	
	file_prefix='/E';
	file_postfix_x='.x';
	file_postfix_y='.y';
	file_postfix_z='.z';

	x_str=str(x_id);
	y_str=str(y_id);
	z_str=str(z_id);
	
	if x_id<10:
		x_str= '0' + x_str;
	
	if y_id<10: 
		y_str= '0' + y_str;
			
	if z_id<10: 
		z_str= '0' + z_str;

	if x_id>=100: 
		print 'Too many stations, check if codes need modified!';

	if y_id>=100:
		print 'Too many stations, check if codes need modified!';
	
	if z_id>=100:
		print 'Too many stations, check if codes need modified!';

	filename = file_prefix + '_0' + x_str + '_0' + y_str + '_0' + z_str; 

	filename_x = sw4_motion_path + filename + file_postfix_x ;

	filename_y = sw4_motion_path + filename + file_postfix_y ; 

	filename_z = sw4_motion_path + filename + file_postfix_z ; 

	sac_info_x = read(filename_x, debug_headers=True); 

	sac_info_y = read(filename_y, debug_headers=True); 

	sac_info_z = read(filename_z, debug_headers=True); 

	vx = sac_info_x[0].data; 

	vy = sac_info_y[0].data; 

	vz = sac_info_z[0].data; 

	vy = -1*vy;

	vz = -1*vz; 

	# vel = sp.concatenate((vx, vy, vz), axis= 1); 

	vel = zip(vx, vy, vz); 

	vel = sp.array(vel); 

	return vel;  


##### Define rotational coordinate transformation 

##### ATTENTION: ROTATION ARE PATH DEPENDENT, please take care the order of calling 3 rotation functions ##########################################
	
	#######################################rotation along z axis###########################################################
def rotation_z(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,z_rotation):

	No_new_node=new_node.shape[0];
	for i4 in xrange(0,No_new_node):
		dx=new_node[i4,1]-rotation_base_station_x
		dy=new_node[i4,2]-rotation_base_station_y
		dz=new_node[i4,3]-rotation_base_station_z
	
		r_xy=math.sqrt(dx*dx+dy*dy)

		if dx==0 and dy>=0:
			theta=90;
		if dx==0 and dy<0:
			theta=270;
		if dx>0 and dy>=0:
			theta=sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		if dx>0 and dy<0:
			theta=2*sp.pi+sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		if dx<0 and dy>=0:
			theta=sp.pi+sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		if dx<0 and dy<0:
			theta=sp.pi+sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		new_theta=theta+z_rotation;
		new_dx=r_xy*math.cos(new_theta*sp.pi/180.0);
		new_dy=r_xy*math.sin(new_theta*sp.pi/180.0);
		new_dz=dz;

		new_node[i4,1]=rotation_base_station_x+new_dx
		new_node[i4,2]=rotation_base_station_y+new_dy
		new_node[i4,3]=rotation_base_station_z+new_dz
	return new_node

	#####################################rotation along x axis###########################################################
def rotation_x(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,x_rotation):

	No_new_node=new_node.shape[0];
	for i5 in xrange(0,No_new_node):
		dx=new_node[i5,1]-rotation_base_station_x
		dy=new_node[i5,2]-rotation_base_station_y
		dz=new_node[i5,3]-rotation_base_station_z
		r_yz=math.sqrt(dy*dy+dz*dz)

		if dy==0 and dz>=0:
			theta=90;
		if dy==0 and dz<0:
			theta=270;
		if dy>0 and dz>=0:
			theta=sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		if dy>0 and dz<0:
			theta=2*sp.pi+sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		if dy<0 and dz>=0:
			theta=sp.pi+sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		if dy<0 and dz<0:
			theta=sp.pi+sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		new_theta=theta+x_rotation;
		new_dy=r_yz*math.cos(new_theta*sp.pi/180.0);
		new_dz=r_yz*math.sin(new_theta*sp.pi/180.0);
		new_dx=dx;
		new_node[i5,1]=rotation_base_station_x+new_dx
		new_node[i5,2]=rotation_base_station_y+new_dy
		new_node[i5,3]=rotation_base_station_z+new_dz
	return new_node


	######################################rotation along y axis#########################################################
def rotation_y(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,y_rotation):
		
	No_new_node=new_node.shape[0];
	for i6 in xrange(0,No_new_node):
		dx=new_node[i6,1]-rotation_base_station_x
		dy=new_node[i6,2]-rotation_base_station_y
		dz=new_node[i6,3]-rotation_base_station_z
		r_xz=math.sqrt(dx*dx+dz*dz)
		if dz==0 and dx>=0:
			theta=90;
		if dz==0 and dx<0:
			theta=270;
		if dz>0 and dx>=0:
			theta=sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		if dz>0 and dx<0:
			theta=2*sp.pi+sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		if dz<0 and dx>=0:
			theta=sp.pi+sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		if dz<0 and dx<0:
			theta=sp.pi+sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		new_theta=theta+y_rotation;
		new_dy=dy
		new_dz=r_xz*math.cos(new_theta*sp.pi/180.0);
		new_dx=r_xz*math.sin(new_theta*sp.pi/180.0);
		new_node[i6,1]=rotation_base_station_x+new_dx
		new_node[i6,2]=rotation_base_station_y+new_dy
		new_node[i6,3]=rotation_base_station_z+new_dz
	return new_node


###############################################################################################################################################################
################ Ending definition of intermediate function ####################################################################
###############################################################################################################################



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++ Beinnng of the main programe +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

################### Generates ESSI box station coordinates ############################### 

No_ESSI_nodes= (1+ESSI_Box_length/ESSI_nodes_x_spacing)*(1+ESSI_Box_width/ESSI_nodes_y_spacing)*(1+ESSI_Box_height/ESSI_nodes_z_spacing);

station=sp.zeros((No_ESSI_nodes,6));  # station will have 6 columns: first three columns is station ID in x y z direction; next three columns are station coordinates in x y z direction
station_index=0; 

for x1 in xrange(0,ESSI_Box_length/ESSI_nodes_x_spacing+1):
	for x2 in xrange(0,ESSI_Box_width/ESSI_nodes_y_spacing+1):
		for x3 in xrange(0,ESSI_Box_height/ESSI_nodes_z_spacing+1):
			station[station_index,0]=x1;
			station[station_index,1]=x2;
			station[station_index,2]=x3;
			station[station_index,3]=Reference_station_x+ESSI_nodes_x_spacing*x1;
			station[station_index,4]=Reference_station_y+ESSI_nodes_y_spacing*x2;
			station[station_index,5]=Reference_station_z+ESSI_nodes_z_spacing*x3;
			station_index=station_index+1;

################## Ending ESSI box station coordinates generation ####################################


####################################### Transfer the coordinates of DRM layer ######################################################################################## 

h5file=h5py.File(DRM_input,"r");

is_boundary_node = h5file['Is Boundary Node'][:]; 

coords = h5file['Coordinates'][:];

DRM_nodes = h5file['DRM Nodes'][:]; 

num_exterior_node = int(h5file['Number of Exterior Nodes'][:]);

num_boundary_node = int(h5file['Number of Boundary Nodes'][:]); 

h5file.close(); 

NO_node = num_boundary_node + num_exterior_node;

boundary_node = sp.zeros((num_boundary_node,6));  ## six columns: Node_ID, x, y, z, numdofs, 0/1. The last column is the tag to mark whether the node is boundary node or exterior node.  

exterior_node = sp.zeros((num_exterior_node,6)); ## six columns: Node_ID, x, y, z, numdofs, 0/1. The last column is the tag to mark whether the node is boundary node or exterior node.  

for x1 in xrange(0, num_boundary_node):

	node_tag = int(DRM_nodes[x1]); 

	boundary_node[x1,0] = node_tag;

	boundary_node[x1,1] = coords[3*x1];

	boundary_node[x1,2] = coords[3*x1+1];

	boundary_node[x1,3] = coords[3*x1+2];

	boundary_node[x1,4] = 3.0;

	boundary_node[x1,5] = 1.0; 

exterior_node_index = 0; 

for x2 in xrange(num_boundary_node, NO_node):

	node_tag = int(DRM_nodes[x2]); 

	exterior_node[exterior_node_index,0] = node_tag;

	exterior_node[exterior_node_index,1] = coords[3*x2];

	exterior_node[exterior_node_index,2] = coords[3*x2+1];

	exterior_node[exterior_node_index,3] = coords[3*x2+2];

	exterior_node[exterior_node_index,4] = 3.0;

	exterior_node[exterior_node_index,5] = 0.0; 

	exterior_node_index = exterior_node_index + 1; 

node=sp.concatenate((boundary_node,exterior_node))

		
for i in xrange(0,NO_node):   ### coordinates transformation
	node[i,2]=-node[i,2];
	node[i,3]=-node[i,3];
base_point_y=-base_point_y;
base_point_z=-base_point_z;


translation_x= translation_base_station_x-base_point_x;
translation_y= translation_base_station_y-base_point_y;
translation_z= translation_base_station_z-base_point_z;

new_node=sp.zeros((NO_node,6))

for i3 in xrange(0,NO_node):  ### Translational transformation

	new_node[i3,0]=node[i3,0]
	new_node[i3,1]=node[i3,1]+translation_x
	new_node[i3,2]=node[i3,2]+translation_y
	new_node[i3,3]=node[i3,3]+translation_z
	new_node[i3,4]=node[i3,4]
	new_node[i3,5]=node[i3,5]

### conduct rotational operation, here our rotate order is z ,x ,y
new_node=rotation_z(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,z_rotation)
new_node=rotation_x(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,x_rotation)
new_node=rotation_y(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,y_rotation)

#######################################  Ending transfer the coordinates of DRM layer ######################################################################################## 

####### Sampled time information #############

file_path = sw4_motion_path + "/E_000_000_000.x";   ### Open any file can get these information 

sac_info = read(file_path, debug_headers=True); 

No_time_step = sac_info[0].data.shape[0]; 

original_time_step = sac_info[0].stats.delta; 

sampled_time_step = original_time_step*sample_time_step_interval;

sampled_No_time_step= int(math.floor((No_time_step-1)/sample_time_step_interval)+1);

Time=[i*sampled_time_step for i in xrange(0,sampled_No_time_step)];

h5file=h5py.File(DRM_input,"r+")

h5file.create_dataset("Time", data=Time);


####### Calling getField() function conduct interpolation and calculate acceleration and displacement ################## 
No_new_node=new_node.shape[0]
         
sampled_acceleration=sp.zeros((1,sampled_No_time_step));
sampled_displacement=sp.zeros((1,sampled_No_time_step));

for i9 in xrange(0,No_new_node):
# for i9 in xrange(0,1):
	sampled_displacement_component,sampled_acceleration_component=getField(new_node[i9,1],new_node[i9,2],new_node[i9,3],new_node[i9,0],sample_time_step_interval);
	# print new_node[i9,1],new_node[i9,2],new_node[i9,3]
	sampled_acceleration=sp.concatenate((sampled_acceleration,sampled_acceleration_component))
	sampled_displacement=sp.concatenate((sampled_displacement,sampled_displacement_component))


sampled_acceleration=sp.array(sampled_acceleration)
sampled_displacement=sp.array(sampled_displacement)

h5file.create_dataset("Accelerations", data=sampled_acceleration[1:,:])
h5file.create_dataset("Displacements", data=sampled_displacement[1:,:])

h5file.close()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++ Ending of the main programe +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
