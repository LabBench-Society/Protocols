
def Stimulate(tc, x):
    key = "{name}.png".format(name = tc.StimulusName)   
    display = tc.Devices.ImageDisplay
    display.Display(tc.Assets.Images.GetAsset(key).Data, tc.DisplayTime)    
    return True
