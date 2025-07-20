
class Checkerboard:
    def __init__(self, tc):
        self.tc = tc
        self.N = 16
        self.F = 0.5
        self.A = 23.824;

    def Initialize(self, N, F):
        display = self.tc.Instruments.ImageDisplay
        self.N = N
        self.F = F
        self.count = 0
        self.evenImage = self.CreateImage(0)
        self.oddImage = self.CreateImage(1)
        display.Display(self.evenImage)

        return True
    
    def CreateImage(self, remainder):
        display = self.tc.Instruments.ImageDisplay

        with self.tc.Image.GetCanvas(display) as canvas:
            metrics = display.Metrics
            L = metrics.AngleToPixels(self.A / self.N)
            canvas.Fill(True)

            for n in range(self.N):
                for m in range(self.N):
                    canvas.Color("#000000" if n*m % 2 == remainder else "#FFFFFF")
                    canvas.Rectangle(m*L, n*L, (m+1)*L - 1, (n+1)* L)                    

            return canvas.GetImage() 

    def Stimulate(self):
        display = self.tc.Instruments.ImageDisplay
        self.count = self.count + 1

        if self.count % 2 == 0:
            pass
        else:
            pass

        return True      

def CreateCheckerboard(tc):
    return Checkerboard(tc)

