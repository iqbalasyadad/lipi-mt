class PlotParameter:
    
    def __init__(self):
        self.header = {
            'file_model': 'FILE_MODEL',
            'file_sta': 'FILE_STATION',
            'file_eq': 'FILE_EARTHQUAKE',
            'eq_rad': 'EARTHQUAKE_RADIUS_(KM)',
            'model_center': 'MODEL_CENTER_(LAT_LNG)',
            'slice_we': 'SLICE_WEST_EAST_(KM)',
            'slice_sn': 'SLICE_SOUTH_NORTH_(KM)',
            'slice_depth': 'SLICE_DEPTH_(KM)',
            'name_we': 'SLICE_WEST_EAST_LABEL',
            'name_sn': 'SLICE_SOUTH_NORTH_LABEL',
            'limit_we': 'LIMIT_WEST_EAST_(KM)',
            'limit_sn': 'LIMIT_SOUTH_NORTH_(KM)',
            'limit_depth': 'LIMIT_DEPTH_(KM)',
            'cbar_tick': 'COLORBAR_TICK'
        }
        self.fname_key = ['file_model', 'file_sta', 'file_eq']
        self.key_wval = ['file_model', 'file_sta', 'file_eq', 'eq_rad']
    
    def __getKey(self, value):
        for key in self.header:
            if self.header[key] == value:
                return key
            
    def __removeSpacingFname(self, fname):
        while(True):
            if (fname[0]==' '):
                fname = fname[1:]
            else:
                break
        while(True):
            if (fname[-1]==' '):
                fname = fname[:-1]
            else:
                break
        return fname
    
    def read(self, file):
        with open(file) as f:
            param_raw = f.readlines()
        param_input = []
        keys = []
        last_key = ''
        values = []
        
        for line in param_raw:
            line = line.replace('\n', '')

            if line != '' and line.replace(' ', '') != '':
                if line.lower() == 'none' or line.lower() == 'default':
                    line = line.lower()
                    
                line_splitted = line.split()
                
                if line_splitted[0] == '#':
                    last_key = self.__getKey(line_splitted[1])
                    keys.append(last_key)
                    values.append([])
                else:
                    if last_key in self.fname_key:
                        fname = self.__removeSpacingFname(line)
                        values[-1].append(fname)
                    else:
                        for num in line_splitted:
                            try:
                                values[-1].append(float(num))
                            except:
                                values[-1].append(num)
        result = {}
        for ikey, key in enumerate(keys):

            if key in self.key_wval:
                result[key] = values[ikey][0]
            else:
                if values[ikey][0] == 'none' or values[ikey][0] == 'default':
                    result[key] = values[ikey][0]
                else:
                    if key == 'model_center':
                        result[key] = {
                            'lat': values[ikey][0],
                            'lng': values[ikey][1]
                        }
                    else:
                        result[key] = values[ikey]
        return result         
