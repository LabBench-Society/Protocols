
def Stimulate(tc, x):
    tc.Instruments.ImageDisplay.Display(tc.Assets.Images[tc.StimulusName], tc.DisplayTime, True)    
    return True
