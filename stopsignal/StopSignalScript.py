﻿import random
import math

class UpDownAlgorithm:
    def __init__(self, tc, stepsize, initialDelay):
        self.lowerLimit = tc.StopSignalLowDelayLimit
        self.highLimit = tc.StopSignalHighDelayLimit
        self.delay = initialDelay
        self.stopSignalDelay = []
        self.stepsize = stepsize

        self.delays = []

    def Complete(self, result):
        result.Annotations.Add("sstDelays", self.delays)
        result.Annotations.Add("sstStopSignalDelay", self.stopSignalDelay)

    def Iterate(self, answer):
        if answer:
            self.delay = self.delay + self.stepsize
            
            if self.delay > self.highLimit:
                self.delay = self.highLimit
        else:
            self.delay = self.delay - self.stepsize
            
            if self.delay < self.lowerLimit:
                self.delay = self.lowerLimit
        
        self.stopSignalDelay.append(self.delay)

class PsiAlgorithm:
    def __init__(self, tc):
        self.lowerLimit = tc.StopSignalLowDelayLimit
        self.highLimit = tc.StopSignalHighDelayLimit
        self.delays = []
        self.method = tc.Create(tc.Psychophysics.PsiMethod()
                                                .NumberOfTrials(tc.StopSignalTrials)
                                                .Function(tc.Psychophysics.Functions.Quick(Beta=1, Lambda=0.02, Gamma=0))
                                                .Alpha(X0=tc.StopSignalAlphaX0,X1=1.0,N = tc.StopSignalAlphaN)
                                                .Beta(X0=tc.StopSignalBetaX0,X1=tc.StopSignalBetaX1,N = tc.StopSignalBetaN)
                                                .Intensity(X0 = tc.StopSignalIntensityX0,X1 = 1.0,N = tc.StopSignalIntensityN))
        
        self.delay = self.Transform(self.method.Setup())     
        self.alpha = []
        self.beta = []
        self.ConfidenceLevel = tc.StopSignalConfidenceLevel
        self.alphaConfidence = []
        self.betaConfidence = []
        self.stopSignalDelay = []
        self.delays = []

    def Transform(self, x):
        return (self.highLimit - self.lowerLimit) * (1 - x) + self.lowerLimit
    
    def Complete(self, result):
        result.Annotations.Add("sstLowerLimit", self.lowerLimit)
        result.Annotations.Add("sstHighLimit", self.highLimit)
        result.Annotations.Add("sstDelays", self.delays)
        result.Annotations.Add("sstStopSignalDelay", self.stopSignalDelay)
        result.Annotations.Add("sstAlpha", self.alpha)        
        result.Annotations.Add("sstAlphaLower", [x[0] for x in self.alphaConfidence])        
        result.Annotations.Add("sstAlphaUpper", [x[1] for x in self.alphaConfidence])        
        result.Annotations.Add("sstBeta", self.beta)   
        result.Annotations.Add("sstBetaLower", [x[0] for x in self.betaConfidence])        
        result.Annotations.Add("sstBetaUpper", [x[1] for x in self.betaConfidence])                

    def Iterate(self, answer):
        self.delays.append(self.delay)

        self.delay = self.Transform(self.method.Iterate(answer))      

        alpha = self.method.EstimateAlpha()
        self.alpha.append(alpha)
        self.beta.append(self.method.EstimateBeta())
        self.alphaConfidence.append(self.method.EstimateAlphaConfidenceInterval(self.ConfidenceLevel))
        self.betaConfidence.append(self.method.EstimateBetaConfidenceInterval(self.ConfidenceLevel))
        self.stopSignalDelay.append(self.Transform(alpha))
        

class StopSignalTask:
    def __init__(self, tc, algorithm, feedback):
        self.Log = tc.Log
        self.feedback = feedback
        self.Buttons = tc.Response.Buttons
        self.display = tc.Devices.ImageDisplay
        self.response = tc.Devices.Button
        self.images = tc.Assets.StopSignalImages
        self.algorithm = algorithm
        self.feedbackTime = tc.StopSignalFeedbackTime
        self.responseTimeout = tc.StopSignalResponseTimeout
        self.feedbackDelay = tc.StopSignalFeedbackDelay
                   
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.result = tc.Current
            
        self.Log.Information("Stop Signal Task [ CREATED ]")
    
    def Complete(self):
        self.result.Annotations.Add("sstGoSignals", self.goSignals)
        self.result.Annotations.Add("sstAnswer", self.answer)
        self.result.Annotations.Add("sstTime", self.time)
        self.algorithm.Complete(self.result)
        self.Log.Information("Stop Signal Task [ SAVED ]")

    def Go(self):
        self.response.Reset()
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left)
        else:
            self.display.Display(self.images.Right)                      
       
        self.Log.Information("STOP-SIGNAL TESTING DELAY [ Delay: {delay} ]".format(delay = self.algorithm.delay))

        return self.algorithm.delay
        
    def Stop(self):
        if self.signal == 0:
            self.display.Display(self.images.StopLeft)
        else:
            self.display.Display(self.images.StopRight)    

        return self.responseTimeout - self.algorithm.delay
            
    def Feedback(self):
        if self.response.LatchedActive != self.Buttons.NoResponse:
            self.answer.append(0)
            self.time.append(self.response.ReactionTime)
        else:           
            self.answer.append(1)
            self.time.append(-1)

        self.algorithm.Iterate(True if self.answer[-1] == 1 else False)

        self.Log.Information("STOP-SIGNAL RESPONSE [ Correct: {answer}, sstDelay: {stopSignalDelay}, New Delay: {delay} ]", 
                        self.answer[-1], 
                        self.algorithm.stopSignalDelay[-1], 
                        self.algorithm.delay)

        self.feedback.StopFeedback(self.answer[-1] == 1)

        return self.feedbackTime

