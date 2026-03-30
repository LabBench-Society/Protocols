import random 


class ResponseTask:
   def __init__(self, tc):
      self.tc = tc
      self.Cross = tc.Assets.Images.Cross
      self.Stimulating = tc.Assets.Images.Stimulating
      self.RatingInstruction = tc.Assets.Images.RatingInstruction
      self.Empty = tc.Assets.Images.Empty
      self.ratings = []    
      self.current = 0  

   def Start(self):
      self.ratings = []      
      return True
   
   def Complete(self):
      self.tc.Current.SetNumbers("ratings", self.ratings)
      return True

   def PlotRating(self, x, y):
      with self.tc.Image.GetCanvas(x, y, "#FFFFFF") as image:
         image.AlignCenter()
         image.AlignMiddle()
         image.Color("#000000")
         image.Write(x /2, y /2, "Rating: {r}".format(r = self.current))
         return image.GetImage()
      
   def Stimulate(self, freq):      
      pass

   def GenerateCues(self):
      with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as image:

         return image.GetImage()

   def GenerateSelectedCue(self):
      with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as image:

         return image.GetImage()

   def Enter(self, srTest):
      id = self.tc.CurrentState.ID
      display = self.tc.Instruments.ImageDisplay
      self.tc.Keyboard.Clear();

      if id == "CROSS":
         display.Display(self.Cross)
         return True
      if id == "SELECTION":
         display.Display(self.GenerateCues())
         return True
      if id == "DISPLAY":
         display.Display(self.GenerateSelectedCue())
         return True
      if id == "STIMULATION":
         self.Stimulate(50)
         display.Display(self.Stimulating)
         return True
      if id == "RATING":
         return True
      if id == "RESET":
         display.Display(self.RatingInstruction)
         return True
      if id == "PAUSE":
         self.current = 0
         self.tc.Log.Information("Actions; ESC) Abort, INSERT) Complete, ENTER) Continue.")
         self.tc.CurrentState.SetPlotter(lambda x, y: self.PlotRating(x,y))
         return True
      
      return False
   
   
   def Leave(self):
      id = self.tc.CurrentState.ID
      self.tc.Keyboard.Clear();

      if id == "CROSS":
         return True
      if id == "SELECTION":
         return True
      if id == "DISPLAY":
         return True
      if id == "STIMULATION":
         return True
      if id == "RATING":
         return True
      if id == "RESET":
         return True
      if id == "PAUSE":
         return True
      
      return True      
   
   def Update(self):
      id = self.tc.CurrentState.ID

      if id == "CROSS":
         self.tc.CurrentState.Status = "Remaining time: {time}".format(time = 2000 - self.tc.CurrentState.RunningTime)
         return "*" if self.tc.CurrentState.RunningTime < 500 else "SELECTION"
      
      if id == "SELECTION":
         button = self.tc.Instruments.Button
         self.tc.CurrentState.Status = "Remaining time: {time}".format(time = 2000 - self.tc.CurrentState.RunningTime)

         if self.tc.CurrentState.RunningTime > 2000: 
            self.tc.Log.Information("No response, selecting one random selection")
            return random.choice(["CUE01", "CUE02"])
         
         if button.IsLatched("1"):
            return "CUE01"

         if button.IsLatched("2"):
            return "CUE02"

         return "*" 
      
      if id == "DISPLAY":
         self.tc.CurrentState.Status = "Running time: {time}".format(time = self.tc.CurrentState.RunningTime)
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "STIMULATION"
      
      if id == "STIMULATION":
         self.tc.CurrentState.Status = "Running time: {time}".format(time = self.tc.CurrentState.RunningTime)
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "RATING"
      
      if id == "RATING":
         button = self.tc.Instruments.Button

         return "*" 
      
      if id == "RESET":
         self.tc.CurrentState.Status = "Running time: {time}".format(time = self.tc.CurrentState.RunningTime)
         return "*"
      
      if id == "PAUSE":
         self.current = self.tc.Instruments.Scale.GetCurrentRating()
         self.tc.CurrentState.Changed = True

         if self.tc.Keyboard.Pressed("ESC"):
            return "abort"
         
         if self.tc.Keyboard.Pressed("INSERT"):
            self.ratings.append(self.current)
            return "complete"
         
         if self.tc.Keyboard.Pressed("ENTER"):
            self.ratings.append(self.current)
            return "CUE"

         return "*"

      return "abort"

def CreateTask(tc):
   return ResponseTask(tc)

