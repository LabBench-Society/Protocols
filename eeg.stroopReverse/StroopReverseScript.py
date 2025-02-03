import random

class Position:
    def __init__(self, display):
        self.Size = display.Height/12
        self.Y1 = display.Height/6
        self.Y2 = display.Height/2
        self.Y3 = display.Height - self.Y1

        self.X1 = display.Width/2 - (self.Y2 - self.Y1)
        self.X2 = display.Width/2
        self.X3 = display.Width/2 + (self.Y2 - self.Y1)

def DrawResponses(tc, position, canvas):
    canvas.Color(tc.StroopColors['r'])
    canvas.Circle(position.X2, position.Y1, position.Size)
    canvas.Color(tc.StroopColors['g'])
    canvas.Circle(position.X3, position.Y2, position.Size)
    canvas.Color(tc.StroopColors['b'])
    canvas.Circle(position.X2, position.Y3, position.Size)
    canvas.Color(tc.StroopColors['y'])
    canvas.Circle(position.X1, position.Y2, position.Size)

def ReverseStroopNeutralStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    triggerGenerator = tc.Instruments.TriggerGenerator
    position = Position(display)

    with tc.Image.GetCanvas(display) as canvas:
        canvas.Fill(True)
        DrawResponses(tc, position, canvas)

        canvas.Color(tc.StroopColors[name[0]])
        canvas.Rectangle(position.X2 - position.Size, position.Y2 - position.Size,position.X2 + position.Size, position.Y2 + position.Size)

        triggerGenerator.GenerateTriggerSequence(tc.Triggers.StartTrigger.Response01, 
                                                 tc.Triggers.Sequence()
                                                   .Add(tc.Triggers.Trigger(10).Stimulus().Code(1)))
        display.Display(canvas, tc.StroopDisplayTime, True)
        
    return True

def ReverseStroopStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    triggerGenerator = tc.Instruments.TriggerGenerator
    position = Position(display)

    with tc.Image.GetCanvas(display) as canvas:
        canvas.Fill(True)
        DrawResponses(tc, position, canvas)
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(100)

        canvas.Color(tc.StroopColors[name[1]])
        canvas.Write(display.Width/2, display.Height/2, tc.StroopWords[name[0]])

        triggerCode = 1 if name[0] == name[1] else 2
        triggerGenerator.GenerateTriggerSequence(tc.Triggers.StartTrigger.Response01, 
                                                 tc.Triggers.Sequence()
                                                   .Add(tc.Triggers.Trigger(10).Stimulus().Code(triggerCode)))
        display.Display(canvas, tc.StroopDisplayTime, True)

    return True


def IsCorrect(tc, result):
    Buttons = tc.Response.Buttons

    if (result.Stimulus[0] == 'b'):
        return True if result.Response == Buttons.B01 else False
    elif (result.Stimulus[0] == 'y'):
        return True if result.Response == Buttons.B02 else False
    elif (result.Stimulus[0] == 'r'):
        return True if result.Response == Buttons.B03 else False
    elif (result.Stimulus[0] == 'g'):
        return True if result.Response == Buttons.B04 else False
    else:
        tc.Log.Error("Invalid stimulus name: " + result.Stimulus)
        return False
    
def StroopEvaluate(tc):
    tc.Current.Annotations.SetBools("correct", [IsCorrect(tc, s) for s in tc.Current.Stimulations])   
    return True