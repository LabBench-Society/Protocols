import random
import math

class TriggerRecording:
    def __init__(self, tc):
        self.triggers = []
        self.result = tc.Current

    def Add(self, code):
        self.triggers.append(code)

    def Complete(self):
        self.result.Annotations.SetIntegers("sstTriggers", self.triggers)

class UpDownAlgorithm:
    def __init__(self, tc, stepsize, initialDelay):
        self.Log = tc.Log
        self.lowerLimit = int(tc.StopSignalLowDelayLimit)
        self.highLimit = int(tc.StopSignalHighDelayLimit)
        self.delay = initialDelay
        self.stopSignalDelay = []
        self.stepsize = stepsize

        self.delays = []

    def Complete(self, result):
        result.Annotations.SetIntegers("sstDelays", self.delays)
        result.Annotations.SetIntegers("sstStopSignalDelays", self.stopSignalDelay)
        result.Annotations.SetInteger("sstLastStopSignalDelay", self.stopSignalDelay[-1])
        self.Log.Debug("Stop Signal Delays [ {delays} ]", self.stopSignalDelay)

    def Iterate(self, answer):
        if answer:
            self.delay = int(self.delay + self.stepsize) if self.delay + self.stepsize < self.highLimit else self.highLimit
        else:
            self.delay = int(self.delay - self.stepsize) if self.delay - self.stepsize > self.lowerLimit else self.lowerLimit
        
        self.stopSignalDelay.append(self.delay)
      
class StopSignalTask:
    def __init__(self, tc, algorithm, feedback, triggers):
        self.Log = tc.Log
        self.feedback = feedback
        self.Buttons = tc.Response.Buttons
        self.display = tc.Instruments.ImageDisplay

        self.triggerGenerator = tc.Instruments.TriggerGenerator
        self.triggerTlk = tc.Triggers
        self.triggers = triggers

        self.response = tc.Instruments.Button
        self.images = tc.Assets.StopSignalGameImages
        self.algorithm = algorithm
        self.feedbackTime = tc.StopSignalFeedbackTime
        self.responseTimeout = tc.StopSignalResponseTimeout
        self.feedbackDelay = tc.StopSignalFeedbackDelay
                   
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.result = tc.Current
        self.Fiducials = tc.ExperimentalSetup != "JOYSTICK"
            
        self.Log.Information("Stop Signal Task [ CREATED ]")
    
    def Complete(self):
        self.result.Annotations.SetIntegers("sstGoSignals", self.goSignals)
        self.result.Annotations.SetBools("sstAnswer", self.answer)
        self.result.Annotations.SetIntegers("sstTime", self.time)
        self.algorithm.Complete(self.result)
        self.Log.Information("Stop Signal Task [ SAVED ]")

    def Go(self):
        self.response.Reset()
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)

        self.triggerGenerator.GenerateTriggerSequence(self.triggerTlk.StartTrigger.Response02, 
                                                      self.triggerTlk.Sequence()
                                                                     .Add(self.triggerTlk.Trigger(1).Stimulus().Code(1)))
        
        if self.signal == 0:
            self.display.Display(self.images.Left, self.Fiducials)
        else:
            self.display.Display(self.images.Right, self.Fiducials)                      
       
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
            self.answer.append(False)
            self.time.append(int(self.response.ReactionTime))
        else:           
            self.answer.append(True)
            self.time.append(int(-1))

        self.algorithm.Iterate(self.answer[-1])
        self.triggers.Add(7 if self.answer[-1] else 9)

        self.Log.Information("STOP-SIGNAL RESPONSE [ Correct: {answer}, sstDelay: {stopSignalDelay} ]", 
                        self.answer[-1], 
                        self.algorithm.stopSignalDelay[-1], 
                        self.algorithm.delay)

        self.feedback.StopFeedback(self.answer[-1])

        return self.feedbackTime

class GoSignalTask:
    def __init__(self, tc, feedback, triggers):   
        self.Log = tc.Log    
        self.Buttons = tc.Response.Buttons
        self.feedback = feedback
        self.tc = tc
        self.display = tc.Instruments.ImageDisplay

        self.triggerGenerator = tc.Instruments.TriggerGenerator
        self.triggerTlk = tc.Triggers
        self.triggers = triggers

        self.response = tc.Instruments.Button
        self.images = tc.Assets.StopSignalGameImages

        self.goDelay = tc.StopSignalHighDelayLimit
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.feedbackTime = tc.StopSignalFeedbackTime
        self.responseTimeout = tc.StopSignalResponseTimeout
        self.feedbackDelay = tc.StopSignalFeedbackDelay
        
        self.result = tc.Current
        self.Fiducials = tc.ExperimentalSetup != "JOYSTICK"
            
        self.Log.Information("Go Signal Task Created")
        
    def Complete(self):
        self.result.Annotations.SetIntegers("gtSignals", self.goSignals)
        self.result.Annotations.SetBools("gtAnswer", self.answer)
        self.result.Annotations.SetNumbers("gtTime", self.time)
    
    def Go(self):
        self.response.Reset()        
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        self.triggerGenerator.GenerateTriggerSequence(self.triggerTlk.StartTrigger.Response02, 
                                                      self.triggerTlk.Sequence()
                                                                     .Add(self.triggerTlk.Trigger(1).Stimulus().Code(1)))

        if self.signal == 0:
            self.display.Display(self.images.Left, self.Fiducials)
        else:
            self.display.Display(self.images.Right, self.Fiducials)                      
       
        return self.responseTimeout
                  
    def Feedback(self):
        button = self.response.LatchedActive
        self.time.append(self.response.ReactionTime)
        
        if button == self.Buttons.NoResponse:
            self.answer.append(False)
            self.triggers.Add(1)
        else:         
            self.answer.append(button == self.Buttons.Left if self.signal == 0 else button == self.Buttons.Right)
            self.triggers.Add(3 if self.answer[-1] else 5)
                        
        self.Log.Information("GO RESPONSE [ Button: {button}, Signal: {signal}, Correct: {answer}, Time: {time}]", 
                         button, 
                         "left" if self.signal == 0 else "right", 
                         self.answer[-1],
                         self.time[-1])

        self.feedback.GoFeedback(self.answer[-1], self.time[-1])

        return self.feedbackTime
 
