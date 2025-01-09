from tkinter import *
from tkinter.ttk import *

root = Tk()
root.title("Draggable Shapes")
#create three ovals
canvas = Canvas(root, width=800, height=400)
canvas.pack()
wheight = root.winfo_height()
wwidth = root.winfo_width()

towers = []
rings = []

class DraggableShape:
    def __init__(self, canvas, x, y, height, width, shape_type="oval", color="blue"):
        self.canvas = canvas
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.item = self.create_shape()
        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.drag)

    def create_shape(self):
        if self.shape_type == "oval":
            return self.canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color)
        elif self.shape_type == "rectangle":
            return self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        # check if object is off canvas based on its width and height
        if (self.x + dx < 0 or self.x + dx > 700) or (self.width + dy < 0 or self.y + dy > 400):
            dx = 0
            dy = 0
        self.canvas.move(self.item, dx, dy)
        self.x = event.x
        self.y = event.y



# create a control panel on the left hand side to allow the user to change how many rings and how many towers there are
#two sliders for the number of towers and the number of rings
numTower = Scale(root, from_=3, to=5, orient=VERTICAL)
numTower.pack()
numTower.place(x=715, y=50)
#move the sliders to the side of the window

numRings = Scale(root, from_=3, to=10, orient=VERTICAL)
numRings.pack()
numRings.place(x=765, y=50)

#create vertical line to seperate command pannel from main window, at x=700 going all the way up the screen
canvas.create_line(700, 0, 700, 800)
#two buttons for reset and solve
#two labels for the number of towers and the number of rings
#two entry boxes for the number of towers and the number of rings
#method for accessing slider values
# def getValues():

# create ring shaped things, using two semicircles attached to rectangles
shape1 = DraggableShape(canvas, 70, 100, 20,35, "rectangle", "red")
shape2 = DraggableShape(canvas, 85, 100, 20,42.5, "rectangle", "orange")
shape3 = DraggableShape(canvas, 100, 100, 20,50, "rectangle", "yellow")
shape4 = DraggableShape(canvas, 115, 100, 20,57.5, "rectangle", "green")
shape5 = DraggableShape(canvas, 130, 100, 20,65, "rectangle", "blue")

#Create towers that are non draggable at bottom of the screen (175, windowHeight)
towers.append(canvas.create_rectangle(175, 400, 190, 400-200, fill="gray", outline="gray"))
towers.append(canvas.create_rectangle(175*2, 400, 190+175, 400-200, fill="gray", outline="gray"))
towers.append(canvas.create_rectangle(175*3, 400, 190+175*2, 400-200, fill="gray", outline="gray"))

def setNumTowers(numTowers):
    for i in range(numTowers):
        towers.append(canvas.create_rectangle(175*(i+1), 400, 190+175*i, 400-200, fill="gray", outline="gray"))

root.mainloop()
