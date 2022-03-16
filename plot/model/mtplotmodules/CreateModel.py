from sys import platform
import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from tqdm import tqdm

import matplotlib
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['axes.unicode_minus'] = False
matplotlib.use('Agg')

class CreateModel:
    
    def __init__(self):
        self.base_path = os.getcwd()
        
        self.input_file = None
        self.sta_file = None
        self.eq_file = None
        
        self.cross_we = None
        self.cross_sn = None
        self.we_names = None
        self.sn_names = None
        
        self.eq_marker_size = 30
        self.select_line = {"x": [], "y": [], "z": []}
        self.kmtom = 1000
        self.fsize_title = 20
        self.fsize_axis = 20
        self.fsize_label = 20
        self.sta_coord = None
        self.pcm_color_min = 0
        self.cbar_ticks = None
        self.setOutputDPI(200)
        self.setOutputFormat('ps')
        self.cmap = plt.get_cmap('jet_r', 20)
    
    def setInputFile(self, file):
        self.input_file = file
        
    def setStationFile(self, file):
        self.sta_file = file
    
    def setEQFile(self, file):
        self.eq_file = file
            
    def __setOutputFolder(self):
        filename_as_foldername = os.path.basename(self.input_file)
        filename_as_foldername = filename_as_foldername.replace('.', '_')
        output_path = os.path.join(self.base_path, "{}/{}/".format("output", filename_as_foldername))
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        self.output_folder = output_path
        
    def setModelCenter(self, lat, lng):
        self.model_center = { 'lat': lat, 'lng': lng }
        
    def __getDistanceFromLatlng(self, lat1, lng1, lat2, lng2):
        # return distance in km
        R = 6371
        dLat = self.__deg2rad(lat2-lat1)
        dlng = self.__deg2rad(lng2-lng1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(self.__deg2rad(lat1)) * math.cos(self.__deg2rad(lat2)) * math.sin(dlng/2) * math.sin(dlng/2) 
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d

    def __deg2rad(self, deg):
        return deg * (math.pi/180)

    def __getXYDistance(self, center_lat, center_lng, lat2, lng2):
        x = self.__getDistanceFromLatlng(center_lat, center_lng, center_lat, lng2)
        y = self.__getDistanceFromLatlng(center_lat, center_lng, lat2, center_lng)
        if lng2<center_lng:
            x = x*-1
        if lat2<center_lat:
            y = y*-1
        return x, y
        
    def __readEQ(self, filename, recenter=True):
        eq_df = pd.read_csv(filename)
        eq_latitude = eq_df['latitude'].values
        eq_longitude = eq_df['longitude'].values
        eq_depth = eq_df['depth'].values
        n_eq = len(eq_latitude)
        eq_data = { 'lat': eq_latitude, 'lng': eq_longitude, 'depth': eq_depth }
        
        if recenter:
            we0 = np.zeros(n_eq, dtype=float)
            sn0 = np.zeros(n_eq, dtype=float)
            for i in range(n_eq):
                we0[i], sn0[i] = self.__getXYDistance(self.model_center['lat'], self.model_center['lng'], eq_latitude[i], eq_longitude[i])
            eq_data['we0'] = we0
            eq_data['sn0'] = sn0
        return eq_data
    
    def setEQRadius(self, radius_m):
        self.eq_radius = radius_m

    def __sliceEQ(self, axis, value, eq_data, eq_radius):
        n_eq = len(eq_data['we0'])

        if axis=='z':
            sliced_we0 = []
            sliced_sn0 = []
            sliced_depth = []
            for i in range(n_eq):
                delta = abs(eq_data['depth'][i]-value)
                if delta <= eq_radius:
                    sliced_we0.append(eq_data['we0'][i])
                    sliced_sn0.append(eq_data['sn0'][i])
                    sliced_depth.append(eq_data['depth'][i])
            return {'we0': np.array(sliced_we0), 'sn0': np.array(sliced_sn0), 'depth': np.array(sliced_depth)}
        elif axis=='sn':
            sliced_we0 = []
            sliced_sn0 = []
            sliced_depth = []
            for i in range(n_eq):
                delta = abs(eq_data['sn0'][i]-value)
                if delta <= eq_radius:
                    sliced_we0.append(eq_data['we0'][i])
                    sliced_sn0.append(eq_data['sn0'][i])
                    sliced_depth.append(eq_data['depth'][i])
            return {'we0': np.array(sliced_we0), 'sn0': np.array(sliced_sn0), 'depth': np.array(sliced_depth)}
        
        elif axis=='we':
            sliced_we0 = []
            sliced_sn0 = []
            sliced_depth = []
            for i in range(n_eq):
                delta = abs(eq_data['we0'][i]-value)
                if delta <= eq_radius:
                    sliced_we0.append(eq_data['we0'][i])
                    sliced_sn0.append(eq_data['sn0'][i])
                    sliced_depth.append(eq_data['depth'][i])
            return {'we0': np.array(sliced_we0), 'sn0': np.array(sliced_sn0), 'depth': np.array(sliced_depth)}
        
    def __readSta(self, filename, recenter):
        sta_df = pd.read_csv(filename)
        n_sta = len(sta_df)
        sta = {}
        for i in range(n_sta):
            sta[sta_df['name'][i]] = { 'lat': sta_df['latitude'][i], 'lng': sta_df['longitude'][i] }
            
        if recenter:
            for i in range(n_sta):
                we0, sn0 = self.__getXYDistance(self.model_center['lat'], self.model_center['lng'],\
                                              sta_df['latitude'][i], sta_df['longitude'][i])
                sta[sta_df['name'][i]]['we0'] = we0
                sta[sta_df['name'][i]]['sn0'] = sn0
        return sta
              
    def __setStaCoord(self, x, y):
        self.sta_coord = { "x": x, "y": y }
    
    def setCrossSN(self, values):
        self.cross_sn = np.array(values)
    
    def setCrossWE(self,values):
        self.cross_we = np.array(values)
        
    def setCrossZ(self,values):
        self.cross_z = np.array(values)
        
    def setNameSN(self, names):
        self.sn_names = names
        
    def setNameWE(self, names):
        self.we_names = names
    
    def setOutputFormat(self, output_format):
        self.output_format = output_format
    
    def setOutputDPI(self, output_dpi):
        self.output_dpi = output_dpi
    
    def setSNLim(self, min_val, max_val):
        self.sn_lim = (min_val, max_val)
    
    def setWELim(self, min_val, max_val):
        self.we_lim = (min_val, max_val)
        
    def setZLim(self, min_val, max_val):
        self.z_lim = (min_val, max_val)
        
    def __readModel(self, file):
        row_title = 0
        row_number = 1
        row_data = 2
        result = {}

        with open(file, 'r') as f:
            rows = f.readlines()

            # title
            line_0 = rows[row_title]
            for r in (("#Iteration No.", "iter_no"), ("RMS =", "rms"), ("LM =","lm")):
                line_0 = line_0.replace(*r)
            line_0 = line_0.split()
            for i in range(len(line_0)):
                if line_0[i]=="iter_no":
                    try:
                        result["iter_no"] = int(line_0[i+1])
                    except:
                        raise TypeError("Iteration is not integer")
                elif line_0[i]=="rms":
                    try:
                        result["rms"] = float(line_0[i+1])
                    except:
                        raise TypeError("rms is not a number")
                elif line_0[i]=="lm":
                    try:
                        result["lm"] = float(line_0[i+1])
                    except:
                        raise TypeError("rms is not a number")

            # number of block
            line_1 = rows[row_number].split()
            for i in range(len(line_1)):
                try:
                    line_1[i] = int(line_1[i])
                except:
                    raise TypeError("Number of block is not integer")

            nx = line_1[0]
            ny = line_1[1]
            nz = line_1[2]
            nr = line_1[3]

            if nr!=0:
                raise ValueError("nr is not 0")

            nSize = nx+ny+nz+nr

            # line 2 and so on
            value_id = 0
            size_x = []
            size_y = []
            size_z = []
            resistivity = [] 
            for i in range(row_data, len(rows)):
                if rows[i]!="" and rows[i]!="\n":
                    for data in rows[i].split():
                        try:
                            data = float(data)
                        except:
                            raise TypeError("value is not float")

                        if value_id <= nx-1:
                            size_x.append(data/self.kmtom)
                        elif value_id > nx-1 and value_id <= (nx+ny-1):
                            size_y.append(data/self.kmtom)
                        elif value_id > ny-1 and value_id <= (nx+ny+nz-1):
                            size_z.append(data/self.kmtom)            
                        elif value_id > nSize-1:
                            resistivity.append(data)

                        value_id += 1

            if len(size_x) != nx:
                raise ValueError("invalid number of size x")
            if len(size_y) != ny:
                raise ValueError("invalid number of size y")
            if len(size_z) != nz:
                raise ValueError("invalid number of size z")
            if len(resistivity) != nx*ny*nz:
                raise ValueError("invalid number of resistivity data")

            result["n"] = { "sn": nx, "ew": ny, "z": nz }
            result["size"] = { "sn": size_x, "we": size_y, "z": size_z }
            result["resistivity"] = resistivity
            return result
    
    def __sumBlock(self, size):
        n_size = len(size)
        result_sum = np.zeros(n_size + 1)
        last_size = 0
        for i in range(n_size):
            last_size += size[i]
            result_sum[i+1] = last_size
        return result_sum

    def __mirrorSumBlock(self, size):
        size = np.array(size)
        n_size = len(size)
        negative_side = size[:n_size//2][::-1]*-1
        positive_side = size[(n_size//2):]

        negative_sum = self.__sumBlock(negative_side)[1:][::-1]
        positive_sum = self.__sumBlock(positive_side)

        result_mirror = np.append(negative_sum, positive_sum)
        return result_mirror

    def __searchRange(self, val, arr):

        for i in range(len(arr)):
            if int(arr[i])==0:
                center_id = i

        if arr[center_id+1]<0:
            mode = 'descending'
        elif arr[center_id+1]>0:
            mode = 'ascending'

        if mode=='descending':
            if val>0:
                for i in range(center_id, 0, -1):
                    if val>arr[i] and val<=arr[i-1]:
                        result_id = i-1
            elif val<0:
                for i in range(center_id, len(arr)-1, 1):
                    if val<arr[i] and val>=arr[i+1]:
                        result_id = i
            elif val==0:
                result_id = center_id-1

        elif mode=='ascending':
            if val<0:
                for i in range(center_id, 0, -1):
                    if val<arr[i] and val>=arr[i-1]:
                        result_id = i-1
            elif val>0:
                for i in range(center_id, len(arr)-1, 1):
                    if val>arr[i] and val<=arr[i+1]:
                        result_id = i
            elif val==0:
                result_id = center_id

        return result_id
    
    def __sliceResistivity(self, axis, value, sum_block, resistivity):        
        val_id = self.__searchRange(value, sum_block)
        if axis=="sn":
            return resistivity[:, val_id, :]
        elif axis=="we":
            return resistivity[:, :, val_id]
        elif axis=="z":
            return resistivity[val_id, :, :]

    def __reverseSlicedWE(self, arr):
        nrow_arr = len(arr)
        ncol_arr = len(arr[0])
        result_arr = np.empty_like(arr)
        for i in range(nrow_arr):
            for j in range(ncol_arr):
                result_arr[i][j] = arr[i][ncol_arr-1-j]
        return result_arr

    def __createMesh(self, axis):
        if axis=="z":
            X = self.sum_we
            Y = self.sum_sn
        elif axis=="sn":
            X = self.sum_we
            Y = self.sum_z
        elif axis=="we":
            X = self.sum_sn
            Y = self.sum_z
        
        xx, yy = np.meshgrid(X, Y, sparse=True)
        return xx, yy

    def setCbarTicks(self, tick_values):
        self.cbar_ticks = tick_values
        
    def plotZLine(self, first_slice, save_output):
        figsize = (7, 7)
        
        xx, yy = self.__createMesh('z')
        sliced_r = self.__sliceResistivity('z', first_slice, self.sum_z, self.resistivity)[::-1]
                
        fig, ax = plt.subplots(figsize=figsize, facecolor='white')        
        slice_plot = ax.pcolormesh(xx, yy, sliced_r, cmap=self.cmap, vmin=self.pcm_color_min, vmax=self.r_max)
        
        if self.sta_file:
            ax.plot(self.sta_coord['x'], self.sta_coord['y'], 'vk')
        if self.eq_file:
            sliced_eq = self.__sliceEQ('z', first_slice, self.eq_data, self.eq_radius)
            ax.scatter(sliced_eq['we0'], sliced_eq['sn0'], s=self.eq_marker_size, facecolors='none', edgecolors='k')

        # add x and y cross-section
        ax.yaxis.tick_right()
        
        if self.cross_we is not None:
            v_coords = self.cross_we
            trans_x = transforms.blended_transform_factory(ax.transData, ax.get_xticklabels()[0].get_transform())
            for i in range(len(v_coords)):
                ax.axvline(x=v_coords[i], color='black')
            if self.we_names is not None:
                for i in range(len(v_coords)):
                    ax.text(v_coords[i],0, "({})".format(self.we_names[i]), transform=trans_x, ha="center", va="top", fontsize=self.fsize_label)

        if self.cross_sn is not None:
            h_coords = self.cross_sn
            trans_y = transforms.blended_transform_factory(ax.get_yticklabels()[0].get_transform(), ax.transData)
            for i in range(len(h_coords)):
                ax.axhline(y=h_coords[i], color='black')
            if self.sn_names is not None:
                for i in range(len(h_coords)):
                    ax.text(1, h_coords[i], "({})".format(self.sn_names[i]), transform=trans_y, ha="left", va="center", fontsize=self.fsize_label)
        
        ax.yaxis.tick_left()
        plt.setp(ax.get_xticklabels(), alpha=0)
        ax.set_xlabel("Y(km)", fontsize=self.fsize_label, alpha=0)
        ax.set_ylabel("X(km)", fontsize=self.fsize_label)
        ax.tick_params(right=True, top=True, labelright=False, labeltop=False)
        ax.tick_params(axis='both', which='major', labelsize=self.fsize_axis)       
        ax.set_title("Depth={}km".format(first_slice), fontsize=self.fsize_title)
            
        ax.set_xlim(self.we_lim[0], self.we_lim[1])
        ax.set_ylim(self.sn_lim[0], self.sn_lim[1])
            
        ax.set_aspect("equal")
        plt.tight_layout()
        
        if save_output:
            filename = "Z_{}_AND_LINE.{}".format(str(first_slice).replace('.','_'), self.output_format)
            plt.savefig(os.path.join(self.output_folder, filename), format=self.output_format, transparent=True)
            
        cbar = plt.colorbar(slice_plot, ax=ax, orientation='horizontal', label='Resistivity (Ohm-meter)')
        if self.cbar_ticks is not None:
            cbar.set_ticks(self.cbar_ticks)
        ax.remove()
        if save_output:
            filename = "Colorbar.{}".format(self.output_format)
            plt.savefig(os.path.join(self.output_folder, filename), dpi=self.output_dpi, bbox_inches='tight', format=self.output_format, transparent=True)
        plt.close('all')

    def plotZCross(self, save_output):
        n_slice = len(self.cross_z)
        figsize = (7,7)

        xx, yy = self.__createMesh('z')
        
        for i in tqdm(range(n_slice)):
            sliced_r = self.__sliceResistivity('z', self.cross_z[i], self.sum_z, self.resistivity)
            sliced_r = sliced_r[::-1]
            
            fig, ax = plt.subplots(figsize=figsize, facecolor='white')
            
            ax.pcolormesh(xx, yy, sliced_r, cmap=self.cmap, vmin=self.pcm_color_min, vmax=self.r_max)
            ax.set_xlabel('Y(km)', fontsize=self.fsize_label)
            ax.set_ylabel('X(km)', fontsize=self.fsize_label)
            ax.tick_params(axis='both', which='major', labelsize=self.fsize_axis)
            ax.set_title("Depth={}km".format(self.cross_z[i]), fontsize=self.fsize_title)

            if self.sta_file:
                ax.plot(self.sta_coord['x'], self.sta_coord['y'], 'vk')
            if self.eq_file:
                sliced_eq = self.__sliceEQ('z', self.cross_z[i], self.eq_data, self.eq_radius)
                ax.scatter(sliced_eq['we0'], sliced_eq['sn0'], s=self.eq_marker_size, facecolors='none', edgecolors='k')
            
            # add x and y cross-section (hidden, to make same plot size)
            
            ax.yaxis.tick_right()
            
            if self.cross_we is not None:
                v_coords = self.cross_we
                trans_x = transforms.blended_transform_factory(ax.transData, ax.get_xticklabels()[0].get_transform())
                if self.we_names is not None:
                    for i_line in range(len(v_coords)):
                        ax.text(v_coords[i_line],0, "({})".format(self.we_names[i_line]), transform=trans_x, ha="center", va="top", fontsize=self.fsize_label, alpha=0)
                    
            if self.cross_sn is not None:            
                h_coords = self.cross_sn
                trans_y = transforms.blended_transform_factory(ax.get_yticklabels()[0].get_transform(), ax.transData)
                if self.sn_names is not None:
                    for i_line in range(len(h_coords)):
                        ax.text(1, h_coords[i_line], "({})".format(self.sn_names[i_line]), transform=trans_y, ha="left", va="center", fontsize=self.fsize_label, alpha=0)

            ax.yaxis.tick_left()
            ax.tick_params(right=True, top=True, labelright=False, labeltop=False)
            ax.set_xlim(self.we_lim[0], self.we_lim[1])
            ax.set_ylim(self.sn_lim[0], self.sn_lim[1])
            ax.set_aspect('equal')
            fig.tight_layout()
            
            if save_output:
                filename = "Z_{}.{}".format(str(self.cross_z[i]).replace('.','_'), self.output_format)
                plt.savefig(os.path.join(self.output_folder, filename), dpi=self.output_dpi, transparent=True, format=self.output_format)
        plt.close('all')
                
    def plotSNCross(self, save_output):
        n_slice = len(self.cross_sn)
        figsize = (7,7)

        title_pos = {"x": -0.1, "y": 1.1}
        xx, yy = self.__createMesh('sn')
        
        for i in tqdm(range(n_slice)):
            sliced_r = self.__sliceResistivity('sn', self.cross_sn[i], self.sum_sn[::-1], self.resistivity)
        
            fig, ax = plt.subplots(figsize=figsize, facecolor='white')            
            ax.pcolormesh(xx, yy, sliced_r, cmap=self.cmap, vmin=self.pcm_color_min, vmax=self.r_max)
            
            if self.eq_file:
                sliced_eq = self.__sliceEQ('sn', self.cross_sn[i], self.eq_data, self.eq_radius)
                ax.scatter(sliced_eq['we0'], sliced_eq['depth'], s=self.eq_marker_size, facecolors='none', edgecolors='k')
            
            ax.set_xlim(self.we_lim[0], self.we_lim[1])
            ax.set_ylim(self.z_lim[0], self.z_lim[1])
            ax.set_ylim(ax.get_ylim()[::-1])
            
            ax.set_xlabel('Y(km)', fontsize=self.fsize_label)
            ax.set_ylabel('Depth(km)', fontsize=self.fsize_label)
            ax.tick_params(right=True, top=True, labelright=False, labeltop=False)
            ax.tick_params(axis='both', which='major', labelsize=self.fsize_axis)
            if self.sn_names is None:
                ax.set_title('X={}km'.format(self.cross_sn[i]), fontsize=self.fsize_title)
            else:
                ax.set_title('({}) X={}km'.format(self.sn_names[i], self.cross_sn[i]), fontsize=self.fsize_title, loc='left', x=title_pos["x"], y=title_pos["y"])

            ax.set_aspect('equal')
            plt.tight_layout()
            
            if save_output:
                if self.sn_names is None:
                    filename = 'SN_{}.{}'.format(str(self.cross_sn[i]).replace('.', '_'), self.output_format)
                else:
                    filename = '{}_SN_{}.{}'.format(self.sn_names[i], str(self.cross_sn[i]).replace('.', '_'), self.output_format)
                plt.savefig(os.path.join(self.output_folder, filename), dpi=self.output_dpi, transparent=True, format=self.output_format)
        plt.close('all')
        
    def plotWECross(self, save_output):
        n_slice = len(self.cross_we)
        figsize = (7,7)
        title_pos = {"x": -0.1, "y": 1.1}
        xx, yy = self.__createMesh('we')
        
        for i in tqdm(range(n_slice)):
            sliced_r = self.__sliceResistivity('we', self.cross_we[i], self.sum_we, self.resistivity)
            sliced_r = self.__reverseSlicedWE(sliced_r)
            
            fig, ax = plt.subplots(figsize=figsize, facecolor='white')            
            ax.pcolormesh(xx, yy, sliced_r, cmap=self.cmap, vmin=self.pcm_color_min, vmax=self.r_max)
            
            if self.eq_file:
                sliced_eq = self.__sliceEQ('we', self.cross_we[i], self.eq_data, self.eq_radius)
                ax.scatter(sliced_eq['sn0'], sliced_eq['depth'], s=self.eq_marker_size, facecolors='none', edgecolors='k')
            ax.set_xlim(self.sn_lim[0], self.sn_lim[1])
            ax.set_ylim(self.z_lim[0], self.z_lim[1])                
            ax.set_ylim(ax.get_ylim()[::-1])            
            
            ax.set_xlabel('X(km)', fontsize=self.fsize_label)
            ax.set_ylabel('Depth(km)', fontsize=self.fsize_label)
            ax.tick_params(right=True, top=True, labelright=False, labeltop=False)
            ax.tick_params(axis='both', which='major', labelsize=self.fsize_axis)
            if self.we_names is None:
                ax.set_title("Y={}km".format(self.cross_we[i]), fontsize=self.fsize_title)
            else:
                ax.set_title("({}) Y={}km".format(self.we_names[i], self.cross_we[i]), fontsize=self.fsize_title, loc='left', x=title_pos["x"], y=title_pos["y"])

            ax.set_aspect('equal')
            plt.tight_layout()
            
            if save_output:
                if self.we_names is None:
                    filename = 'WE_{}.{}'.format(str(self.cross_we[i]).replace('.', '_'), self.output_format)
                else:
                    filename = '{}_WE_{}.{}'.format(self.we_names[i], str(self.cross_we[i]).replace('.', '_'), self.output_format)
                plt.savefig(os.path.join(self.output_folder, filename), dpi=self.output_dpi, transparent=True, format=self.output_format)            
        plt.close('all')
        
    def process(self):
        if self.input_file:
            self.__setOutputFolder()
            model_data = self.__readModel(os.path.join(self.base_path, self.input_file))
            self.r_min = np.min(model_data["resistivity"])
            self.r_max = np.max(model_data["resistivity"])
            self.resistivity = np.array(model_data["resistivity"]).reshape(model_data["n"]["z"], \
                                                                           model_data["n"]["sn"], model_data["n"]["ew"])
            self.sum_sn = self.__mirrorSumBlock(model_data["size"]["sn"])
            self.sum_we = self.__mirrorSumBlock(model_data["size"]["we"])
            self.sum_z = self.__sumBlock(model_data["size"]["z"])

            self.sn_lim = (np.min(self.sum_sn), np.max(self.sum_sn))
            self.we_lim = (np.min(self.sum_we), np.max(self.sum_we))
            self.z_lim = (np.min(self.sum_z), np.max(self.sum_z))

        if self.eq_file is not None:
            self.eq_data = self.__readEQ(self.eq_file, recenter=True)
        
        if self.sta_file is not None:
            self.sta_data = self.__readSta(self.sta_file, recenter=True)
            n_sta = len(self.sta_data)
            sta_x = np.zeros(n_sta, dtype=float)
            sta_y = np.zeros(n_sta, dtype=float)
            
            for i, sta_name in enumerate(self.sta_data):
                sta_x[i] = self.sta_data[sta_name]['we0']
                sta_y[i] = self.sta_data[sta_name]['sn0']
            self.__setStaCoord(sta_x, sta_y)
