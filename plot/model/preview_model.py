from sys import platform
import os
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import readline

class Model:
    
    def __init__(self, file_model):
        self.kmtom = 1000
        raw_data = self.__read(file_model)
        self.r_min = np.min(raw_data["resistivity"])
        self.r_max = np.max(raw_data["resistivity"])
        self.resistivity = np.array(raw_data["resistivity"]).reshape(raw_data["n"]["z"], raw_data["n"]["sn"], raw_data["n"]["ew"])
        self.sum_sn = self.__mirrorSumBlock(raw_data["size"]["sn"])/self.kmtom
        self.sum_we = self.__mirrorSumBlock(raw_data["size"]["we"])/self.kmtom
        self.sum_z = self.__sumBlock(raw_data["size"]["z"])/self.kmtom
        
    def __read(self, file):
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
                            size_x.append(data)
                        elif value_id > nx-1 and value_id <= (nx+ny-1):
                            size_y.append(data)
                        elif value_id > ny-1 and value_id <= (nx+ny+nz-1):
                            size_z.append(data)            
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

    def __sumBlock(self, size_list):
        n_size = len(size_list)
        result_sum = np.zeros(n_size + 1)
        last_size = 0
        for i in range(n_size):
            last_size += size_list[i]
            result_sum[i+1] = last_size
        return result_sum

    def __mirrorSumBlock(self, size_list):
        size_list = np.array(size_list)
        n_size = len(size_list)
        negative_side = size_list[:n_size//2][::-1]*-1
        positive_side = size_list[(n_size//2):]
        negative_sum = self.__sumBlock(negative_side)[1:][::-1]
        positive_sum = self.__sumBlock(positive_side)
        result_mirror = np.append(negative_sum, positive_sum)
        return result_mirror
    
    def createMesh(self, axis):
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
    
class IndexTracker:
    def __init__(self, ax, xx, yy, data, sum_z):
        n_color = 20
        self.cmap = plt.get_cmap('jet_r', n_color)
        self.ax = ax
        self.ax.set_xlabel('Y (km)')
        self.ax.set_ylabel('X (km)')
        self.ax.tick_params(right=True, top=True, labelright=False, labeltop=False)
        self.ax.set_aspect('equal')
        self.xx = xx
        self.yy = yy
        self.data = data
        self.data_min = np.min(self.data)
        self.data_max = np.max(self.data)
        self.sum_z = sum_z
        self.slices = len(data)
        self.ind = 0
        sliced_r = self.data[self.ind][::-1]
        self.pcm = ax.pcolormesh(self.xx, self.yy, sliced_r, cmap=self.cmap, vmin=0, vmax=self.data_max)
        plt.colorbar(self.pcm, ax=ax, orientation='horizontal', label='Resistivity (Ohm-meter)', fraction=0.04)
        self.update()

    def on_scroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        sliced_r = self.data[self.ind][::-1]
        self.pcm.set_array(sliced_r.ravel())
        self.ax.set_title('Depth {}-{} km'.format(self.sum_z[self.ind], self.sum_z[self.ind+1]))
        self.pcm.axes.figure.canvas.draw()

class PlotPreviewCLI:
    def __init__(self):
        self.base_path = os.getcwd()
        readline.parse_and_bind("tab:complete")
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")
        
    
    def showHeader(self):
        print("####################################################################")
        print("                           PREVIEW MODEL                            ")
        print("####################################################################")
        print("{0:17s}: {1}".format("CTRL+C or \'exit\'", "close the program"))
        print("{0:17s}: {1}".format("BASE PATH", self.base_path))
        print("####################################################################")
    
    def getInput(self):
        user_input = input(">> ")
        if user_input.lower() == "exit":
            print("Program closed")
            exit()
        else:
            return user_input
    
    def showTable(self, sum_sn, sum_we, sum_z, resistivity):
        print()
        table_data = [ 
            ['minimum', np.min(resistivity), np.min(sum_sn), np.min(sum_we), np.min(sum_z)],
            ['maximum', np.max(resistivity), np.max(sum_sn), np.max(sum_we), np.max(sum_z)]
        ]
        print(tabulate(table_data, headers=[' ', 'Resistivity\n(Ohm-meter)', 'South-North\n(km)', \
            'West-East\n(km)', 'Depth\n(km)'], tablefmt="pretty"))

def main():

    previewCLI = PlotPreviewCLI()
    previewCLI.showHeader()

    print("Model File:")
    while(True):
        inputFile = previewCLI.getInput()
        try:
            myModel = Model(inputFile)
        except Exception as err:
            print(err)
        else:
            break
    
    previewCLI.showTable(myModel.sum_sn, myModel.sum_we, myModel.sum_z, myModel.resistivity)

    
    fig, ax = plt.subplots(1, 1)
    xx, yy = myModel.createMesh('z')
    tracker = IndexTracker(ax, xx, yy, myModel.resistivity, myModel.sum_z)
    fig.canvas.mpl_connect('scroll_event', tracker.on_scroll)
    plt.show()

if __name__ == '__main__':
    main()
