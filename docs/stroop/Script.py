from Serilog import Log
import traceback
import random

class StroopTask:
    def __init__(self, tc):
        stimuli = tc.Assets.images
        self.congruent = {
                "r": stimuli.GetAsset("rr.png"),
                "g": stimuli.GetAsset("gg.png"),
                "b": stimuli.GetAsset("bb.png"),
                "y": stimuli.GetAsset("yy.png")
            }
        self.neutral = {
                "r": stimuli.GetAsset("rn.png"),
                "g": stimuli.GetAsset("gn.png"),
                "b": stimuli.GetAsset("bn.png"),
                "y": stimuli.GetAsset("yn.png")
            }
        self.incongruent = {
                "rg": stimuli.GetAsset("rg.png"),
                "rb": stimuli.GetAsset("rb.png"),
                "ry": stimuli.GetAsset("ry.png"),
                "gr": stimuli.GetAsset("gr.png"),
                "gb": stimuli.GetAsset("gb.png"),
                "gy": stimuli.GetAsset("gy.png"),
                "br": stimuli.GetAsset("br.png"),
                "by": stimuli.GetAsset("by.png"),
                "bg": stimuli.GetAsset("bg.png"),
                "yr": stimuli.GetAsset("yr.png"),
                "yb": stimuli.GetAsset("yb.png"),
                "yg": stimuli.GetAsset("yg.png"),
            }
        
    def initialize(self):
        pass
    
    def getCongruent(self):
        return self.congruent["r"]
    
    def getIncongruent(self):
        return self.congruent["rg"]
    
    def getNeutral(self):
        return self.neutral["g"]
        

def CreateTask(tc):
    return StroopTask(tc)

def Initialize(tc):
    try:
        task = tc.StroopTask
        task.initialize()
        return True
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False    

def Stimulate(tc, x):
    retValue = True
    
    try:
        task = tc.StroopTask
        display = tc.Devices.Display
    
        if (tc.StimulusName == "Congruent"):
                display.Display(task.getCongruent())
        elif (tc.StimulusName == "Inconguent"):
            display.Display(task.getIncongruent())
        elif (tc.StimulusName == "Neutral"):
            display.Display(task.getNeutral())
        else:
            raise ValueError("Unknown stimulus type")       
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        retValue = False
        
    return retValue