from Serilog import Log
import traceback
import random

def getImages(tc):
    if tc.Language == "DA":
        return tc.Assets.DanishImages
    else:
        return tc.Assets.EnglishImages
    
def Initialize(tc):
    display = tc.Devices.Display
    display.Display(getImages(tc).GetAsset("blank.PNG").Data)
    return True

def Stimulate(tc, x):
    key = "{name}.PNG".format(name = tc.StimulusName)   
    display = tc.Devices.Display
    display.Display(getImages(tc).GetAsset(key).Data)       
    return True