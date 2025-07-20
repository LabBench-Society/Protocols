
class Checkerboard:
    def __init__(self, tc):
        self.tc = tc
        self.N = 16
        self.F = 0.5
        self.A = 23.824;

    def Setup(self, N, F):
        display = self.tc.Instruments.ImageDisplay
        self.N = N
        self.F = F
        self.Period = 1000 / F
        self.count = 0
        self.evenImage = self.CreateImage(0)
        self.oddImage = self.CreateImage(1)
        display.Display(self.evenImage)

        return True
    
    def GetPeriod(self):
        return 1/self.F
    
    def Initialize(self):
        display = self.tc.Instruments.ImageDisplay
        display.Display(self.evenImage)
        self.count = 0

        return True      
    
    def CreateImage(self, remainder):
        display = self.tc.Instruments.ImageDisplay

        with self.tc.Image.GetCanvas(display) as canvas:
            metrics = display.Metrics
            L = metrics.AngleToPixels(self.A / self.N)
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
            canvas.Line(canvas.Width/2 - L, canvas.Height/2, canvas.Width/2 + L, canvas.Height/2)
            canvas.Line(canvas.Width/2, canvas.Height/2 - L, canvas.Width/2, canvas.Height/2 + L)

            return canvas.GetImage() 
        
    def Stimulate(self):
        display = self.tc.Instruments.ImageDisplay
        self.count = self.count + 1
        image = self.evenImage if self.count % 2 == 0 else self.oddImage

        self.tc.Scheduler.Run(self.tc.Scheduler.Create()
                              .Add(self.Period/2, lambda: display.Display(image, True))
                              .Add(self.Period/2, lambda: display.Display(image, False)))

        return True      

def CreateCheckerboard(tc):
    return Checkerboard(tc)

