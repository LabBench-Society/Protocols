import random

# ================================ COMFIGURATION FUNCTIONS ==========================================

def GenerateCreamSequence(tc):
   sequence = list(range(4))
   random.shuffle(sequence)
   return sequence

def GenerateLocationSequence(tc):
   sequence = list(range(4))
   random.shuffle(sequence)
   return sequence

def GetTimeSlotDuration(tc):
    return 10 if tc.SESSION_NAME.startswith('TEST') else 45*60

def GetCOVASDuration(tc):
    return 60 if tc.SESSION_NAME.startswith('TEST') else 600

def GetCreamNames():
   return [ 'Cream A', 'Cream B', 'Cream C', 'Cream D']

def GetLocationNames():
   return [ 'A1', 'A2', 'A3', 'A4' ]

def GetLocationColors():
   return [ '#8FAADC', '#A9D18E', '#F4B183', '#FFD966' ]
     
def GetPruritogenSES01(tc):
   return "Cowhage" if tc.SubjectNumber % 2 == 0 else "Histamine"

def GetPruritogenSES02(tc):
   return "Histamine" if tc.SubjectNumber % 2 == 0 else "Cowhage"

# ================= TESTING SETTING ANNOTATIONS =====================================================

def Annotate(tc):
   annotations = tc.Current.Annotations
   annotations.SetInteger("A", 1)
   annotations.SetNumber("B", 2.0)
   annotations.SetBool("Happy", True)
   annotations.SetString("Greeting", "Hello, World!")

   annotations.SetIntegers("As", [1, 2, 3])
   annotations.SetNumbers("Bs", [1.0, 2.0])
   annotations.SetBools("Happyness", [True, False])
   annotations.SetStrings("Greetings", ["Hello, World!", "Bonjour le monde!", "Ciao mondo!"])

   return True

# ================= TIME SLOT INSTRUCTIONS ==========================================================

def GetTimeSlot(tc):
   if 'SLOT01' in tc.Current.ID:
      return 1
   if 'SLOT02' in tc.Current.ID:
      return 2
   if 'SLOT03' in tc.Current.ID:
      return 3
   if 'SLOT04' in tc.Current.ID:
      return 4
   if 'SLOT05' in tc.Current.ID:
      return 5
   if 'SLOT06' in tc.Current.ID:
      return 6
   
   return 0

def TimeSlotInstruction(tc):
   slot = GetTimeSlot(tc)
   tc.Log.Debug("Time slot: {slot}", slot)
   markerColors = ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]

   if (slot == 1):
      markerColors[tc.LocationSequence[0]] = "#4472C4"
   elif (slot == 2):
      markerColors[tc.LocationSequence[1]] = "#4472C4"
   elif (slot == 3):
      markerColors[tc.LocationSequence[2]] = "#4472C4"
      markerColors[tc.LocationSequence[0]] = "#FF0000"
   elif (slot == 4):
      markerColors[tc.LocationSequence[3]] = "#4472C4"
      markerColors[tc.LocationSequence[1]] = "#FF0000"
   elif (slot == 5):
      markerColors[tc.LocationSequence[2]] = "#FF0000"
   elif (slot == 6):
      markerColors[tc.LocationSequence[3]] = "#FF0000"

   imageEngine = tc.Image.GetImageEngine(tc.Assets.Sequence.AreaPreparation)
   imageEngine.ReplaceColor([imageEngine.CreateMask(tc.Assets.Sequence.AreaPreparation, color) for color in GetLocationColors()], markerColors)

   if slot in ['SLOT01', 'SLOT02', 'SLOT03', 'SLOT04']:
      imageEngine.AddImage(tc.Assets.Sequence.ApplyCreamOverlay)
   if slot in ['SLOT03', 'SLOT04', 'SLOT05', 'SLOT06']:
      imageEngine.AddImage(tc.Assets.Sequence.RemoveCreamOverlay)

   return imageEngine.GetImageAsset() 

def DisplayTimeSlotInstruction(tc):
   tc.Devices.SubjectInstructions.Display(TimeSlotInstruction(tc).Image)
   return True

# ================= FUNCTIONS FOR THE PREPARATION STEPS =============================================

def ApplicationEnabled(tc):
   enabled = [True, True, True, True, False, False]
   return enabled[GetTimeSlot(tc) - 1]

def RemovalEnabled(tc):
   enabled = [False, False, True, True, True, True]
   return enabled[GetTimeSlot(tc) - 1]

def Application(tc):
   slot = GetTimeSlot(tc)

   if (slot < 5):
      return GetCreamNames()[tc.CreamSequence[slot -1]]

   return "No cream"


# ================ FUNCTIONS FOR PRURITOGENS =============================

def GetApplyInstructionImage(tc):
   if tc.ActiveSession == "SES01":
      return tc.Assets.Sequence.ApplyCowhage if GetPruritogenSES01(tc) == "Cowhage" else tc.Assets.Sequence.ApplyHistamine
   else:
      return tc.Assets.Sequence.ApplyCowhage if GetPruritogenSES02(tc) == "Cowhage" else tc.Assets.Sequence.ApplyHistamine

def GetRemovalInstructionImage(tc):
   if tc.ActiveSession == "SES01":
      return tc.Assets.Sequence.RemoveCowhage if GetPruritogenSES01(tc) == "Cowhage" else tc.Assets.Sequence.RemoveHistamine
   else:
      return tc.Assets.Sequence.RemoveCowhage if GetPruritogenSES02(tc) == "Cowhage" else tc.Assets.Sequence.RemoveHistamine


def PruritogenApplication(tc):
   markerColors = ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]
   areaAssignment = tc.LocationSequence 

   if ('SITE01' in tc.Current.ID):
      markerColors[int(areaAssignment[0])] = "#4472C4"
   elif ( 'SITE02' in tc.Current.ID):
      markerColors[int(areaAssignment[1])] = "#4472C4"
   elif ('SITE03' in tc.Current.ID):
      markerColors[int(areaAssignment[2])] = "#4472C4"
   elif ('SITE04' in tc.Current.ID):
      markerColors[int(areaAssignment[3])] = "#4472C4"

   instructionImage = GetApplyInstructionImage(tc)
   imageEngine = tc.Image.GetImageEngine(instructionImage)
   imageEngine.ReplaceColor([imageEngine.CreateMask(tc.Assets.Sequence.AreaPreparation, color) for color in GetLocationColors()], markerColors)

   return imageEngine.GetImageAsset() 

def PruritogenRemoval(tc):
   markerColors = ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]
   areaAssignment = tc.LocationSequence 

   if ('SITE01' in tc.Current.ID):
      markerColors[int(areaAssignment[0])] = "#FF0000"
   elif ( 'SITE02' in tc.Current.ID):
      markerColors[int(areaAssignment[1])] = "#FF0000"
   elif ( 'SITE03' in tc.Current.ID):
      markerColors[int(areaAssignment[2])] = "#FF0000"
   elif ( 'SITE04' in tc.Current.ID):
      markerColors[int(areaAssignment[3])] = "#FF0000"

   instructionImage = GetRemovalInstructionImage(tc)
   imageEngine = tc.Image.GetImageEngine(instructionImage)
   imageEngine.ReplaceColor([imageEngine.CreateMask(tc.Assets.Sequence.AreaPreparation, color) for color in GetLocationColors()], markerColors)

   return imageEngine.GetImageAsset() 