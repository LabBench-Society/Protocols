import random

class RandomWalk:
   def __init__(self, tc):
      self.tc = tc
      self.value = 0
      self.step = 0.2

   def Sample(self):
      scale = self.tc.Instruments.RatioScale
      self.value = self.value - self.step if scale.Length * random.random() < scale.GetRatioRating()   else self.value + self.step
      self.value = max(0, min(scale.Length, self.value))

      return [self.value]

def CreateRandomWalk(tc):  
   return RandomWalk(tc)