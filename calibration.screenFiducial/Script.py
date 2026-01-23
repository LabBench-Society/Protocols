
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

def StartVerifySize(tc):
   display = tc.Instruments.ImageDisplay
   with tc.Image.GetCanvas(display) as canvas:
      metrics = display.Metrics
      length = metrics.LengthToPixels(10)

      canvas.Font("Roboto")
      canvas.TextSize(48)
      canvas.Color("#ffffff")
      canvas.AlignCenter()
      canvas.Fill(True)

      metrics = display.Metrics
      length = metrics.LengthToPixels(10)

      canvas.Color("#ffffff")      
      canvas.Rectangle(canvas.Width/2 - length/2, canvas.Height/2 - length/2, canvas.Width/2 + length/2, canvas.Height/2 + length/2)
      canvas.AlignTop()
      canvas.Write(canvas.Width/2, canvas.Height/2 + length/2 + 20, "10cm")
      canvas.AlignLeft()
      canvas.AlignMiddle()
      canvas.Write(canvas.Width/2 + length/2 + 20, canvas.Height/2, "10cm")
      
      display.Display(canvas)

   return True

def StartAngleSize(tc):
   display = tc.Devices.ImageDisplay
   with tc.Image.GetCanvas(display) as canvas:
      metrics = display.Metrics
      length = metrics.LengthToPixels(10)

      canvas.Font("Roboto")
      canvas.TextSize(48)
      canvas.Color("#ffffff")
      canvas.AlignCenter()
      canvas.Fill(True)

      metrics = display.Metrics
      length = metrics.AngleToPixels(10)

      canvas.Color("#ffffff")      
      canvas.Rectangle(canvas.Width/2 - length/2, canvas.Height/2 - 20, canvas.Width/2 + length/2, canvas.Height/2 + 40)
      canvas.AlignTop()
      canvas.Write(canvas.Width/2, canvas.Height/2 + 60, "10°")
      
      canvas.AlignBottom()
      canvas.Write(canvas.Width /2, canvas.Height - 20, "Drawing with visual angles")
      display.Display(canvas)

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