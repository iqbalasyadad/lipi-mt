from sys import platform
import os
import ntpath
import numpy as np
import math
from tabulate import tabulate
import readline

class GDParameter:
    
    def __init__(self):
        pass
    
    def read(self, file):
        
        hmode = ''
        data = []
        dataDic = {
            'FILE_PT1': [],
            'FILE_DATA': '',
            'FILE_ERROR': '',
            'OUTPUT_FOLDER': '',
            'OUTPUT_NAME': [],
            'LOG_OUTPUT': []
        }
        
        with open(file) as f:
            for line in f:
                line = line.replace('\n', '')
                splitd_line = line.split()
                
                if len(splitd_line) == 0:
                    continue
                
                if splitd_line[0] == '#':
                    hmode = splitd_line[1]
                    data.append([])
                else:
                    if hmode=='FILE_PT1': 
                        line = line.split('.pt1')
                        for cpath in line:
                            if len(cpath.split())==0:
                                continue
                            else:
                                dataDic[hmode].append(cpath.strip()+'.pt1')
                    
                    elif hmode=='FILE_DATA':
                        dataDic[hmode] = line.strip()
                    
                    elif hmode=='FILE_ERROR':
                        dataDic[hmode] = line.strip()
                    
                    elif hmode=='OUTPUT_FOLDER':
                        dataDic[hmode] = line.strip()
                    
                    elif hmode=='OUTPUT_NAME':
                        if line.strip().upper() == 'DEFAULT':
                            dataDic[hmode].append('DEFAULT')
                        else:
                            for name in splitd_line:
                                dataDic[hmode].append(ntpath.basename(name))
                                
                    elif hmode=='LOG10_OUTPUT':
                        logmode = line.strip().upper()
                        if logmode=='TRUE':
                            logmode = True
                        else:
                            logmode = False
                        dataDic[hmode] = logmode
        
        if dataDic['OUTPUT_NAME'][0] == 'DEFAULT':
            dataDic['OUTPUT_NAME'] = 'DEFAULT'
            
        return(dataDic)
    
