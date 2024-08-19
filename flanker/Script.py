from Serilog import Log
import traceback
import random

def getImages(tc):
    return tc.Assets.EnglishImages
   
def Instructions(tc):
    display = tc.Devices.Display
    display.Display(getImages(tc).GetAsset("instruct.png").Data)
    return True

def Initialize(tc):
    display = tc.Devices.Display
    display.Display(getImages(tc).GetAsset("blank.png").Data)
    return True

def Stimulate(tc, x):
    key = "{name}.png".format(name = tc.StimulusName)   
    display = tc.Devices.Display
    display.Display(getImages(tc).GetAsset(key).Data, tc.DisplayTime)       
    return True

def IsCorrect(result):
    name = result.Stimulus
    
    if (name[0] == 'h'):
        return 1 if result.Response == 2 else 0
    elif (name[0] == 'k'):
        return 1 if result.Response == 2 else 0
    elif (name[0] == 's'):
        return 1 if result.Response == 4 else 0
    elif (name[0] == 'c'):
        return 1 if result.Response == 4 else 0
    else:
        return 0
    
def Evaluate(tc):
    result = tc.Current
    tc.Current.Annotations.Add("correct", [IsCorrect(s) for s in result.Stimulations])
    
    return True