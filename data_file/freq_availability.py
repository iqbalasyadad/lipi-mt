import os
from sys import platform
import readline
import glob
import numpy as np
from tabulate import tabulate

class FreqAvail:
    
    def __init__(self):
        self.basepath = os.getcwd()
    
    def setPt1Folder(self, folder):
        self.pt1_folder = folder
        
    def setPt1Files(self, files):
        if files == '.' or files == '*':
            self.pt1_files = np.sort([os.path.basename(x) for x in glob.glob(os.path.join(self.pt1_folder, '*.pt1'))])
        else:
            self.pt1_files = files
            
    def readPt1(self, file):
        ffile = os.path.join(self.pt1_folder, file)
        freqs = []
        freq_mode = False
        freq_done = False
        with open(ffile) as f:
            for line in f:
                splitted_line = line.split()
                
                if freq_done:
                    break
                
                if freq_mode:
                    for val in splitted_line:
                        try:
                            val = float(val)
                        except:
                            freq_done = True
                            freq_mode = False
                            break
                        else:
                            freqs.append(val)
                else:
                    if splitted_line[0] == 'FREQS:':
                        freq_mode = True
        return {file: np.array(freqs)}
        
    def multiReadPt1(self, files):
        result = {}
        for file in files:
            pt1_data = self.readPt1(file)
            result.update(pt1_data)
        return result
    
    def getFreqsIntersect(self):
        
        if len(self.pt1_files)==1:
            return self.pt1s_dict[self.pt1_files[0]]
        
        same_freqs = self.pt1s_dict[self.pt1_files[0]]
        for fname in self.pt1_files[1:]:
            same_freqs = np.intersect1d(same_freqs, self.pt1s_dict[fname])
        same_freqs = same_freqs[::-1]
        if 0 in same_freqs :
            id_0 = np.where(same_freqs==0)
            same_freqs = np.delete(same_freqs, id_0)
        return same_freqs
    
    def getFreqsAvailability(self):
        
        if len(self.pt1_files)==1:
            all_freqs = self.pt1s_dict[self.pt1_files[0]]
        else:
            all_freqs = []
            for fname in self.pt1_files:
                for val in self.pt1s_dict[fname]:
                    all_freqs.append(val)
            all_freqs = np.array(list(set(all_freqs)))
            
        if 0 in all_freqs :
            id_0 = np.where(all_freqs==0)
            all_freqs = np.delete(all_freqs, id_0)
        all_freqs = np.sort(all_freqs)[::-1]
        
        pt1_f_av = { 'all_freqs': all_freqs }
        nfreqs = len(all_freqs)
        for fname in self.pt1_files:
            f_av_temp = np.zeros(nfreqs, dtype=int)
            for ifreq, freq in enumerate(all_freqs):    
                if freq in self.pt1s_dict[fname]:
                    f_av_temp[ifreq] = 1
                else:
                    pass
            pt1_f_av[fname] = f_av_temp
        return pt1_f_av
    
    def createStrSameFreqs(self):
        table_data = [self.same_freqs.tolist()] 
        str_out = ''
        str_out += 'Available frequencies in all files\n'
        str_out += tabulate(table_data, tablefmt="plain")
        str_out += '\n\n\n'
        return str_out
    
    def createStrAvFreqs(self):
        table_data = []
        for fname in self.pt1_files:
            data_temp = [fname]
            for val in self.av_freqs[fname]:
                if val==1:
                    val_sign = 'v'
                else:
                    val_sign = ' '
                data_temp.append(val_sign)
            table_data.append(data_temp)
        str_out = ''
        str_out += 'Details:\n'
        str_out += tabulate(table_data, headers=self.av_freqs['all_freqs'], tablefmt="pretty")
        return str_out
                        
        
    def process(self):
        self.pt1s_dict = self.multiReadPt1(self.pt1_files)
        self.same_freqs = self.getFreqsIntersect()
        self.av_freqs = self.getFreqsAvailability()
        
        self.str_result = ''
        self.str_result += self.createStrSameFreqs()
        self.str_result += self.createStrAvFreqs()
    
    def saveOutput(self, save_name):
        with open (save_name, 'w') as f:
            f.write(self.str_result)
            
class FreqAvailCLI:
    
    def __init__(self):
        self.base_path = os.getcwd()
        readline.parse_and_bind("tab:complete")
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")
    
    def showHeader(self):
        print("####################################################################")
        print("                        GET PT1 FREQUENCIES                         ")
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
    
    def getPt1Folder(self):
        print()
        print("Input pt1 folder:")
        while(True):
            pt1_folder = self.getInput()
            if os.path.isdir(pt1_folder):
                self.pt1_folder = pt1_folder
                break
            else:
                print("Error: folder doesn't exist")
                continue
    
    def getPt1File(self):
        print()
        print("Input pt1 files:")
        fname_temp = []
        while(True):
            user_input = self.getInput()
            if user_input == '.':
                self.pt1_files = user_input
                break
            else:
                user_input = user_input.split(' ')
                if user_input == '':
                    pass
                else:
                    for word in user_input:
                        if word == 'end':
                            self.pt1_files = fname_temp
                            return
                        else:
                            fname_temp.append(word)

    def getOutName(self):
        print()
        print("Output name:")
        while(True):
            save_name = self.getInput()
            if save_name.replace(' ', '') == '':
                continue
            else:
                self.save_name = save_name
                return
                
def main():
    facli = FreqAvailCLI()
    facli.showHeader()
    
    facli.getPt1Folder()
    facli.getPt1File()
    facli.getOutName()
    
    myAF = FreqAvail()
    myAF.setPt1Folder(facli.pt1_folder)
    myAF.setPt1Files(facli.pt1_files)
    myAF.process()
    
    try:
        myAF.saveOutput(facli.save_name)
    except Exception as err:
        print(err)
    else:
        print()
        print("Success...")
    

if __name__ == "__main__":
    main()
