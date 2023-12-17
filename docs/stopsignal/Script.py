from Serilog import Log
from LabBench.Interface.Instruments.Response import ButtonID
import traceback
import random

class ImageRepository:
    def __init__(self, tc):
        images = tc.Assets.Images

        self.Left = images.GetImageFromArchive("left.png")
        self.Right = images.GetImageFromArchive("right.png")
        self.StopLeft = images.GetImageFromArchive("stopLeft.png")
        self.StopRight = images.GetImageFromArchive("stopRight.png")
        self.Correct = images.GetImageFromArchive("correct.png")
        self.Wrong = images.GetImageFromArchive("wrong.png")
        self.InstructionSound = images.GetImageFromArchive("instructionsSound.png")        
        self.InstructionVisual = images.GetImageFromArchive("instructionsVisual.png")        
        self.FixationCross = images.GetImageFromArchive("fixation.png")

class VisualStopSignal:
    def __init__(self, tc):
        self.display = tc.Devices.ImageDisplay
        self.images = tc.Images

    def run(self, signal):
        if signal == 0:
            self.display.Display(self.images.StopLeft)
        else:
            self.display.Display(self.images.StopRight)       

class AuditoryStopSignal:
    def __init__(self, tc):
        self.sound = tc.Devices.Sound
        self.stopSound = tc.Create(tc.Waveforms.Sin(1, 500, 0, int(0.2 * 44100), 44100))

    def run(self, signal):
        self.sound.playsc(self.stopSound)

class UpDownStopSignalTask:
    def __init__(self, tc, stopSignal):
        self.display = tc.Devices.ImageDisplay
        self.response = tc.Devices.Response
        self.images = tc.Images
        self.stopSignal = stopSignal
                   
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        self.lowerLimit = tc.LowDelayLimit
        self.highLimit = tc.HighDelayLimit
        self.feedbackTime = tc.FeedbackTime
        self.feedbackDelay = tc.FeedbackDelay


        self.delay = (self.highLimit - self.lowerLimit)/2 + self.lowerLimit
        self.stopSignalDelay = self.delay
        
        self.result = tc.Current
            
        Log.Information("Stop Signal Task (Up/Down) CREATED")
    
    def Complete(self):
        self.result.Annotations.Add("sstGoSignals", self.goSignals)
        self.result.Annotations.Add("sstAnswer", self.answer)
        self.result.Annotations.Add("sstTime", self.time)
        self.result.Annotations.Add("sstStopSignalDelay", self.stopSignalDelay)
        Log.Information("Stop Signal Task (Up/Down) SAVED")

    def Go(self):
        self.response.Reset()
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left)
        else:
            self.display.Display(self.images.Right)                      
       
        return self.delay
        
    def Stop(self):
        self.stopSignal.run(self.signal)
        return self.feedbackDelay - self.delay
        
    def Feedback(self):
        self.stopSignalDelay = self.delay
        
        if self.response.LatchedActive != ButtonID.BUTTON_NONE:
            self.answer.append(0)
            self.time.append(self.response.ReactionTime)
            self.display.Display(self.images.Wrong)

            self.delay = self.delay - 50
            
            if self.delay < self.lowerLimit:
                self.delay = self.lowerLimit
        
        else:           
            self.answer.append(1)
            self.time.append(-1)
            self.display.Display(self.images.Correct)

            self.delay = self.delay + 50
            
            if self.delay > self.highLimit:
                self.delay = self.highLimit
            
        Log.Information("STOP-SIGNAL RESPONSE [ Correct: {answer}, Delay: {delay} ]", self.answer[-1], self.delay)
        
        return self.feedbackTime

