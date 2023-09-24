from Serilog import Log
import traceback
import random

class StroopTask:
    def __init__(self, tc):
        if tc.Language == "DA":
            stimuli = tc.Assets.DanishImages
        else:
            stimuli = tc.Assets.EnglishImages
            
        self.blank = stimuli.GetAsset("blank.PNG")
        
        self.congruent = {
                "r": stimuli.GetAsset("rr.PNG"),
                "g": stimuli.GetAsset("gg.PNG"),
                "b": stimuli.GetAsset("bb.PNG"),
                "y": stimuli.GetAsset("yy.PNG")
            }
        self.neutral = {
                "r": stimuli.GetAsset("rn.PNG"),
                "g": stimuli.GetAsset("gn.PNG"),
                "b": stimuli.GetAsset("bn.PNG"),
                "y": stimuli.GetAsset("yn.PNG")
            }
        self.incongruent = {
                "rg": stimuli.GetAsset("rg.PNG"),
                "rb": stimuli.GetAsset("rb.PNG"),
                "ry": stimuli.GetAsset("ry.PNG"),
                "gr": stimuli.GetAsset("gr.PNG"),
                "gb": stimuli.GetAsset("gb.PNG"),
                "gy": stimuli.GetAsset("gy.PNG"),
                "br": stimuli.GetAsset("br.PNG"),
                "by": stimuli.GetAsset("by.PNG"),
                "bg": stimuli.GetAsset("bg.PNG"),
                "yr": stimuli.GetAsset("yr.PNG"),
                "yb": stimuli.GetAsset("yb.PNG"),
                "yg": stimuli.GetAsset("yg.PNG"),
            }
        
    def initialize(self, tc):
        self.numberOfStimuli = tc.NumberOfCongruentStimuli * tc.CongruentRepetitions
        
        ckeys = list(self.congruent.keys())
        self.congruentId = [ckeys[n % len(self.congruent)] for n in range(self.numberOfStimuli)]
        self.congruentIndex = 0
    
    def getCongruent(self):
        if self.congruentIndex >= self.numberOfStimuli:
            raise ValueError("Congruent index out of bounds")
        
        retValue = self.congruent[self.congruentId[self.congruentIndex]].Data
        self.congruentIndex = self.congruentIndex + 1                          
        return retValue
    
    def getNeutral(self):
        return self.neutral["g"].Data

    def getIncongruent(self):
        return self.incongruent["rg"].Data 
    
    def getBlank(self):
        return self.blank.Data

def CreateTask(tc):
    return StroopTask(tc)

def Initialize(tc):
    try:
        task = tc.StroopTask
        display = tc.Devices.Display
        task.initialize(tc)
        display.Display(task.getBlank())
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
                display.Display(task.getCongruent(), tc.DisplayTime)
        elif (tc.StimulusName == "Inconguent"):
            display.Display(task.getIncongruent(), tc.DisplayTime)
        elif (tc.StimulusName == "Neutral"):
            display.Display(task.getNeutral(), tc.DisplayTime)
        else:
            raise ValueError("Unknown stimulus type")       
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        retValue = False
        
    return retValue