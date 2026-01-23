
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
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.UpdateInstruction, False)
   return True

def StartVerifyFiducial(tc):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images.FiducialCheck, True)
   return True

def CheckTriggers(tc):
   actualTriggers = tc.Instruments.TriggerDetector.Count
   expectedTriggers = 4 * tc.NumberOfRepetitions

   if actualTriggers == expectedTriggers:
      tc.Log.Information("Test PASSED! Expected {expectedTriggers} triggers and received {actualTriggers} triggers.", expectedTriggers, actualTriggers)
   else:
      tc.Log.Error("Test FAILED! Expected {expectedTriggers} triggers and received {actualTriggers} triggers.", expectedTriggers, actualTriggers)

   return actualTriggers == expectedTriggers

def Initialize(tc):
   tc.Instruments.TriggerDetector.Reset()
   return True

def Stimulate(tc,x):
   tc.Instruments.ImageDisplay.Display(tc.Assets.Images[tc.StimulusName], 500, True)
   triggers = tc.Instruments.TriggerDetector.Count
   tc.Log.Information("Number of detected triggers: {triggers}", triggers)
   return True