class PsiStopSignalTask:
    def __init__(self, tc, stopSignal):
        self.display = tc.Devices.ImageDisplay
        self.response = tc.Devices.Response
        self.images = tc.Images
        self.stopSignal = stopSignal

        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        self.lowerLimit = tc.LowDelayLimit
        self.highLimit = tc.HighDelayLimit
        self.feedbackTime = tc.FeedbackTime
        self.feedbackDelay = tc.FeedbackDelay


        self.method = tc.Create(tc.Psychophysics.PsiMethod()
                                                .NumberOfTrials(tc.Trials)
                                                .Function(tc.Psychophysics.Functions.Quick(Beta=1, Lambda=0.02, Gamma=0))
                                                .Alpha(X0=tc.AlphaX0,X1=1.0,N = tc.AlphaN)
                                                .Beta(X0=tc.BetaX0,X1=tc.BetaX1,N = tc.BetaN)
                                                .Intensity(X0 = tc.IntensityX0,X1 = 1.0,N = tc.IntensityN))
        
        self.delay = self.Transform(self.method.Setup())     
        self.alpha = []
        self.beta = []
        self.ConfidenceLevel = tc.ConfidenceLevel
        self.alphaConfidence = []
        self.betaConfidence = []
        self.stopSignalDelay = []
        self.delays = []

        self.result = tc.Current
                    
        Log.Information("Stop Signal Task (Psi Method) CREATED")
        
    def Transform(self, x):
        return (self.highLimit - self.lowerLimit) * (1 - x) + self.lowerLimit
        
    def Complete(self):
        self.result.Annotations.Add("sstGoSignals", self.goSignals)
        self.result.Annotations.Add("sstAnswer", self.answer)
        self.result.Annotations.Add("sstTime", self.time)
        self.result.Annotations.Add("sstAlpha", self.alpha)        
        self.result.Annotations.Add("sstAlphaLower", [x[0] for x in self.alphaConfidence])        
        self.result.Annotations.Add("sstAlphaUpper", [x[1] for x in self.alphaConfidence])        
        self.result.Annotations.Add("sstBeta", self.beta)   
        self.result.Annotations.Add("sstBetaLower", [x[0] for x in self.betaConfidence])        
        self.result.Annotations.Add("sstBetaUpper", [x[1] for x in self.betaConfidence])                
        self.result.Annotations.Add("sstStopSignalDelay", self.stopSignalDelay) 
        self.result.Annotations.Add("sstDelays", self.delays)
        Log.Information("Stop Signal Task (Psi Method) SAVED")
       
    def Go(self):
        self.response.Reset()
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left)
        else:
            self.display.Display(self.images.Right)                      
       
        return self.delay
        
    def Stop(self):
        self.stopSignal.run(self.signal)
        return self.feedbackDelay - self.delay
        
    def Feedback(self):
        if self.response.LatchedActive != ButtonID.BUTTON_NONE:
            self.answer.append(0)
            self.time.append(self.response.ReactionTime)
            self.display.Display(self.images.Wrong)                   
        else:           
            self.answer.append(1)
            self.time.append(-1)
            self.display.Display(self.images.Correct)
                 
        alpha = self.method.EstimateAlpha()
        self.alpha.append(alpha)
        self.beta.append(self.method.EstimateBeta())
        self.alphaConfidence.append(self.method.EstimateAlphaConfidenceInterval(self.ConfidenceLevel))
        self.betaConfidence.append(self.method.EstimateAlphaConfidenceInterval(self.ConfidenceLevel))
        self.stopSignalDelay.append(self.Transform(alpha))
        self.delays.append(self.delay)

        self.delay = self.Transform(self.method.Iterate(self.answer[-1] == 1))            

        Log.Information("STOP-SIGNAL RESPONSE [ Correct: {answer}, Delay: {stopSignalDelay}, New Delay: {delay} ]", 
                        self.answer[-1], 
                        self.stopSignalDelay[-1], 
                        self.delay)
        
        return self.feedbackTime

