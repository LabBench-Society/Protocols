from Serilog import Log
import traceback
import random

def getImages(tc):
    return tc.Assets.EnglishImages
   
def Instructions(tc):
    display = tc.Devices.ImageDisplay
    display.Display(getImages(tc).GetAsset("instruct.png").Data)
    return True

def Initialize(tc):
    display = tc.Devices.ImageDisplay
    display.Display(getImages(tc).GetAsset("blank.png").Data)
    return True

def Stimulate(tc, x):
    key = "{name}.png".format(name = tc.StimulusName)   
    display = tc.Devices.ImageDisplay
    display.Display(getImages(tc).GetAsset(key).Data, tc.DisplayTime)       
    return True

def IsCorrect(result):
    name = result.Stimulus
    
    if (name == 'go'):
        return 1 if result.Response == 1 else 0
    elif (name == 'nogo'):
        return 0 if result.Response == 1 else 1
    else:
        return 0
    
def Evaluate(tc):
    result = tc.Current
    tc.Current.Annotations.Add("correct", [IsCorrect(s) for s in result.Stimulations])
    return True