class GameFeedback:
    def __init__(self, tc):
        self.tc = tc

        self.images = tc.Assets.StopSignalGameImages
        self.display = tc.Instruments.ImageDisplay

        self.score = 0
        self.accumulated = 0
        self.result = tc.Current

    def Complete(self):
        self.result.Annotations.SetInteger("score", int(self.score))

    def GoFeedback(self, answer, time):        
        display = self.display
        with self.tc.Image.GetCanvas(self.display) as canvas:
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Font("Roboto")
            canvas.TextSize(98)
            distance = display.Height/14

            if answer:
                score = math.ceil((self.tc.StopSignalResponseTimeout - time)/10)
                score = score if score > 0 else 1
                self.score = int(self.score + score)
                self.accumulated = int(self.accumulated + score)
                canvas.Color("#00FF00")
                canvas.Write(display.Width/2 , display.Height/2 - distance, "YOU WIN")
                canvas.Write(display.Width/2, display.Height/2 + distance, "+{score} points".format(score = score))
            else:
                canvas.Color("#FF0000")
                canvas.Write(display.Width/2 , display.Height/2, "YOU LOOSE")

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
                canvas.Write(display.Width/2 , display.Height/2, "YOU WIN")
            else:
                self.level = 1
                canvas.Color("#FF0000")
                canvas.Write(display.Width/2 , display.Height/2 - distance, "YOU LOOSE")
                canvas.Write(display.Width/2, display.Height/2 + distance, "-{score} points".format(score = self.accumulated))
                self.score = self.score - self.accumulated # Penalty for loosing

            self.accumulated = 0
            self.display.Display(canvas)

class CognitiveTask:
    def __init__(self, tc):
        self.tc = tc        

    def Initialize(self, stepsize, initialDelay):
        self.Triggers = TriggerRecording(self.tc)
        self.Feedback = GameFeedback(self.tc)
        self.StopTask = StopSignalTask(self.tc, UpDownAlgorithm(self.tc, stepsize, initialDelay), self.Feedback, self.Triggers)
        self.GoTask = GoSignalTask(self.tc, self.Feedback, self.Triggers)        
        return True

    def Complete(self):
        self.StopTask.Complete()
        self.GoTask.Complete()        
        self.Feedback.Complete()
        self.Triggers.Complete()
        return True
    
    def Stimulate(self):
        tc = self.tc
        display = tc.Instruments.ImageDisplay
        
        if tc.StimulusName == "STOP":
            display.Run(display.Sequence(self.StopTask)
                        .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFixationDelay)
                        .Run(lambda task: task.Go())
                        .Run(lambda task: task.Stop())
                        .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFeedbackDelay)
                        .Run(lambda task: task.Feedback()))
            
        elif tc.StimulusName == "GO":
            display.Run(display.Sequence(self.GoTask)
                        .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFixationDelay)
                        .Run(lambda task: task.Go())
                        .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFeedbackDelay)
                        .Run(lambda task: task.Feedback()))
        else:
            tc.Log.Error("Unknown stimulus: {name}".format(name = tc.StimulusName))

        return True

def CreateTask(tc):
    return CognitiveTask(tc)

def DisplayScore(tc):
    with tc.Image.GetCanvas(tc.DisplayWidth, tc.DisplayHeight) as canvas:
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(72)
        canvas.Color("#FFFFFF")
        canvas.Write(tc.DisplayWidth/2, tc.DisplayHeight/2, "Final Score: {points} points".format(points = int(tc.Current.Annotations.score)))
        return canvas.GetAsset()
    
def CalculateRT(tc):
    gtTime = tc.StopSignalGame.Annotations.gtTime
    gtAnswer = tc.StopSignalGame.Annotations.gtAnswer
    rt = [time for time, answer in zip(gtTime, gtAnswer) if answer]
    return int(sum(rt) / len(rt) if rt else 0)

def CalculateSSD(tc):
    ssd = tc.StopSignalGame.Annotations.sstStopSignalDelays
    return int(sum(ssd) / len(ssd) if ssd else 0)

def CalculateSSRT(tc):
    return CalculateRT(tc) - CalculateSSD(tc)