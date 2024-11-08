﻿import random
import math

class UpDownAlgorithm:
    def __init__(self, tc, stepsize, initialDelay):
        self.lowerLimit = tc.LowDelayLimit
        self.highLimit = tc.HighDelayLimit
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
        self.lowerLimit = tc.LowDelayLimit
        self.highLimit = tc.HighDelayLimit
        self.delays = []
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
        self.images = tc.Assets.Images
        self.algorithm = algorithm
        self.feedbackTime = tc.FeedbackTime
        self.responseTimeout = tc.ResponseTimeout
        self.feedbackDelay = tc.FeedbackDelay
                   
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
        self.images = tc.Assets.Images

        self.goDelay = tc.HighDelayLimit
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.feedbackTime = tc.FeedbackTime
        self.responseTimeout = tc.ResponseTimeout
        self.feedbackDelay = tc.FeedbackDelay
        
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
        self.images = tc.Assets.Images
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

class GameFeedback:
    def __init__(self, tc):
        self.images = tc.Assets.Images
        self.tc = tc
        self.display = tc.Devices.ImageDisplay
        self.score = 0
        self.levels = []
        self.level = 1
        self.result = tc.Current

    def Complete(self):
        self.result.Annotations.SetInteger("score", int(self.score))
        self.result.Annotations.SetIntegers("levels", self.levels)

    def GoFeedback(self, answer, time):        
        display = self.display
        with self.tc.Image.GetCanvas(self.display) as canvas:
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Font("Roboto")
            canvas.TextSize(98)
            distance = display.Height/14

            if answer:
                levelIncease = math.ceil((self.tc.ResponseTimeout - time)/10)
                levelIncease = levelIncease if levelIncease > 0 else 1
                self.score = int(self.score + self.level)
                self.level = int(self.level + levelIncease)
                canvas.Color("#00FF00")
                canvas.Write(display.Width/2 , display.Height/2 - distance, "YOU WIN")
                canvas.Write(display.Width/2, display.Height/2 + distance, "{score} points".format(score = self.score))
            else:
                canvas.Color("#FF0000")
                canvas.Write(display.Width/2 , display.Height/2, "YOU LOOSE")

            self.levels.append(self.level)
            self.display.Display(canvas)

    def StopFeedback(self, answer):
        display = self.display
        with self.tc.Image.GetCanvas(self.display) as canvas:
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Font("Roboto")
            canvas.TextSize(98)
            distance = display.Height/14

            if answer:
                canvas.Color("#00FF00")
                canvas.Write(display.Width/2 , display.Height/2 - distance, "YOU WIN")
                canvas.Write(display.Width/2, display.Height/2 + distance, "Level: {level}".format(level = self.level))
            else:
                self.level = 1
                canvas.Color("#FF0000")
                canvas.Write(display.Width/2 , display.Height/2 - distance, "YOU LOOSE")
                canvas.Write(display.Width/2, display.Height/2 + distance, "Level: {level}".format(level = self.level))

            self.levels.append(self.level)
            self.display.Display(canvas)

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

def PsiGameInitialize(tc):
    feedback = GameFeedback(tc)
    tc.Defines.Set("Feedback", feedback)
    tc.Defines.Set("StopTask", StopSignalTask(tc, PsiAlgorithm(tc), feedback))
    tc.Defines.Set("GoTask", GoSignalTask(tc, feedback))
    return True

def Complete(tc):
    tc.StopTask.Complete()
    tc.GoTask.Complete()
    tc.Feedback.Complete()
    return True

def DisplayScore(tc):
    with tc.Image.GetCanvas(tc.DisplayWidth, tc.DisplayHeight) as canvas:
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(72)
        canvas.Color("#FFFFFF")
        canvas.Write(tc.DisplayWidth/2, tc.DisplayHeight/2, "Final Score: {points} points".format(points = int(tc.Current.Annotations.score)))
        return canvas.GetAsset()


def Stimulate(tc, x):   
    display = tc.Devices.ImageDisplay
    
    if tc.StimulusName == "STOP":
        display.Run(display.Sequence(tc.StopTask)
                    .Display(tc.Assets.Images.FixationCross, tc.FixationDelay)
                    .Run(lambda task: task.Go())
                    .Run(lambda task: task.Stop())
                    .Display(tc.Assets.Images.FixationCross, tc.FeedbackDelay)
                    .Run(lambda task: task.Feedback()))
        
    elif tc.StimulusName == "GO":
        display.Run(display.Sequence(tc.GoTask)
                    .Display(tc.Assets.Images.FixationCross, tc.FixationDelay)
                    .Run(lambda task: task.Go())
                    .Display(tc.Assets.Images.FixationCross, tc.FeedbackDelay)
                    .Run(lambda task: task.Feedback()))
    else:
        tc.Log.Error("Unknown stimulus: {name}".format(name = tc.StimulusName))

    return True

