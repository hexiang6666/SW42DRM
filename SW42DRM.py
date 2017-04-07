#! /usr/bin/env python
import h5py
import scipy as sp
import time
import pickle

from ESSI_location import * 
from interpolation_function_array import *
from numpy.linalg import inv

model_name="test_model_development"
DRM_hdf5_filename=model_name+".h5.drminput"

# f=open('new_DRM_nodes.p','r')
# new_DRM_nodes=pickle.load(f);
# f.close;
No_new_node=new_node.shape[0]
boundary_node=sp.loadtxt("boundary_node.txt",dtype=sp.int32)
exterior_node=sp.loadtxt("exterior_node.txt",dtype=sp.int32)
element=sp.loadtxt("DRM_element.txt",dtype=sp.int32)
u_total=sp.loadtxt("u_total.txt")

############################################ Generate time data #####################################
No_time_step=u_total.shape[0]
time_step= u_total[1,0]-u_total[0,0]

# print u_total[0,0], u_total[1,0], No_time_step
Time=sp.zeros((No_time_step))
for i3 in xrange(0,No_time_step):
	Time[i3]=u_total[i3,0]
####################################################################################################

######################################### generate DRM node and element data########################

Ne=exterior_node.shape[0]
Nb=boundary_node.shape[0]
Nt=Ne+Nb

Exterior_node=sp.zeros((Ne))
Boundary_node=sp.zeros((Nb))

for i1 in xrange(0,Ne):
	Exterior_node[i1]=exterior_node[i1,0]
for i2 in xrange(0,Nb):
	Boundary_node[i2]=boundary_node[i2,0]

all_nodes=sp.hstack((Boundary_node,Exterior_node))
is_boundary_node=sp.zeros(Nt, dtype=sp.int32)
is_boundary_node[0:Nb]=1

######################################################################################################

#################################### generate displacement and acceleration data ###################
station_grid_space=10;
search_scale=1.1;
Interpolation_Radius=station_grid_space*search_scale;
scale_ratio=1.2;
	############search all interpolation nodes#####################################################
def interpolation_nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio):
	No_station=station.shape[0];
	interpolation_nodes=[];
	interpolation_nodes_index=0
	for i4 in xrange(0,No_station):
		selected_points=sp.zeros((7));
		if (station[i4,3]-new_node_x)*(station[i4,3]-new_node_x)+(station[i4,4]-new_node_y)*(station[i4,4]-new_node_y)+(station[i4,5]-new_node_z)*(station[i4,5]-new_node_z)<=Interpolation_Radius*Interpolation_Radius:
			selected_points[0:6]=station[i4,0:6]
			selected_points[6]=i4;
			interpolation_nodes.append(selected_points);
			interpolation_nodes_index=interpolation_nodes_index+1
	# print interpolation_nodes,interpolation_nodes_index,"I am here"
	while interpolation_nodes_index<4:
		print "serach radius R is too small for node ", new_node_index, ", search again using",scale_ratio, "*R..."
		Interpolation_Radius=Interpolation_Radius*scale_ratio
		interpolation_nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio)
	while interpolation_nodes_index>35:
		print "serach radius R is too big for node ", new_node_index, ", search again using R/",scale_ratio,"..."
		Interpolation_Radius=Interpolation_Radius/scale_ratio
		interpolation_nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio)
	print "Done interpolation nodes searching"
	return interpolation_nodes


def interpolated_motion(interpolation_nodes,new_node_x,new_node_y,new_node_z,u_total):
	# No_station=(u_total.shape[1]-1)/3;
	No_interpolation_nodes=len(interpolation_nodes)
	No_time_step=u_total.shape[0]
	node_motion_component=sp.zeros((3,No_time_step))

	for i7 in xrange(0,No_time_step):  
	# for i7 in xrange(0,1): 
		for i6 in xrange(0,3):  # 0 1 2 for ux uy uz
			RHS=sp.zeros((No_interpolation_nodes,1))
			LHS=[]
			for i5 in xrange(0,No_interpolation_nodes):
				LHS_component=sp.zeros((No_interpolation_nodes))
				for i12 in xrange(0,No_interpolation_nodes):
					LHS_component[i12]=fun_list[i12](interpolation_nodes[i5][3],interpolation_nodes[i5][4],interpolation_nodes[i5][5])
				# print LHS_component, "\n"
				LHS.append(LHS_component)
				RHS_column=int(interpolation_nodes[i5][6]*3+i6+1)
				RHS[i5,0]=u_total[i7][RHS_column]
			LHS=sp.array(LHS)
	 		# print RHS,"\n"
	 		# print LHS,"\n"
			inv_LHS=inv(LHS)
			interpolation_parameter=np.dot(inv_LHS, RHS)
			# print interpolation_parameter, "\n"
			motion=0;
			for i8 in xrange(0,No_interpolation_nodes):
				motion=motion+interpolation_parameter[i8,0]*fun_list[i8](new_node_x,new_node_y,new_node_z)
			node_motion_component[i6,i7]=motion
	return node_motion_component

	#####################finally generate motion for every DRM node##############################################
node_motion=[]

for i9 in xrange(0,No_new_node):
# for i9 in xrange(0,3):
	interpolation_nodes=interpolation_nodes(station,new_node[i9,1],new_node[i9,2],new_node[i9,3],Interpolation_Radius,(i9+1),scale_ratio)
	node_motion_component=interpolated_motion(interpolation_nodes,new_node[i9,1],new_node[i9,2],new_node[i9,3],u_total)
	node_motion.append(node_motion_component)

node_motion=sp.array(node_motion)


#############################from displacement generate velocity and acceleration#############################
u=sp.zeros((3*Nt,No_time_step))
v=sp.zeros((3*Nt,No_time_step))
for i10 in xrange(1,No_time_step):
	v[:,i10]=(node_motion[:,i10]-node_motion[:,i10-1])/time_step
for i11 in xrange(1,No_time_step):
	a[:,i11]=(v[:,i11]-v[:,i11-1])/time_step


############################################write output hdf5 file###################################
h5file=h5py.File(DRM_hdf5_filename,"w")
h5file.create_dataset("Elements", data=element)
h5file.create_dataset("DRM Nodes", data=all_nodes)
h5file.create_dataset("Is Boundary Node", data=is_boundary_node)
h5file.create_dataset("Number of Exterior Nodes", data=Ne)
h5file.create_dataset("Number of Boundary Nodes", data=Nb)
h5file.create_dataset("Time", data=Time)
h5file.create_dataset("Accelerations", data=a)
h5file.create_dataset("Displacements", data=node_motion)

h5file.close()
##################################################################################################




























