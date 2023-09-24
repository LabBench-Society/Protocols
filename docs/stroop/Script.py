from Serilog import Log
import traceback
import random

def getImages(tc):
    if tc.Language == "DA":
        return tc.Assets.DanishImages
    else:
        return tc.Assets.EnglishImages
    
def getBlank(tc):
    return getImages(tc).GetAsset("blank.PNG").Data
        
def Initialize(tc):
    try:
        tc.Devices.Display.Display(getBlank(tc))
        return True
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False    

def Stimulate(tc, x):
    try:
        images = getImages(tc)
        key = "{name}.PNG".format(name = tc.StimulusName)
        tc.Devices.Display.Display(images.GetAsset(key).Data)       
        return True
    
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False