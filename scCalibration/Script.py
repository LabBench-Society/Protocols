def StartFiducial(tc):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.FiducialInstruction, True)
   return True

def CheckTriggers(tc):
   return True

def Initialize(tc):
   return True

def Stimulate(tc,x):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images[tc.StimulusName], True)
   return True