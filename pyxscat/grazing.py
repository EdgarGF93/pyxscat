
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

LIMS_X = [-2,2]
LIMS_Y = [-2,2]
LIMS_Z = [-1,2]
LABEL_X = 'x'
LABEL_Y = 'y'
LABEL_Z = 'z'
UNIT_VECTOR_X = {'origin' : (-2,-2,0), 'length' : (1,0,0), 'name':'x'}
UNIT_VECTOR_Y = {'origin' : (-2,-2,0), 'length' : (0,1,0), 'name':'y'}
UNIT_VECTOR_Z = {'origin' : (-2,-2,0), 'length' : (0,0,1), 'name':'z'}


class GIGrid():
    def __init__(self):
        self.figure = plt.figure(figsize=(10,10))
        self.ax = self.figure.add_subplot(111, projection='3d')
   
    def init_grid(self):
        self.ax.set_xlim(LIMS_X)
        self.ax.set_ylim(LIMS_Y)
        self.ax.set_zlim(LIMS_Z)
        self.ax.set_xlabel(LABEL_X)
        self.ax.set_ylabel(LABEL_Y)
        self.ax.set_zlabel(LABEL_Z)
        self.ax.set_aspect("equal")
        self.ax.text(0,0,-0.1,s='sample')

    def draw_vector(self, dict_vector, color='black', length_ratio=0.1):
        origin_x = dict_vector['origin'][0]
        origin_y = dict_vector['origin'][1]
        origin_z = dict_vector['origin'][2]
        length_x = dict_vector['length'][0]
        length_y = dict_vector['length'][1]
        length_z = dict_vector['length'][2]

        self.ax.quiver(
            origin_x,
            origin_y,
            origin_z,
            length_x,
            length_y,
            length_z,
            color=color, 
            arrow_length_ratio=length_ratio,
        )
        text_x = origin_x+length_x
        text_y = origin_y+length_y
        text_z = origin_z+length_z

        self.ax.text(
            text_x,
            text_y,
            text_z,
            s=dict_vector['name'], 
            color='black',
        )

    def draw_vector_projections(self, dict_vector, color='black', length_ratio=0.1):
        # full vector
        v_x0 = dict_vector['origin'][0]
        v_y0 = dict_vector['origin'][1]
        v_z0 = dict_vector['origin'][2]
        v_xf = dict_vector['length'][0]
        v_yf = dict_vector['length'][1]
        v_zf = dict_vector['length'][2]
        
        # x projection
        vx_x0 = v_x0
        vx_y0 = v_y0
        vx_z0 = v_x0
        vx_xf = v_xf
        vx_yf = 0
        vx_zf = 0
        x_projection = {'origin' : (vx_x0,vx_y0,vx_z0), 'length' : (vx_xf,vx_yf,vx_zf), 'name':f"{dict_vector['name']}_x"}
        self.draw_vector(x_projection, 'grey')
        
        # y projection
        vy_x0 = v_x0
        vy_y0 = v_y0
        vy_z0 = v_x0
        vy_xf = 0
        vy_yf = v_yf
        vy_zf = 0
        y_projection = {'origin' : (vy_x0,vy_y0,vy_z0), 'length' : (vy_xf,vy_yf,vy_zf), 'name':f"{dict_vector['name']}_y"}
        self.draw_vector(y_projection, 'grey')

        # z projection
        vz_x0 = v_x0
        vz_y0 = v_y0
        vz_z0 = v_x0
        vz_xf = 0
        vz_yf = 0
        vz_zf = v_zf
        z_projection = {'origin' : (vz_x0,vz_y0,vz_z0), 'length' : (vz_xf,vz_yf,vz_zf), 'name':f"{dict_vector['name']}_z"}
        self.draw_vector(z_projection, 'grey')
        
        # xy projection
        vxy_x0 = v_x0
        vxy_y0 = v_y0
        vxy_z0 = v_x0
        vxy_xf = v_xf
        vxy_yf = v_yf
        vxy_zf = 0
        xy_projection = {'origin' : (vxy_x0,vxy_y0,vxy_z0), 'length' : (vxy_xf,vxy_yf,vxy_zf), 'name':f"{dict_vector['name']}_xy"}
        self.draw_vector(xy_projection, 'grey') 
        
        # xz projection (not draw)
        vxz_x0 = v_x0
        vxz_y0 = v_y0
        vxz_z0 = v_x0
        vxz_xf = v_xf
        vxz_yf = 0
        vxz_zf = v_zf
        xz_projection = {'origin' : (vxz_x0,vxz_y0,vxz_z0), 'length' : (vxz_xf,vxz_yf,vxz_zf), 'name':f"{dict_vector['name']}_xz"}
        # draw_vector(ax, xz_projection, 'cyan') 
        
        # yz projection (not draw)
        vyz_x0 = v_x0
        vyz_y0 = v_y0
        vyz_z0 = v_x0
        vyz_xf = 0
        vyz_yf = v_yf
        vyz_zf = v_zf
        yz_projection = {'origin' : (vyz_x0,vyz_y0,vyz_z0), 'length' : (vyz_xf,vyz_yf,vyz_zf), 'name':f"{dict_vector['name']}_yz"}
        # draw_vector(ax, yz_projection, 'cyan') 
        
        #v to vz line
        self.ax.plot([v_xf, vz_xf], [v_yf, vz_yf], [v_zf, vz_zf], color='grey', ls='--') 

        #v to vxy line
        self.ax.plot([v_xf, vxy_xf], [v_yf, vxy_yf], [v_zf, vxy_zf], color='grey', ls='--') 
        #v to vxz line
        self.ax.plot([v_xf, vxz_xf], [v_yf, vxz_yf], [v_zf, vxz_zf], color='grey', ls='--') 
        #v to vyz line
        self.ax.plot([v_xf, vyz_xf], [v_yf, vyz_yf], [v_zf, vyz_zf], color='grey', ls='--') 
        
        #vy to vyz line
        self.ax.plot([vy_xf, vyz_xf], [vy_yf, vyz_yf], [vy_zf, vyz_zf], color='grey', ls='--') 
        #vz to vyz line
        self.ax.plot([vz_xf, vyz_xf], [vz_yf, vyz_yf], [vz_zf, vyz_zf], color='grey', ls='--') 
        
        #vx to vxz line
        self.ax.plot([vx_xf, vxz_xf], [vx_yf, vxz_yf], [vx_zf, vxz_zf], color='grey', ls='--') 
        #vz to vxz line
        self.ax.plot([vz_xf, vxz_xf], [vz_yf, vxz_yf], [vz_zf, vxz_zf], color='grey', ls='--') 
        
        #x to xy line
        self.ax.plot([vx_xf, vxy_xf], [vx_yf, vxy_yf], [vx_zf, vxy_zf], color='grey', ls='--') 
        #y to xy line
        self.ax.plot([vy_xf, vxy_xf], [vy_yf, vxy_yf], [vy_zf, vxy_zf], color='grey', ls='--')  

    def draw_unit_vectors(self):
        self.draw_vector(UNIT_VECTOR_X)
        self.draw_vector(UNIT_VECTOR_Y)
        self.draw_vector(UNIT_VECTOR_Z)
    
    def draw_incoming_beam(self):
        INCOMING_BEAM = {'origin' : (-2,0,0), 'length' : (2,0,0), 'name' : 'ki'}
        self.draw_vector(INCOMING_BEAM, 'red')
    
    def draw_outcoming_beam(self):
        OUTCOMING_BEAM = {'origin' : (0,0,0), 'length' : (0.5,0.64,0.46), 'name' : 'kf'}
        self.draw_vector(OUTCOMING_BEAM, 'blue')
        self.draw_vector_projections(OUTCOMING_BEAM, 'cyan')