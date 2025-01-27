import random

def StroopNeutralStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    with tc.Image.GetCanvas(display) as canvas:
        canvas.Fill(True)
        canvas.Color(tc.StroopColors[name[0]])
        canvas.Circle(display.Width/2, display.Height/2, display.Height/8)

        display.Display(canvas, tc.StroopDisplayTime, tc.ExperimentalSetup != 'JOYSTICK')
        
    return True

def StroopStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    with tc.Image.GetCanvas(display) as canvas:
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(200)

        canvas.Color(tc.StroopColors[name[0]])
        canvas.Write(display.Width/2, display.Height/2, tc.StroopWords[name[1]])

        display.Display(canvas, tc.StroopDisplayTime, tc.ExperimentalSetup != 'JOYSTICK')
        
    return True

def IsCorrect(tc, result):
    if (result.Stimulus[0] == 'b'):
        return True if result.Response == 1 else False
    elif (result.Stimulus[0] == 'y'):
        return True if result.Response == 2 else False
    elif (result.Stimulus[0] == 'r'):
        return True if result.Response == 3 else False
    elif (result.Stimulus[0] == 'g'):
        return True if result.Response == 4 else False
    else:
        tc.Log.Error("Invalid stimulus name: " + result.Stimulus)
        return False
    
def StroopEvaluate(tc):
    tc.Current.Annotations.SetBools("correct", [IsCorrect(tc, s) for s in tc.Current.Stimulations])   
    return True