class GoSignalTask:
    def __init__(self, tc, feedback):   
        self.Log = tc.Log    
        self.Buttons = tc.Response.Buttons
        self.feedback = feedback
        self.tc = tc
        self.display = tc.Devices.ImageDisplay
        self.response = tc.Devices.Button
        self.images = tc.Assets.StopSignalImages

        self.goDelay = tc.StopSignalHighDelayLimit
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.feedbackTime = tc.StopSignalFeedbackTime
        self.responseTimeout = tc.StopSignalResponseTimeout
        self.feedbackDelay = tc.StopSignalFeedbackDelay
        
        self.result = tc.Current
            
        self.Log.Information("Go Signal Task Created")
        
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
       
        return self.responseTimeout
                  
    def Feedback(self):
        button = self.response.LatchedActive
        self.time.append(self.response.ReactionTime)
        
        if button == self.Buttons.NoResponse:
            self.answer.append(0)
        else:         
            if self.signal == 0: # Left
                if button == self.Buttons.Left: # Correct
                    self.answer.append(1)
                else: # wrong
                    self.answer.append(0)
                    
            else: # Right
                if button == self.Buttons.Right: # Correct
                    self.answer.append(1)
                else: # wrong
                    self.answer.append(0)
                        
        self.Log.Information("GO RESPONSE [ Button: {button}, Signal: {signal}, Correct: {answer}, Time: {time}]", 
                         button, 
                         "left" if self.signal == 0 else "right", 
                         self.answer[-1],
                         self.time[-1])

        self.feedback.GoFeedback(self.answer[-1] == 1, self.time[-1])

        return self.feedbackTime
 
class TaskFeedback:
    def __init__(self, tc):
        self.images = tc.Assets.StopSignalImages
        self.display = tc.Devices.ImageDisplay

    def Complete(self):
        pass

    def GoFeedback(self, answer, time):
        if answer:
            self.display.Display(self.images.Correct)
        else:
            self.display.Display(self.images.Wrong)

    def StopFeedback(self, answer):
        if answer:
            self.display.Display(self.images.Correct)
        else:
            self.display.Display(self.images.Wrong)

def UpDownInitialize(tc):
    feedback = TaskFeedback(tc)
    tc.Defines.Set("Feedback", feedback)
    tc.Defines.Set("StopTask", StopSignalTask(tc, UpDownAlgorithm(tc, 100, 150), feedback))
    tc.Defines.Set("GoTask", GoSignalTask(tc, feedback))
    return True

def PsiInitialize(tc):
    feedback = TaskFeedback(tc)
    tc.Defines.Set("Feedback", feedback)
    tc.Defines.Set("StopTask", StopSignalTask(tc, PsiAlgorithm(tc), feedback))
    tc.Defines.Set("GoTask", GoSignalTask(tc, feedback))
    return True

def Complete(tc):
    tc.StopTask.Complete()
    tc.GoTask.Complete()
    tc.Feedback.Complete()
    return True

def Stimulate(tc, x):   
    display = tc.Devices.ImageDisplay
    
    if tc.StimulusName == "STOP":
        display.Run(display.Sequence(tc.StopTask)
                    .Display(tc.Assets.StopSignalImages.FixationCross, tc.StopSignalFixationDelay)
                    .Run(lambda task: task.Go())
                    .Run(lambda task: task.Stop())
                    .Display(tc.Assets.StopSignalImages.FixationCross, tc.StopSignalFeedbackDelay)
                    .Run(lambda task: task.Feedback()))
        
    elif tc.StimulusName == "GO":
        display.Run(display.Sequence(tc.GoTask)
                    .Display(tc.Assets.StopSignalImages.FixationCross, tc.StopSignalFixationDelay)
                    .Run(lambda task: task.Go())
                    .Display(tc.Assets.StopSignalImages.FixationCross, tc.StopSignalFeedbackDelay)
                    .Run(lambda task: task.Feedback()))
    else:
        tc.Log.Error("Unknown stimulus: {name}".format(name = tc.StimulusName))

    return True
