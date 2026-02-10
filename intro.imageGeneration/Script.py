import random

def RandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return "#{r:02x}{g:02x}{b:02x}".format(r = r, g = g, b = b)

def Shapes(tc):
   display = tc.Instruments.ImageDisplay
   with tc.Image.GetCanvas(display) as canvas:
      canvas.Font("Monospace")
      canvas.TextSize(24)
      canvas.Color("#ffffff")
      canvas.AlignCenter()
      canvas.AlignBottom()

      # Setting up the different drawing regions
      cvsWidth = canvas.Width / 4
      cvsHeight = canvas.Height / 2
      xoffset = 0
      yoffset = 0

      # Drawing points of different sizes
      numberOfPoints = 5

      canvas.RoundStrokeCap()
      x_values = [random.uniform(40, cvsWidth - 40) for _ in range(numberOfPoints)]
      y_values = [random.uniform(40, cvsHeight - 40) for _ in range(numberOfPoints)]
      width_values = [random.uniform(5, 20) for _ in range(numberOfPoints)]
      canvas.Color("#ff00ff")

      for x, y, width in zip(x_values, y_values, width_values):
         canvas.StrokeWidth(width)
         canvas.Point(x + xoffset,y + yoffset)

      canvas.SquareStrokeCap()
      x_values = [random.uniform(40, cvsWidth -40) for _ in range(numberOfPoints)]
      y_values = [random.uniform(40, cvsHeight - 40) for _ in range(numberOfPoints)]
      width_values = [random.uniform(5, 20) for _ in range(numberOfPoints)]
      canvas.Color("#00ff00")

      for x, y, width in zip(x_values, y_values, width_values):
         canvas.StrokeWidth(width)
         canvas.Point(x + xoffset,y + yoffset)

      canvas.Color("#ffffff")
      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Fill(True)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Points")
      canvas.Fill(False)

      #Drawing lines
      xoffset = xoffset + cvsWidth
      numberOfLines = 10
      x1_values = [random.uniform(40, cvsWidth - 40) for _ in range(numberOfLines)]
      y1_values = [random.uniform(40, cvsHeight - 40) for _ in range(numberOfLines)]
      x2_values = [random.uniform(40, cvsWidth - 40) for _ in range(numberOfLines)]
      y2_values = [random.uniform(40, cvsHeight - 40) for _ in range(numberOfLines)]
      width_values = [random.uniform(1, 10) for _ in range(numberOfLines)]

      canvas.RoundStrokeCap()
      for x1, y1,x2,y2, width in zip(x1_values, y1_values,x2_values, y2_values, width_values):
         canvas.Color(RandomColor())
         canvas.StrokeWidth(width)
         canvas.Line(x1 + xoffset,y1 + yoffset,x2 + xoffset,y2 + yoffset)

      canvas.Color("#ffffff")
      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Lines")

      #Drawing circles
      xoffset = xoffset + cvsWidth
      canvas.Color("#ff0000")
      canvas.Fill(True)
      canvas.Circle(xoffset + cvsWidth/2, yoffset + cvsHeight / 2, cvsHeight/4)

      canvas.StrokeWidth(4)
      canvas.Color("#ffffff")
      canvas.Fill(False)
      canvas.Circle(xoffset + cvsWidth/2, yoffset + cvsHeight / 3, cvsHeight/4)

      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Circles")

      #Drawing rectangles
      xoffset = xoffset + cvsWidth

      canvas.Color("#00ff00")
      canvas.Fill(True)
      canvas.Rectangle(xoffset + 30, yoffset + 30, xoffset + 30 + cvsWidth/2, yoffset + cvsHeight/2)

      canvas.StrokeWidth(4)
      canvas.Color("#ffffff")
      canvas.Fill(False)
      canvas.Rectangle(xoffset + cvsWidth/4, yoffset + cvsHeight/4, xoffset + 0.8*cvsWidth, yoffset + 0.8*cvsHeight)

      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Rectangles")

      #Drawing round rectangle      
      xoffset = 0
      yoffset = yoffset + cvsHeight

      canvas.Color("#0000ff")
      canvas.Fill(True)
      canvas.Rectangle(xoffset + 30, yoffset + 30, xoffset + 30 + cvsWidth/2, yoffset + cvsHeight/2, 20)

      canvas.StrokeWidth(4)
      canvas.Color("#ffffff")
      canvas.Fill(False)
      canvas.Rectangle(xoffset + cvsWidth/4, yoffset + cvsHeight/4, xoffset + 0.8*cvsWidth, yoffset + 0.8*cvsHeight, 40)

      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Rounded Rectangle")

      #Drawing assymetric rounded rectangle
      xoffset = xoffset + cvsWidth

      canvas.Color("#ff00ff")
      canvas.Fill(True)
      canvas.Rectangle(xoffset + 30, yoffset + 30, xoffset + 30 + cvsWidth/2, yoffset + cvsHeight/2, 40, 80)

      canvas.StrokeWidth(4)
      canvas.Color("#ffffff")
      canvas.Fill(False)
      canvas.Rectangle(xoffset + cvsWidth/4, yoffset + cvsHeight/4, xoffset + 0.8*cvsWidth, yoffset + 0.8*cvsHeight, 100, 50)

      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Assymetric Rectangle")

      #Drawing paths
      xoffset = xoffset + cvsWidth

      with canvas.CreatePath() as path:
         path.Move(xoffset + 40, yoffset + 40)
         path.RelativeLine((cvsWidth - 80), cvsHeight/2 - 40)
         path.RelativeLine(-(cvsWidth - 80), cvsHeight/2 -40)
         path.Close()
         canvas.StrokeWidth(15)
         canvas.RoundStrokeCap()
         canvas.Draw(path)

      with canvas.CreatePath() as path:
         path.Move(xoffset + cvsWidth - 40, yoffset + 40)
         path.RelativeLine(-0.6*(cvsWidth - 40), cvsHeight/2 - 40)
         path.RelativeLine(0.6*(cvsWidth - 40), cvsHeight/2 -40)
         canvas.StrokeWidth(15)
         canvas.Color("#ffff00")
         canvas.RoundStrokeCap()
         canvas.Draw(path)

      canvas.Color("#ffffff")
      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Line paths")

      display.Display(canvas)

      #Drawing text on paths
      xoffset = xoffset + cvsWidth

      with canvas.CreatePath() as path:
         path.Move(xoffset + 40, yoffset + 40)
         path.RelativeLine(cvsWidth - 80, cvsHeight - 80)
         canvas.Write(path, 0, 0, "Text along a line")

      canvas.StrokeWidth(1)
      canvas.Rectangle(xoffset, yoffset, xoffset + cvsWidth, yoffset + cvsHeight)
      canvas.Write(cvsWidth/2 + xoffset, cvsHeight + yoffset - 10, "Text on paths")

      display.Display(canvas)

   return True

