import random

def StroopNeutralStimulate(tc, x):
    display = tc.Devices.ImageDisplay
    name =  tc.StimulusName
    with tc.Image.GetCanvas(display) as canvas:
        if (name[0] == 'b'):
            canvas.Color("#0000FF")
        elif (name[0] == 'y'):
            canvas.Color("#FFFF00")
        elif (name[0] == 'r'):
            canvas.Color("#FF0000")
        elif (name[0] == 'g'):
            canvas.Color("#00FF00")
        else:
            return False

        canvas.Fill(True)
        canvas.Circle(display.Width/2, display.Height/2, display.Height/8)
        display.Display(canvas, tc.DisplayTime, True)
        
    return True

def StroopStimulate(tc, x):
    display = tc.Devices.ImageDisplay
    name =  tc.StimulusName
    with tc.Image.GetCanvas(display) as canvas:
        if (name[0] == 'b'):
            canvas.Color("#0000FF")
        elif (name[0] == 'y'):
            canvas.Color("#FFFF00")
        elif (name[0] == 'r'):
            canvas.Color("#FF0000")
        elif (name[0] == 'g'):
            canvas.Color("#00FF00")
        else:
            return False

        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(200)

        if (name[1] == 'b'):
            canvas.Write(display.Width/2, display.Height/2, "BLUE")
        elif (name[1] == 'y'):
            canvas.Write(display.Width/2, display.Height/2, "YELLOW")
        elif (name[1] == 'r'):
            canvas.Write(display.Width/2, display.Height/2, "RED")
        elif (name[1] == 'g'):
            canvas.Write(display.Width/2, display.Height/2, "GREEN")
        else:
            return False

        display.Display(canvas, tc.DisplayTime, True)
        
    return True

def IsCorrect(tc, result):
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
        tc.Log.Error("Invalid stimulus name: " + name)
        return False
    
def StroopEvaluate(tc):
    tc.Current.Annotations.SetBools("correct", [IsCorrect(tc, s) for s in tc.Current.Stimulations])   
    return True