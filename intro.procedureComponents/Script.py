
def Initialize(contect):
    return True

def Stimulate(context, x):
    context.Instruments.Stimulator.Generate("port2", context.Stimulus)
    context.Instruments.ImageDisplay.Display(context.Assets.Images.Cue, 250, True)
    return True