class CreateGD:
    
    def __init__(self):
        self.basepath = os.getcwd()
        self.outputFolder = 'output'
        self.outputPath = os.path.join(self.basepath, self.outputFolder)
        self.NoneSym = 'NaN '
        self.outNames = None
    
    def __vartoerr(self, data):
        return data ** 0.5
    
    def setpt1Files(self, pt1files):
        self.pt1_files = pt1files
    
    def readpt1(self, file):
        headers=[]
        data=[]
        header_num = 0
        with open(file) as f:
            for line in f:
                first_str = line.split()[0]
                try:
                    float (first_str)
                    for val in line.split():
                        data[header_num-1].append(float(val))
                except:
                    if first_str == "PARAMETER#":
                        headers.append(' '.join(line.split()[3:]))
                    else:
                        headers.append(line.split()[0].replace(':',''))
                    header_num +=1
                    data.append([])
                
        usedHeader = {
            'freqs': 'FREQS',
            'rhoxy': 'Rhoxy ohm-m.', 
            'rhoyx': 'Rhoyx ohm-m.',
            'phasexy': 'PHASExy Deg.',
            'phaseyx': 'PHASEyx Deg.',
            'vrhoxy' :'Var Log Rhoxy',
            'vrhoyx' : 'Var Log Rhoyx',
            'vphasexy': 'Var PHASExy', 
            'vphaseyx': 'Var PHASEyx'
        }
        
        pt1_dic = {}
        for ih, hname in enumerate(headers):
            for key in usedHeader:
                if hname == usedHeader[key]:
                    pt1_dic[key] = np.array(data[ih])
        
        pt1_dic['erhoxy'] = self.__vartoerr(pt1_dic['vrhoxy'])
        pt1_dic['erhoyx'] = self.__vartoerr(pt1_dic['vrhoyx'])
        pt1_dic['ephasexy'] = self.__vartoerr(pt1_dic['vphasexy'])
        pt1_dic['ephaseyx'] = self.__vartoerr(pt1_dic['vphaseyx'])
        
        var_key = ['vrhoxy', 'vrhoyx', 'vphasexy', 'vphaseyx']
        for key in var_key:
            del pt1_dic[key]
        
        return pt1_dic
    
    def readpt1s(self, files):
        self.pt1sfname = []
        self.pt1s_dic = {}
        for file in files:
            fname = ntpath.basename(file)
            self.pt1s_dic[fname] = self.readpt1(os.path.join(self.basepath, file))
            self.pt1sfname.append(fname)
        
    def readOutput(self, file, fmode):
        
        '''
            read output file
            arg:
                - file: output filename
                - fmode: file mode ('data', 'resp', 'err')
            return (dict):
                - number of station, period, response
                - station location (ns and ew)
                - periods selected
                - impedance/error impedance
                - additional parameter in resp file (iter_no, rms, lm)
        '''
        
        with open(file) as f:
            lines = f.readlines()
            
        n_sta, n_period, n_resp = list(map(int, lines[0].split()))
        del lines[0]
    
        sta_ns = []
        sta_ew = []        
        periods = []
        impds = []
        err_impds = []
        resp_add = {}
        
        for line in lines:
            if len(line.split())==0:
                continue
            if 'Station_Location: N-S' in line:
                h_mode = 'sta_ns'
                
            elif 'Station_Location: E-W' in line:
                h_mode = 'sta_ew'
            
            elif 'DATA_Period:' in line:
                h_mode = 'data_period'
                impds.append([])
                splitted_line = line.split()
                try:
                    period = float(splitted_line[1])
                except:
                    raise TypeError('Period can\'t be converted to float32')
                else:
                    periods.append(period)
            
            elif 'ERROR_Period' in line:
                h_mode = 'err_period'
                err_impds.append([])
                splitted_line = line.split()
                try:
                    period = float(splitted_line[1])
                except:
                    raise TypeError('Period can\'t be converted to float32')
                else:
                    periods.append(period)
            
            elif '#Iteration No.' in line:
                h_mode = 'resp_add'
                line = line.replace('#Iteration No.', '#Iteration_No.')

                if 'RMS =' in line:
                    line = line.replace('RMS =', 'RMS=')
                if 'LM =' in line:
                    line = line.replace('LM =', 'LM=')
                
                splitted_line = line.split()
                for i, word in enumerate(splitted_line):
                    if word == '#Iteration_No.':
                        resp_add['iter_no'] = int(splitted_line[i+1])
                    elif word == 'RMS=':
                        resp_add['rms'] = float(splitted_line[i+1])
                    elif word == 'LM=':
                        resp_add['lm'] = float(splitted_line[i+1])
            else:
                splitted_line = line.split()
            
                for word in splitted_line:
                    try:
                        word = float(word)
                    except:
                        raise TypeError('Invalid data type')
                    else:
                        if h_mode == 'sta_ns':
                            sta_ns.append(word)
                        elif h_mode == 'sta_ew':
                            sta_ew.append(word)
                        elif h_mode == 'data_period':
                            impds[-1].append(word)
                        elif h_mode == 'err_period':
                            err_impds[-1].append(word)
        dictfile = {
            'n_sta': n_sta,
            'n_period': n_period,
            'n_resp': n_resp,
            'sta_ns': np.array(sta_ns),
            'sta_ew': np.array(sta_ew),
            'periods': np.array(periods),
        }
        
        if fmode == 'resp':
            dictfile.update(resp_add)
            self.respfdict = dictfile
        elif fmode == 'data':
            impds = np.array(impds).reshape(n_period, n_sta, n_resp)
            dictfile['impds'] = {}
            for ifname, fname in enumerate(self.pt1sfname):
                dictfile['impds'][fname] = impds[:,ifname]
            self.datafdict = dictfile
        elif fmode == 'err':
            eimpds = np.array(err_impds).reshape(n_period, n_sta, n_resp)
            dictfile['eimpds']  = {}
            for ifname, fname in enumerate(self.pt1sfname):
                dictfile['eimpds'][fname] = eimpds[:,ifname]
            self.errfdict = dictfile
            self.confOutPeriod()
            
    def confOutPeriod(self):
        dPeriods = self.datafdict['periods']
        ePeriods = self.errfdict['periods']
        self.periods = []
        comparison = dPeriods == ePeriods
        if comparison.all():
            self.periods = dPeriods
        else:
            raise ValueError('period doesn\'t match')
                
    def getApResPhs(self, periodId, fname):
        period = self.periods[periodId]
        impd = self.datafdict['impds'][fname][periodId]
        erimpd = self.errfdict['eimpds'][fname][periodId]

        factor=10**4/(4*np.pi)

        zxyr=factor*impd[2]
        zxyi=factor*impd[3]*(-1)
        zyxr=factor*impd[4]
        zyxi=factor*impd[5]*(-1)

        zxy=np.sqrt(zxyr**2+zxyi**2)
        zyx=np.sqrt(zyxr**2+zyxi**2)

        ezxyr=factor*erimpd[2]
        ezxyi=factor*erimpd[3]
        ezyxr=factor*erimpd[4]
        ezyxi=factor*erimpd[5]

        ezxy=np.sqrt(ezxyr**2+ezxyi**2)
        ezyx=np.sqrt(ezyxr**2+ezyxi**2)

        rhoxy=period/5.*(zxyr**2 + zxyi**2)
        rhoyx=period/5.*(zyxr**2 + zyxi**2)

        phsxy=math.atan2(zxyi,zxyr)*180./np.pi
        phsyx=math.atan2(zyxi,zyxr)*180./np.pi

        erhoxy=period/5.*2*zxy*ezxy
        erhoyx=period/5.*2*zyx*ezyx
        ephsxy=abs(math.atan2(ezxy,np.sqrt(zxy**2-ezxy**2)))*180./np.pi
        ephsyx=abs(math.atan2(ezyx,np.sqrt(zyx**2-ezyx**2)))*180./np.pi
        
        result = {
            'rhoxy': rhoxy,
            'rhoyx': rhoyx,
            'phasexy': phsxy,
            'phaseyx': phsyx,
            'erhoxy': erhoxy,
            'erhoyx': erhoyx,
            'ephasexy': ephsxy,
            'ephaseyx': ephsyx
        }
        
        return result

    def getMatchPeriods(self, fname):
        freqs = self.pt1s_dic[fname]['freqs']
        pt1Periods = np.empty_like(freqs)
        
        for ifreq, freq in enumerate(freqs):
            if freq!=float(0):
                pt1Periods[ifreq] = 1/freq
            else:
                pt1Periods[ifreq] = np.inf
        
        pt1Periods_str = []
        for period in pt1Periods:
            if np.isfinite(period):
                pt1Periods_str.append('{}'.format(round(period, 5)))
            else:
                pt1Periods_str.append('inf')
                
        outputPeriods = self.datafdict['periods']
        outputPeriods_str = ['{}'.format(round(period, 5)) for period in outputPeriods]
        
        pt1PeriodId = []
        outPeriodId = []
        for ipt1, pt1period in enumerate(pt1Periods_str):
            for iout, outPeriod in enumerate(outputPeriods_str):
                if outPeriod == pt1period:
                    pt1PeriodId.append(ipt1)
                    outPeriodId.append(iout)
        return {'pt1': pt1PeriodId, 'out': outPeriodId}

    def createStrOutput(self, fname):    
        self.output = ''
        nfreq = len(self.pt1s_dic[fname]['freqs'])
        ncol = 17
        out_vals = [[0 for lcol in range(ncol)] for lrow in range(nfreq)]
        matchPeriodId = self.getMatchPeriods(fname)
                
        for ifreq, freq in enumerate(self.pt1s_dic[fname]['freqs']):
            out_vals[ifreq][0] = freq
            out_vals[ifreq][1] = self.pt1s_dic[fname]['rhoxy'][ifreq]
            out_vals[ifreq][2] = self.pt1s_dic[fname]['rhoyx'][ifreq]
            out_vals[ifreq][3] = self.pt1s_dic[fname]['phasexy'][ifreq]
            out_vals[ifreq][4] = self.pt1s_dic[fname]['phaseyx'][ifreq]
            out_vals[ifreq][5] = self.pt1s_dic[fname]['erhoxy'][ifreq]
            out_vals[ifreq][6] = self.pt1s_dic[fname]['erhoyx'][ifreq]
            out_vals[ifreq][7] = self.pt1s_dic[fname]['ephasexy'][ifreq]
            out_vals[ifreq][8] = self.pt1s_dic[fname]['ephaseyx'][ifreq]
            
            if ifreq in matchPeriodId['pt1']:
                for ipout in range(len(matchPeriodId['pt1'])):
                    if ifreq == matchPeriodId['pt1'][ipout]:
                        outPId = matchPeriodId['out'][ipout]
                
                calcVal = self.getApResPhs(outPId, fname)
                
                out_vals[ifreq][9] = calcVal['rhoxy']
                out_vals[ifreq][10] = calcVal['rhoyx']
                out_vals[ifreq][11] = calcVal['phasexy']
                out_vals[ifreq][12] = calcVal['phaseyx']
                out_vals[ifreq][13] = calcVal['erhoxy']
                out_vals[ifreq][14] = calcVal['erhoyx']
                out_vals[ifreq][15] = calcVal['ephasexy']
                out_vals[ifreq][16] = calcVal['ephaseyx']
                
            else:
                for icol in range(9, 17):
                    out_vals[ifreq][icol] = self.NoneSym
            
            # to log val
            logIds = [0,1,2,5,6,9,10,13,14]
            
            if self.logMode:
                for valId in logIds:
                    if type(out_vals[ifreq][valId]) == str:
                        continue
                    else:
                        try:
                            out_vals[ifreq][valId] = np.log10(out_vals[ifreq][valId])
                        except Exception as err:
                            print(err)
        stdoldheaders = ['freqs', 'obs_rhoxy', 'obs_rhoyx', 'obs_phasexy', 'obs_phaseyx', 
                       'obs_erhoxy', 'obs_erhoyx', 'obs_ephasexy', 'obs_ephaseyx',
                       'calc_rhoxy', 'calc_rhoyx', 'calc_phasexy', 'calc_phaseyx', 
                       'calc_erhoxy', 'calc_erhoyx', 'calc_ephasexy', 'calc_ephaseyx']
        
        stdHeaders = ['freqs_Hz', 'obs_rhoxy_ohm-m', 'obs_rhoyx_ohm-m', 
                       'obs_phasexy_deg', 'obs_phaseyx_deg', 
                       'obs_erhoxy', 'obs_erhoyx', 
                       'obs_ephasexy', 'obs_ephaseyx',
                       'calc_rhoxy_ohm-m', 'calc_rhoyx_ohm-m', 
                       'calc_phasexy', 'calc_phaseyx', 
                       'calc_erhoxy', 'calc_erhoyx', 
                       'calc_ephasexy', 'calc_ephaseyx']
        
        if self.logMode:
            headers = []
            for iheader, header in enumerate(stdHeaders):
                if iheader in logIds:
                    headers.append('log10({})'.format(header))
                else:
                    headers.append(header)
        else:
            headers = stdHeaders


        out_str = tabulate(out_vals, headers, numalign="right", tablefmt='plain')
        return out_str
    
    def setLogMode(self, mode):
        self.logMode = mode

    def setOutName(self, outNames):
        self.outNames = outNames
        
    def saveOutputs(self):
        outfexist = os.path.exists(self.outputPath)
        if not outfexist:
            os.makedirs(self.outputPath)
        
        if self.outNames == 'DEFAULT' or self.outNames is None:
            if self.logMode:
                self.outNames = [fname.replace('.pt1', '_log.out') for fname in self.pt1sfname]
            else:
                self.outNames = [fname.replace('pt1', 'out') for fname in self.pt1sfname]
        
        for i, fname in enumerate(self.pt1sfname):
            strOut = self.createStrOutput(fname)
            fOutPath = os.path.join(self.outputPath, self.outNames[i])
            try:
                with open(fOutPath, 'w') as f:
                    f.write(strOut)
            except Exception as err:
                print(err)
            else:
                print('Created {}'.format(os.path.join(self.outputFolder, self.outNames[i])))

class GDCLI:
    
    def __init__(self):
        self.base_path = os.getcwd()
        readline.parse_and_bind("tab:complete")
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")
    
    def showHeader(self):
        print("####################################################################")
        print("                  GENERATE FREQUENCY, RHO, AND PHASE                ")
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
    gdCLI = GDCLI()
    gdParam = GDParameter()

    gdCLI.showHeader()

    print('Parameter File:')
    while(True):
        param_file = gdCLI.getInput()
        try:
            param = gdParam.read(param_file)
        except Exception as err:
            print(err)
        else:
            break

    pt1files = param['FILE_PT1']
    data_file = param['FILE_DATA']
    error_file = param['FILE_ERROR']
    outnames = param['OUTPUT_NAME']
    logmode = param['LOG10_OUTPUT']

    myGData = CreateGD()
    myGData.readpt1s(pt1files)
    myGData.readOutput(data_file, 'data')
    myGData.readOutput(error_file, 'err')
    myGData.setLogMode(logmode)
    myGData.setOutName(outnames)
    myGData.saveOutputs()

if __name__=='__main__':
    main()
