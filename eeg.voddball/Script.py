
def Stimulate(tc, x):
    tc.Instruments.ImageDisplay.Display(tc.Assets.Images.GetAsset(tc.StimulusName).Data, tc.DisplayTime, True)    
    return True