class GoSignalTask:
    def __init__(self, tc):       
        self.tc = tc
        self.display = tc.Devices.ImageDisplay
        self.response = tc.Devices.Response
        self.images = tc.Images

        self.goDelay = tc.HighDelayLimit
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.feedbackTime = tc.FeedbackTime
        self.feedbackDelay = tc.FeedbackDelay
        
        self.result = tc.Current
            
        Log.Information("Go Signal Task Created")
        
    def Complete(self):
        self.result.Annotations.Add("gtSignals", self.goSignals)
        self.result.Annotations.Add("gtAnswer", self.answer)
        self.result.Annotations.Add("gtTime", self.time)
    
    def Go(self):
        self.response.Reset()        
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left)
        else:
            self.display.Display(self.images.Right)                      
       
        return self.feedbackDelay
               
    def Feedback(self):
        button = self.response.LatchedActive
        self.time = self.response.ReactionTime
        
        if button == ButtonID.BUTTON_NONE:
            self.answer.append(0)
            self.display.Display(self.images.Wrong)
       
        else:         
            if self.signal == 0: # Left
                if button == ButtonID.LEFT: # Correct
                    self.answer.append(1)
                    self.display.Display(self.images.Correct)
                else: # wrong
                    self.answer.append(0)
                    self.display.Display(self.images.Wrong)
                    
            else: # Right
                if button == ButtonID.RIGHT: # Correct
                    self.answer.append(1)
                    self.display.Display(self.images.Correct)
                else: # wrong
                    self.answer.append(0)
                    self.display.Display(self.images.Wrong)
                        
        Log.Debug("GO RESPONSE [ Button: {button}, Signal: {signal}, Correct: {answer}, ]", button, "left" if self.signal == 0 else "right", self.answer[-1])
        
        return self.feedbackTime
 
def CreateImages(tc):
    return ImageRepository(tc)

def InstructionsVisual(tc):
    tc.Devices.ImageDisplay.Display(tc.Images.InstructionVisual)
    return True

def InstructionsAuditory(tc):
    tc.Devices.ImageDisplay.Display(tc.Images.InstructionSound)
    return True

def UpDownInitializeAuditory(tc):
    tc.Defines.Set("StopTask", UpDownStopSignalTask(tc, AuditoryStopSignal(tc)))
    tc.Defines.Set("GoTask", GoSignalTask(tc))
    return True

def PsiInitializeAuditory(tc):
    tc.Defines.Set("StopTask", PsiStopSignalTask(tc, AuditoryStopSignal(tc)))
    tc.Defines.Set("GoTask", GoSignalTask(tc))
    return True

def UpDownInitializeVisual(tc):
    tc.Defines.Set("StopTask", UpDownStopSignalTask(tc, VisualStopSignal(tc)))
    tc.Defines.Set("GoTask", GoSignalTask(tc))
    return True

def PsiInitializeVisual(tc):
    tc.Defines.Set("StopTask", PsiStopSignalTask(tc, VisualStopSignal(tc)))
    tc.Defines.Set("GoTask", GoSignalTask(tc))
    return True

def Complete(tc):
    tc.StopTask.Complete()
    tc.GoTask.Complete()
    return True

def Go(task):
    return task.Go()
    
def Stop(task):
    return task.Stop()
    
def Feedback(task):
    return task.Feedback()
    
def Stimulate(tc, x):   
    display = tc.Devices.ImageDisplay
    
    if tc.StimulusName == "STOP":
        display.Run(display.Sequence(tc.StopTask)
                    .Display(tc.Images.FixationCross, tc.FixationDelay)
                    .Run(Go)
                    .Run(Stop)
                    .Display(tc.Images.FixationCross, tc.FixationDelay)
                    .Run(Feedback))
        
    elif tc.StimulusName == "GO":
        display.Run(display.Sequence(tc.GoTask)
                    .Display(tc.Images.FixationCross, tc.FixationDelay)
                    .Run(Go)
                    .Display(tc.Images.FixationCross, tc.FixationDelay)
                    .Run(Feedback))
    else:
        Log.Error("Unknown stimulus: {name}".format(name = tc.StimulusName))

    return True

