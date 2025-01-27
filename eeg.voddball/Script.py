from Serilog import Log
import traceback
import random

def ResponseInstructions(tc):
    display = tc.Devices.Display
    display.Display(tc.Assets.Images.GetAsset("responseTask.png").Data)
    return True

def CountingInstructions(tc):
    display = tc.Devices.Display
    display.Display(tc.Assets.Images.GetAsset("countingTask.png").Data)
    return True

def Initialize(tc):
    display = tc.Devices.Display
    display.Display(tc.Assets.Images.GetAsset("blank.png").Data)
    return True

def Stimulate(tc, x):
    try:        
        key = "{name}.png".format(name = tc.StimulusName)   
        display = tc.Devices.Display
        display.Display(tc.Assets.Images.GetAsset(key).Data, tc.DisplayTime)    
        return True
    except Exception as e:
        # Print the exception and its stack trace
        Log.Error("An exception occurred: {exception}", e)
        Log.Debug("Stack trace:", traceback.format_exc()) 
        return False  