def Color(tc):
   display = tc.Instruments.ImageDisplay
   with tc.Image.GetCanvas(display) as canvas:
      canvas.Font("Roboto")
      canvas.AlignCenter()
      canvas.AlignMiddle()
      canvas.TextSize(48)

      canvas.Fill(True)
      canvas.Color("#34C0EB")
      canvas.Rectangle(0.1*canvas.Width, 0.1*canvas.Height, 0.4*canvas.Width, 0.4*canvas.Height)
      canvas.Color("#FFFFFF")
      canvas.Write(((0.4-0.1)/2 + 0.1) * canvas.Width,((0.4-0.1)/2 + 0.1)*canvas.Height, "#34C0EB")

      canvas.Fill(True)
      canvas.Color("#ED5197")
      canvas.Rectangle(0.3*canvas.Width, 0.3*canvas.Height, 0.6*canvas.Width, 0.6*canvas.Height)
      canvas.Color("#FFFFFF")
      canvas.Write(((0.6-0.3)/2 + 0.3) * canvas.Width,((0.6-0.3)/2 + 0.3)*canvas.Height, "#ED5197")

      canvas.Color("#9045D13B")
      canvas.Rectangle(0.5*canvas.Width, 0.5*canvas.Height, 0.8*canvas.Width, 0.8*canvas.Height)
      canvas.Color("#FFFFFF")
      canvas.Write(((0.8-0.5)/2 + 0.5) * canvas.Width,((0.8-0.5)/2 + 0.5)*canvas.Height, "#9045D13B")

      canvas.Color("#ffffff")
      canvas.AlignBottom()
      canvas.Write(canvas.Width /2, canvas.Height - 80, "Using color")
      display.Display(canvas)

   return True

def Sprites(tc):
   display = tc.Instruments.ImageDisplay
   with tc.Image.GetCanvas(tc.Assets.Instructions.Background) as canvas:
      canvas.Font("Roboto")
      canvas.TextSize(48)
      canvas.Color("#ffffff")

      canvas.AlignCenter()
      canvas.AlignBottom()
      canvas.Sprite(canvas.Width /2, canvas.Height - 180, tc.Assets.Sprites.Left)

      canvas.Color("#ffffff")
      canvas.AlignBottom()
      canvas.Write(canvas.Width /2, canvas.Height - 80, "Add to existing image and drawing Sprites")
      display.Display(canvas)

   return True

