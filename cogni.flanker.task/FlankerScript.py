
def GenerateImage(tc, name):
    with tc.Image.GetCanvas(1920,1080) as canvas:
        canvas.Font('Roboto')
        canvas.TextSize(200)
        canvas.Color("#FFFFFF")
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Write(1920/2, 1080/2, (3*name [1]) + name[0] + (3*name[1]))
        return canvas.GetImage()

def GetImages(tc):
    return {
        'CH': GenerateImage(tc, 'CH'),
        'CK': GenerateImage(tc, 'CK'),
        'CS': GenerateImage(tc, 'CS'),
        'HC': GenerateImage(tc, 'HC'),
        'HK': GenerateImage(tc, 'HK'),
        'HS': GenerateImage(tc, 'HS'),
        'KC': GenerateImage(tc, 'KC'),
        'KH': GenerateImage(tc, 'KH'),
        'KS': GenerateImage(tc, 'KS'),
        'SC': GenerateImage(tc, 'SC'),
        'SH': GenerateImage(tc, 'SH'),
        'SK': GenerateImage(tc, 'SK')
    }
    
def Stimulate(tc, x):
    tc.Instruments.ImageDisplay.Display(tc.Images[tc.StimulusName], tc.DisplayTime, tc.ExperimentalSetup != "JOYSTICK")       
    return True

def IsCorrect(tc, result):
    name = result.Stimulus
    return result.Response == tc.Response.Buttons.Left if name[0] == 'H' or name[0] == 'K' else result.Response == tc.Response.Buttons.Right
    
def Evaluate(tc):
    tc.Current.Annotations.SetBools("correct", [IsCorrect(tc, s) for s in tc.Current.Stimulations])    
    return True