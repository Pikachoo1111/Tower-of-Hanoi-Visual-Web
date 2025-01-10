from tkinter import *
from tkinter.ttk import *

root = Tk()
root.title("Draggable Shapes")
# create three ovals
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
        if (self.x + dx < 0 or self.x + dx + self.width > 700) or (self.y + dy < 0 or self.y + dy + self.height > 400):
            dx = 0
            dy = 0
        self.canvas.move(self.item, dx, dy)
        self.x = event.x
        self.y = event.y

def getNumTowersSliderValue():
    return int(round(numTower.get()))
def getNumRingsSliderValue():
    return int(round(numRings.get()))
def setNumTowers(*args):
    numTowers = getNumTowersSliderValue()
    # print(numTowers, type(numTowers))
    # Clear existing towers
    for tower in towers:
        canvas.delete(tower)
    towers.clear()

    # Create new towers based on the slider value
    tower_width = 15
    spacing = (700 - numTowers * tower_width) / (numTowers + 1)
    for i in range(numTowers):
        x = spacing + i * (tower_width + spacing)
        tower = canvas.create_rectangle(x, 400, x + tower_width, 200, fill="gray", outline="gray")
        towers.append(tower)
def setNumRings(*args):

    numRings = getNumRingsSliderValue()
    print(len(rings))
    # Clear existing rings
    for ring in rings:
        canvas.delete(ring.item)
    rings.clear()

    # Create new rings based on the slider value
    ring_height = 15
    ring_width = 50
    ring_spacing = 10
    for i in range(numRings):
        x = 175
        y = 400 - (i + 1) * (ring_height + ring_spacing)
        tower_coords = canvas.coords(towers[0])  # Get the coordinates of the first tower
        x = (tower_coords[0] + tower_coords[2]) / 2  # Calculate the center x of the first tower
        ring_width = 70 + i * (100 / (numRings - 1))  # Calculate ring width dynamically
        ring = DraggableShape(canvas, x - (ring_width / 2), y, ring_height, ring_width, "rectangle", "red")
        ring_spacing = 0
        rings.append(ring)
# def resetAll()
# create a control panel on the left hand side to allow the user to change how many rings and how many towers there are
# two sliders for the number of towers and the number of rings with on update function
numTower = Scale(root, from_=3, to=5, orient=VERTICAL, command=setNumTowers)
numTower.place(x=715, y=50)

numRings = Scale(root, from_=5, to=10, orient=VERTICAL, command=setNumRings)
numRings.place(x=765, y=50)

# create vertical line to separate command panel from main window, at x=700 going all the way up the screen
canvas.create_line(700, 0, 700, 800)

# Create towers that are non-draggable at bottom of the screen (175, windowHeight)
towers.append(canvas.create_rectangle(175, 400, 190, 400-200, fill="gray", outline="gray"))
towers.append(canvas.create_rectangle(175*2, 400, 190+175, 400-200, fill="gray", outline="gray"))
towers.append(canvas.create_rectangle(175*3, 400, 190+175*2, 400-200, fill="gray", outline="gray"))

#pack all of the towers

# create ring shaped things, using rectangles
shape1 = DraggableShape(canvas, 70, 100, 20, 35, "rectangle", "red")
shape2 = DraggableShape(canvas, 85, 100, 20, 42.5, "rectangle", "orange")
shape3 = DraggableShape(canvas, 100, 100, 20, 50, "rectangle", "yellow")
shape4 = DraggableShape(canvas, 115, 100, 20, 57.5, "rectangle", "green")
shape5 = DraggableShape(canvas, 130, 100, 20, 65, "rectangle", "blue")

def snap_to_tower(event):
    closest_tower = None
    min_distance = float('inf')
    for tower in towers:
        tower_coords = canvas.coords(tower)
        tower_center_x = (tower_coords[0] + tower_coords[2]) / 2
        distance = abs(event.x - tower_center_x)
        if distance < min_distance:
            min_distance = distance
            closest_tower = tower

    if closest_tower:
        tower_coords = canvas.coords(closest_tower)
        tower_center_x = (tower_coords[0] + tower_coords[2]) / 2
        shape = event.widget.find_withtag("current")[0]
        shape_coords = canvas.coords(shape)
        shape_width = shape_coords[2] - shape_coords[0]
        shape_height = shape_coords[3] - shape_coords[1]
        canvas.coords(shape, tower_center_x - shape_width / 2, shape_coords[1], 
                      tower_center_x + shape_width / 2, shape_coords[3])

# Bind the snap_to_tower function to the release event of the draggable shapes

def snap_to_ring(event):
    shape = event.widget.find_withtag("current")[0]
    shape_coords = canvas.coords(shape)
    shape_width = shape_coords[2] - shape_coords[0]
    shape_height = shape_coords[3] - shape_coords[1]

    closest_tower = None
    min_distance = float('inf')
    for tower in towers:
        tower_coords = canvas.coords(tower)
        tower_center_x = (tower_coords[0] + tower_coords[2]) / 2
        distance = abs(event.x - tower_center_x)
        if distance < min_distance:
            min_distance = distance
            closest_tower = tower

    if closest_tower:
        tower_coords = canvas.coords(closest_tower)
        tower_center_x = (tower_coords[0] + tower_coords[2]) / 2

        # Find the topmost ring on the closest tower
        topmost_y = 400
        for ring in rings:
            ring_coords = canvas.coords(ring)
            if ring_coords[0] == tower_coords[0] and ring_coords[2] == tower_coords[2]:
                if ring_coords[1] < topmost_y:
                    topmost_y = ring_coords[1]

        new_y = topmost_y - shape_height - 10  # 10 is the spacing between rings
        if new_y < 200:  # Ensure the ring doesn't go above the tower
            new_y = 200

        canvas.coords(shape, tower_center_x - shape_width / 2, new_y, 
                      tower_center_x + shape_width / 2, new_y + shape_height)
        # Update the ring's position in the rings list
        for i, ring in enumerate(rings):
            if ring == shape:
                rings[i] = shape
                break

# Bind the snap_to_ring function to the release event of the draggable shapes

for element in rings:
    canvas.tag_bind(element.item, "<ButtonRelease-1>", snap_to_ring)
    canvas.tag_bind(element.item, "<ButtonRelease-1>", snap_to_tower)
canvas.tag_bind(shape1.item, "<ButtonRelease-1>", snap_to_ring)
canvas.tag_bind(shape2.item, "<ButtonRelease-1>", snap_to_ring)
canvas.tag_bind(shape3.item, "<ButtonRelease-1>", snap_to_ring)
canvas.tag_bind(shape4.item, "<ButtonRelease-1>", snap_to_ring)
canvas.tag_bind(shape5.item, "<ButtonRelease-1>", snap_to_ring)
canvas.tag_bind(shape1.item, "<ButtonRelease-1>", snap_to_tower)
canvas.tag_bind(shape2.item, "<ButtonRelease-1>", snap_to_tower)
canvas.tag_bind(shape3.item, "<ButtonRelease-1>", snap_to_tower)
canvas.tag_bind(shape4.item, "<ButtonRelease-1>", snap_to_tower)
canvas.tag_bind(shape5.item, "<ButtonRelease-1>", snap_to_tower)

root.mainloop()