def Text(tc):
   display = tc.Instruments.ImageDisplay
   with tc.Image.GetCanvas(display) as canvas:
      x1 = (1.0/4.0) * canvas.Width
      x2 = (2.0/4.0) * canvas.Width
      x3 = (3.0/4.0) * canvas.Width
      y1 = (1.0/4.0) * canvas.Height
      y2 = (2.0/4.0) * canvas.Height
      y3 = (3.0/4.0) * canvas.Height

      canvas.Color("#545755")
      canvas.Line(x1, 0, x1, canvas.Height)
      canvas.Line(x2, 0, x2, canvas.Height)
      canvas.Line(x3, 0, x3, canvas.Height)
      canvas.Line(0, y1, canvas.Width, y1)
      canvas.Line(0, y2, canvas.Width, y2)
      canvas.Line(0, y3, canvas.Width, y3)

      canvas.Font("Roboto")
      canvas.TextSize(24)
      canvas.Color("#ffffff")
      
      canvas.AlignTop()
      canvas.AlignRight()
      canvas.Write(x1,y1,"AlignTop() + AlignRight()")
      canvas.AlignCenter()
      canvas.Write(x2,y1,"AlignTop() + AlignCenter()")
      canvas.AlignLeft()
      canvas.Write(x3,y1,"AlignTop() + AlignLeft()")

      canvas.AlignMiddle()
      canvas.AlignRight()
      canvas.Write(x1,y2,"AlignMiddle() + AlignRight()")
      canvas.AlignCenter()
      canvas.Write(x2,y2,"AlignMiddle() + AlignCenter()")
      canvas.AlignLeft()
      canvas.Write(x3,y2,"AlignMiddle() + AlignLeft()")

      canvas.AlignBottom()
      canvas.AlignRight()
      canvas.Write(x1,y3,"AlignBottom() + AlignRight()")
      canvas.AlignCenter()
      canvas.Write(x2,y3,"AlignBottom() + AlignCenter()")
      canvas.AlignLeft()
      canvas.Write(x3,y3,"AlignBottom() + AlignLeft()")

      canvas.TextSize(48)
      canvas.AlignCenter()
      canvas.AlignBottom()
      canvas.Write(canvas.Width /2, canvas.Height - 20, "Writing text")
      display.Display(canvas)

   return True

def PhysicalLengths(tc):
   display = tc.Instruments.ImageDisplay
   with tc.Image.GetCanvas(display) as canvas:
      metrics = display.Metrics
      length = metrics.LengthToPixels(10)

      canvas.Font("Roboto")
      canvas.TextSize(48)
      canvas.Color("#ffffff")
      canvas.AlignCenter()
      canvas.Fill(True)

      metrics = display.Metrics
      length = metrics.LengthToPixels(10)

      canvas.Color("#ffffff")      
      canvas.Rectangle(canvas.Width/2 - length/2, canvas.Height/2 - 20, canvas.Width/2 + length/2, canvas.Height/2 + 40)
      canvas.AlignTop()
      canvas.Write(canvas.Width/2, canvas.Height/2 + 60, "10cm")
      
      canvas.AlignBottom()
      canvas.Write(canvas.Width /2, canvas.Height - 20, "Drawing with physcial lengths")
      display.Display(canvas)

   return True

def VisualAngles(tc):
   display = tc.Instruments.ImageDisplay
   with tc.Image.GetCanvas(display) as canvas:
      metrics = display.Metrics
      length = metrics.LengthToPixels(10)

      canvas.Font("Roboto")
      canvas.TextSize(48)
      canvas.Color("#ffffff")
      canvas.AlignCenter()
      canvas.Fill(True)

      metrics = display.Metrics
      length = metrics.AngleToPixels(10)

      canvas.Color("#ffffff")      
      canvas.Rectangle(canvas.Width/2 - length/2, canvas.Height/2 - 20, canvas.Width/2 + length/2, canvas.Height/2 + 40)
      canvas.AlignTop()
      canvas.Write(canvas.Width/2, canvas.Height/2 + 60, "10°")
      
      canvas.AlignBottom()
      canvas.Write(canvas.Width /2, canvas.Height - 20, "Drawing with visual angles")
      display.Display(canvas)

   return True
