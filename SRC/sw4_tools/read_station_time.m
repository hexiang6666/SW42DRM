%#####################################usr input part######################################################################################
% file_path='/home/hexiang/SMR_work/smr/sw4_motion/M5.5_ESSI_srf.sw4output';    % absolute path of SW4 motion file

%################################################################################################################################################
% function t,No_time_step]=read_station(file_path,i,j,k)  % i is station_x_ID;  j is station_y_ID;  k is station_z_ID
function t=read_station_time(file_path,i,j,k)

% addpath(file_path);



file_prefix='E';
file_postfix_x='.x';
file_postfix_y='.y';
file_postfix_z='.z';



			x_str=num2str(i);
			y_str=num2str(j);
			z_str=num2str(k);
			if(i<10)
				x_str=strcat('0',x_str);
			end
			if(j<10)
				y_str=strcat('0',y_str);
			end
			if(k<10)
				z_str=strcat('0',z_str);
			end
			if(i>=100)
				disp('too many stations, check if codes need modified!');
			end

% #########################currently the filename format is E_060_012_001#############################
			x_str=strcat('0',x_str);
			y_str=strcat('0',y_str);
			z_str=strcat('0',z_str);
% ##############################################################################################
			
			str_element={file_prefix,x_str,y_str,z_str};
			filename=strjoin(str_element,{'_','_','_'});
			filename_x=strcat(filename,file_postfix_x);
			filename_y=strcat(filename,file_postfix_y);
			filename_z=strcat(filename,file_postfix_z);

			[u_x, dt, lat, lon, b, e, npts, year, jday, hour, min, sec, msec, cmpaz, cmpinc, idep, stnam ]=readsac(filename_x);
			% [u_y, dt, lat, lon, b, e, npts, year, jday, hour, min, sec, msec, cmpaz, cmpinc, idep, stnam ]=readsac(filename_y);
			% [u_z, dt, lat, lon, b, e, npts, year, jday, hour, min, sec, msec, cmpaz, cmpinc, idep, stnam ]=readsac(filename_z);
			% u=[u_x,u_y,u_z];
			t=dt;
			% No_time_step=npts;
end





			% ####################################### station information ##################################################################################
			% station_index=station_index+1;
			% station_index=(i+1)*(j+1)*(k+1);
			% station{(i+1)*(j+1)*(k+1),1}=i;
			% station{(i+1)*(j+1)*(k+1),2}=j;
			% station{(i+1)*(j+1)*(k+1),3}=k;
			% station{(i+1)*(j+1)*(k+1),4}=x_start_point+i*x_grid_space;
			% station{(i+1)*(j+1)*(k+1),5}=y_start_point+j*y_grid_space;
			% station{(i+1)*(j+1)*(k+1),6}=z_start_point+k*z_grid_space;
			% 
			% #############################################################################################################################################

% 			if((i==0)&&(j==0)&&(k==0))
% 				u_total=b:dt:(dt*(npts-1));
% 				u_total=u_total';
% 			end

% 			% if((i==0)&&(j==0)&&(k==0))
% 			%  	time=b:dt:(dt*(npts-1));
% 			%  	time=time';
% 			% end

% 			u_total=[u_total,u_x,u_y,u_z];
% 			% u_parallel(:,1,i+1,j+1,k+1)=u_x(:,1);
% 			% u_parallel(:,2,i+1,j+1,k+1)=u_y(:,1);
% 			% u_parallel(:,3,i+1,j+1,k+1)=u_z(:,1);
% 			% clear u_x, u_y, u_z, dt, lat, lon, b, e, npts, year, jday, hour, min, sec, msec, cmpaz, cmpinc, idep, stnam;
% 			u_x=[];
% 			u_y=[];
% 			u_z=[];
% 			dt=[];
% 			lat=[];
% 			lon=[];
% 			b=[];
% 			e=[];
% 			npts=[];
% 			year=[];
% 			jday=[];
% 			hour=[];
% 			min=[];
% 			sec=[];
% 			msec=[];
% 			cmpaz=[];
% 			cmpinc=[];
% 			idep=[];
% 			stnam=[];
% 		end
% 	end
% end

% end

% spmd
%   x = labindex;
% end

% time=linspace(0,total_time,No_time_step);
% time=time';

% ulocal = [u_parallel{:}];   % ulocal is a 5-D variable: first number is rows; second number is columns; third number is x station index; 4th number is y station index; 5th number is z station index  
% u_dis=[];
% for i1=0:No_node_x
% 	for i2=0:No_node_y
% 		for i3=0:No_node_z
% 			u_temp=ulocal(:,:,i1+1,i2+1,i3+1);
% 			if((i1==0)&&(i2==0)&&(i3==0))
% 				u_dis=[time,u_dis]
% 			end
% 			u_dis=[u_dis,u_temp];
% 		end
% 	end
% end	
% % ulocal=[time,ulocal];



% ##############################save the output file###########################################################################
% save /home/hexiang/SMR_work/smr/sw4_motion/SW42DRM/data/u_total.txt u_total -ascii;   % u_total has 4 columns: 1 time-value and 3 motion component
% save /home/hexiang/SMR_work/smr/sw4_motion/SW42DRM/data/station.txt station -ascii;   % station variable has 6 columns: first 3 columns are station ID in x, y and z direction; next 3 columns are station coordinates in x,y,z direction
