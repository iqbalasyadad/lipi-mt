from sys import platform
import os
import ntpath
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import readline

class ModelValPos:
    
    def __init__(self):
        self.kmtom = 1000
        self.basepath = os.getcwd()
        self.output_folder = 'output'
        self.output_path = os.path.join(self.basepath, self.output_folder)
        self.outName = None
    
    def __readModel(self, file):
        row_title = 0
        row_number = 1
        row_data = 2
        rmodel = {}

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
                        rmodel["iter_no"] = int(line_0[i+1])
                    except:
                        raise TypeError("Iteration is not integer")
                elif line_0[i]=="rms":
                    try:
                        rmodel["rms"] = float(line_0[i+1])
                    except:
                        raise TypeError("rms is not a number")
                elif line_0[i]=="lm":
                    try:
                        rmodel["lm"] = float(line_0[i+1])
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

            rmodel["n"] = { "sn": nx, "ew": ny, "z": nz }
            rmodel["size"] = { "sn": size_x, "we": size_y, "z": size_z }
            rmodel["resistivity"] = resistivity
            

            self.sumB = {
                'sn': self.__mirrorSumBlock(rmodel["size"]["sn"]),
                'rvdsn': self.__mirrorSumBlock(rmodel["size"]["sn"])[::-1],
                'we': self.__mirrorSumBlock(rmodel["size"]["we"]),
                'z': self.__sumBlock(rmodel["size"]["z"])
            }
            self.resistivity = np.array(rmodel["resistivity"]).reshape(rmodel['n']['z'], \
                                                                       rmodel['n']['sn'],
                                                                       rmodel['n']['ew'])
            
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

    def setOutName(self, fname):
        self.outName = fname
    
    def createPos(self, file):
        self.__readModel(file)
        out_vals = np.zeros([len(self.resistivity.flatten()), 7])
        ir=0
        for irz, rz in enumerate(self.resistivity):
            for irsn, rsn in enumerate(rz):
                for irwe, rwe in enumerate(rsn):
                    out_vals[ir][0] = rwe
                    out_vals[ir][1] = self.sumB['we'][irwe]
                    out_vals[ir][2] = self.sumB['we'][irwe+1]
                    out_vals[ir][3] = self.sumB['rvdsn'][irsn]
                    out_vals[ir][4] = self.sumB['rvdsn'][irsn+1]
                    out_vals[ir][5] = self.sumB['z'][irz]
                    out_vals[ir][6] = self.sumB['z'][irz+1]
                    ir+=1
        rpos_h = ['resistivity', 'we_start', 'we_end', 'sn_start', 'sn_end','depth_start', 'depth_end']
        rpos_str = tabulate(out_vals, rpos_h, numalign="right", tablefmt='plain')
         
        # save section
        inputFname = ntpath.basename(file)        
        if self.outName is None:
            self.outName = inputFname.replace('.','_') + '.rpos'
        outfexist = os.path.exists(self.output_path)
        if not outfexist:
            os.makedirs(self.output_path)
        fOutPath = os.path.join(self.output_path, self.outName)
        with open(fOutPath, 'w') as f:
            f.write(rpos_str)
        print('Created {}'.format(os.path.join(self.output_folder, self.outName)))


class RPosCLI:
    
    def __init__(self):
        self.base_path = os.getcwd()
        readline.parse_and_bind("tab:complete")
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")
    
    def showHeader(self):
        print("####################################################################")
        print("                     CREATE RESISTIVITY POSITION                    ")
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
            return user_input.strip()

def main():
    rPosCLI = RPosCLI()
    rPosCLI.showHeader()
    myMpos = ModelValPos()

    print('Model File:')
    while(True):
        model_file = rPosCLI.getInput()
        try:
            myMpos.createPos(model_file)
        except Exception as err:
            print(err)
        else:
            break

if __name__=='__main__':
    main()
