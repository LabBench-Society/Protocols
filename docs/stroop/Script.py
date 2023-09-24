from Serilog import Log
import traceback
import random

def generateSequence(size, images):
    keys = list(images.keys())
    retValue = [keys[n % len(keys)] for n in range(size)]
    random.shuffle(retValue)
    return retValue

def getImages(tc):
    if tc.Language == "DA":
        return tc.Assets.DanishImages
    else:
        return tc.Assets.EnglishImages
    
def getBlank(tc):
    images = getImages(tc)
    return images.GetAsset("blank.PNG").Data

def LoadImages(tc):
    images = getImages(tc)
    return {
                "rr": images.GetAsset("rr.PNG").Data,
                "gg": images.GetAsset("gg.PNG").Data,
                "bb": images.GetAsset("bb.PNG").Data,
                "yy": images.GetAsset("yy.PNG").Data,        
                "rn": images.GetAsset("rn.PNG").Data,
                "gn": images.GetAsset("gn.PNG").Data,
                "bn": images.GetAsset("bn.PNG").Data,
                "yn": images.GetAsset("yn.PNG").Data,
                "rg": images.GetAsset("rg.PNG").Data,
                "rb": images.GetAsset("rb.PNG").Data,
                "ry": images.GetAsset("ry.PNG").Data,
                "gr": images.GetAsset("gr.PNG").Data,
                "gb": images.GetAsset("gb.PNG").Data,
                "gy": images.GetAsset("gy.PNG").Data,
                "br": images.GetAsset("br.PNG").Data,
                "by": images.GetAsset("by.PNG").Data,
                "bg": images.GetAsset("bg.PNG").Data,
                "yr": images.GetAsset("yr.PNG").Data,
                "yb": images.GetAsset("yb.PNG").Data,
                "yg": images.GetAsset("yg.PNG").Data                
        }
        
def Initialize(tc):
    try:
        tc.Devices.Display.Display(getBlank(tc))
        return True
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False    

def Stimulate(tc, x):
    try:
        tc.Devices.Display.Display(tc.Images[tc.StimulusName])       
        return True
    
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False