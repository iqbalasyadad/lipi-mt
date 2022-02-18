from mtplotmodules.PlotParameter import PlotParameter
from mtplotmodules.CreateModel import CreateModel
from mtplotmodules.PlotCLI import PlotCLI

def main():
    myCLI = PlotCLI()
    myParam = PlotParameter()
    myModel = CreateModel()
    
    myCLI.displayHeader()

    while(True):
        param_file = myCLI.getInput()
        try: 
            param = myParam.read(param_file)
        except Exception as err:
            print(err)
        else:
            break    

    myModel.setInputFile(param['file_model'])
    myModel.setModelCenter(param['model_center']['lat'], param['model_center']['lng'])
    
    if param['file_sta'] != 'none':
        myModel.setStationFile(param['file_sta'])
    
    if param['file_eq'] != 'none':
        myModel.setEQFile(param['file_eq'])
        myModel.setEQRadius(param['eq_rad'])
    
    if param['slice_we'] != 'none':
        myModel.setCrossWE(param['slice_we'])
    if param['slice_sn'] != 'none':
        myModel.setCrossSN(param['slice_sn'])
    if param['slice_depth'] != 'none':
        myModel.setCrossZ(param['slice_depth'])
        
    if param['name_we'] != 'none':
        myModel.setNameWE(param['name_we'])
    if param['name_sn'] != 'none':
        myModel.setNameSN(param['name_sn'])
        
    myModel.process()                                          

    if param['limit_we'] != 'none' and param['limit_we'] != 'default':
        myModel.setWELim(param['limit_we'][0], param['limit_we'][1])
        
    if param['limit_sn'] != 'none' and param['limit_sn'] != 'default':
        myModel.setSNLim(param['limit_sn'][0], param['limit_sn'][1])
                                                     
    if param['limit_depth'] != 'none' and param['limit_depth'] != 'default':
        myModel.setZLim(param['limit_depth'][0], param['limit_depth'][1])  

    if param['cbar_tick'] != 'none' and param['cbar_tick'] != 'default':
        print('input_cbar_ok')
        myModel.setCbarTicks(param['cbar_tick'])

    
    # save plot
    try:
        if param['slice_we'] != 'none':
            myModel.plotWECross(save_output=True)
        if param['slice_sn'] != 'none':
            myModel.plotSNCross(save_output=True)
        if param['slice_depth'] != 'none':
            myModel.plotZLine(param['slice_depth'][0], save_output=True)
            myModel.plotZCross(save_output=True)
    except Exception as err:
        print(err)
    else:
        print('Success...')
        print('Saved to {}'.format(myModel.output_folder))
        
if __name__ == '__main__':
    main()