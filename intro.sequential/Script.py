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
         image.Write(x /2, y /2, f"Rating: {self.current}")
         return image.GetImage()
      
   def Stimulate(self, intensity):    
      # TODO: Generate stimulation based on selected intensity
      self.tc.Log.Information("Stimulating: {intensity}", intensity)

   def GenerateCues(self):
      with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as image:
         # TODO: Generate Lure and Target Cues as assigned to button 1 (left) and button 2 (right)
         return image.GetImage()

   def GenerateSelectedCue(self):
      with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as image:
         # TODO: Generate the selected cue Lure or Target
         return image.GetImage()
   
   def Start(self):
      return True

   def Complete(self):
      return True

   def Enter(self, srTest):
      id = self.tc.CurrentState.ID
      display = self.tc.Instruments.ImageDisplay
      self.tc.Instruments.Button.Reset();

      if id == "CROSS":
         display.Display(self.Cross)
      if id == "SELECTION":
         display.Display(self.GenerateCues())
      if id == "DISPLAY":
         display.Display(self.GenerateSelectedCue())
      if id == "STIMULATION":
         self.Stimulate(50)
         display.Display(self.Stimulating)
      if id == "RATING":
         self.tc.CurrentState.SetPlotter(lambda x, y: self.PlotRating(x,y))
      if id == "RESET":
         display.Display(self.RatingInstruction)
      if id == "PAUSE":
         self.current = 0
         self.tc.Log.Information("Actions; ESC) Abort, INSERT) Complete, ENTER) Continue.")
      
      return True
      
   def Leave(self):
      return True      
   
   def Update(self):
      id = self.tc.CurrentState.ID
      self.tc.CurrentState.Status = f"Running time: {self.tc.CurrentState.RunningTime}"

      if id == "CROSS":
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "SELECTION"      
      
      if id == "SELECTION":
         if self.tc.CurrentState.RunningTime > 4000: 
            self.tc.Log.Information("No response, selecting one random selection")
            # Select a the lure
            return "DISPLAY"         
         if self.tc.Instruments.Button.IsLatched("1"):
            # Select the cue assigned to button 1
            return "DISPLAY"
         if self.tc.Instruments.Button.IsLatched("2"):
            # Select the cue assigned to button 2
            return "DISPLAY"      
         
      if id == "DISPLAY":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "STIMULATION"  
          
      if id == "STIMULATION":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "RATING"      
      
      if id == "RATING":
         button = self.tc.Instruments.Button
         self.current = self.tc.Instruments.RatioScale.GetCurrentRating()
         self.tc.CurrentState.Changed = True

         if button.IsLatched("1") or button.IsLatched("2"):
            return "RESET"      
         
      if id == "RESET":
         rating = self.tc.Instruments.RatioScale.GetCurrentRating()
         self.tc.CurrentState.Status = f"Current rating: {rating}"
         
         return "PAUSE" if rating < 0.5 else "*"
             
      if id == "PAUSE":
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "CROSS"      

      return "*"

def CreateTask(tc):
   return ResponseTask(tc)

