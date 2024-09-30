import random

def Stimulate(tc, x):
    key = "{name}.png".format(name = tc.StimulusName)   
    display = tc.Devices.Display
    display.Display(getImages(tc).GetAsset(key).Data, tc.DisplayTime)       
    return True

def IsCorrect(result):
    name = result.Stimulus
    
    if (name[0] == 'b'):
        return True if result.Response == 1 else False
    elif (name[0] == 'y'):
        return True if result.Response == 2 else False
    elif (name[0] == 'r'):
        return True if result.Response == 3 else False
    elif (name[0] == 'g'):
        return True if result.Response == 4 else False
    else:
        return 0
    
def StroopEvaluate(tc):
    result = tc.Current
    tc.Current.Annotations.SetBools("correct", [IsCorrect(s) for s in result.Stimulations])
    
    return True