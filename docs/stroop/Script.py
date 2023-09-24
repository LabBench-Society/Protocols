from Serilog import Log
import traceback
import random

def getImages(tc):
    if tc.Language == "DA":
        return tc.Assets.DanishImages
    else:
        return tc.Assets.EnglishImages

def NeutralInstructions(tc):
    display = tc.Devices.Display
    display.Display(getImages(tc).GetAsset("ninstruct.png").Data)
    return True
    
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