
class Checkerboard:
    def __init__(self, tc):
        self.tc = tc
        self.N = 16
        self.F = 0.5
        self.A = 23.824;

    def Setup(self, N, F):
        self.display = self.tc.Instruments.ImageDisplay
        self.N = N
        self.F = F
        self.Period = 1000 / F
        self.count = 0
        self.evenImage = self.CreateImage(0)
        self.oddImage = self.CreateImage(1)
        self.display.Display(self.evenImage)
        return True
    
    def GetPeriod(self):
        return 1/self.F
    
    def Initialize(self):
        self.display.Display(self.evenImage)
        self.count = 0
        return True      
    
    def CreateImage(self, remainder):
        with self.tc.Image.GetCanvas(self.display) as canvas:
            L = self.display.Metrics.AngleToPixels(self.A / self.N)
            Lc = self.display.Metrics.AngleToPixels(self.A / 16)
            canvas.Fill(True)
            xoffset = (canvas.Width - self.N*L)/2
            yoffset = (canvas.Height - self.N*L)/2

            for n in range(self.N):
                for m in range(self.N):
                    x1 = m*L + xoffset
                    y1 = n*L + yoffset
                    x2 = (m + 1) * L - 1 + xoffset
                    y2 = (n + 1) * L - 1 + yoffset
                    color = "#000000" if (m + (n % 2)) % 2 == remainder else "#FFFFFF"
                    canvas.Color(color)
                    canvas.Rectangle(x1, y1, x2, y2)                    

            canvas.Color("#FF0000")
            canvas.StrokeWidth(3)
            canvas.Line(canvas.Width/2 - Lc, canvas.Height/2, canvas.Width/2 + Lc, canvas.Height/2)
            canvas.Line(canvas.Width/2, canvas.Height/2 - Lc, canvas.Width/2, canvas.Height/2 + Lc)

            return canvas.GetImage() 
        
    def Display(self, image, fiducial):
        self.display.Display(image, fiducial)
        return self.Period/2
        
    def Stimulate(self):
        triggerGenerator = self.tc.Instruments.TriggerGenerator

        self.count = self.count + 1
        image = self.evenImage if self.count % 2 == 0 else self.oddImage

        triggerGenerator.GenerateTriggerSequence(self.tc.Triggers.StartTrigger.Response01, 
                                                 self.tc.Triggers.Sequence()
                                                                 .Add(self.tc.Triggers.Trigger(1).Stimulus().Digital().Code(1)))

        self.tc.Scheduler.Run(self.tc.Scheduler.Create()
                              .Add(lambda: self.Display(image, True))
                              .Add(lambda: self.Display(image, False)))

        return True      

def CreateCheckerboard(tc):
    return Checkerboard(tc)

