
def StartSize(tc):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.ScreenSizeInstruction, False)
   return True

def StartPosition(tc):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.ScreenPositionInstruction, False)
   return True

def StartFiducial(tc):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.Blank, False)
   return True

def StartUpdate(tc):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.UpdateInstruction, True)
   return True

def StartVerify(tc):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.FiducialCheck, True)
   return True

def CheckTriggers(tc):
   return True

def Initialize(tc):
   return True

def Stimulate(tc,x):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images[tc.StimulusName], 500, True)
   return True