from tkinter import *
from tkinter.ttk import *

# Initialize the main application window
root = Tk()
root.title("Tower of Hanoi")

# Create the canvas for the game
canvas = Canvas(root, width=800, height=400, bg="white")
canvas.pack()

# Define variables to hold towers and rings
towers = []
rings = []
ring_stacks = [[], [], []]  # Track rings on each tower (index: tower number)

# Define the ring class
class DraggableRing:
    def __init__(self, canvas, x, y, height, width, color="blue"):
        self.canvas = canvas
        self.height = height
        self.width = width
        self.color = color
        self.item = self.create_ring(x, y)
        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.drag)
        self.canvas.tag_bind(self.item, "<ButtonRelease-1>", self.snap_to_tower)
        self.current_tower = 0  # Track which tower the ring is on

    def create_ring(self, x, y):
        return self.canvas.create_rectangle(x, y, x + self.width, y + self.height, fill=self.color, outline="black")

    def start_drag(self, event):
        # Ensure only the top ring of a tower is draggable
        if self.item not in ring_stacks[self.current_tower] or ring_stacks[self.current_tower][-1] != self.item:
            return
        self.offset_x = event.x - self.canvas.coords(self.item)[0]
        self.offset_y = event.y - self.canvas.coords(self.item)[1]
        self.dragging = True

    def drag(self, event):
        if not getattr(self, 'dragging', False):
            return
        # Move the ring while dragging
        self.canvas.coords(self.item, event.x - self.offset_x, event.y - self.offset_y,
                            event.x - self.offset_x + self.width, event.y - self.offset_y + self.height)

    def snap_to_tower(self, event):
        if not getattr(self, 'dragging', False):
            return
        self.dragging = False
        closest_tower = None
        min_distance = float('inf')

        # Find the closest tower
        for idx, tower in enumerate(towers):
            tower_coords = self.canvas.coords(tower)
            tower_center_x = (tower_coords[0] + tower_coords[2]) / 2
            distance = abs(event.x - tower_center_x)
            if distance < min_distance:
                min_distance = distance
                closest_tower = idx

        if closest_tower is not None:
            # Validate the move (only allow smaller rings on larger ones)
            if (not ring_stacks[closest_tower] or
                    self.width < self.canvas.coords(ring_stacks[closest_tower][-1])[2] - self.canvas.coords(ring_stacks[closest_tower][-1])[0]):

                # Place the ring on the new tower
                tower_coords = self.canvas.coords(towers[closest_tower])
                tower_center_x = (tower_coords[0] + tower_coords[2]) / 2
                new_y = 400 - (len(ring_stacks[closest_tower]) + 1) * self.height
                self.canvas.coords(self.item, tower_center_x - self.width / 2, new_y,
                                    tower_center_x + self.width / 2, new_y + self.height)

                # Update the stacks
                ring_stacks[self.current_tower].remove(self.item)
                ring_stacks[closest_tower].append(self.item)
                self.current_tower = closest_tower
            else:
                # Reset ring position if the move is invalid
                self.reset_position()

    def reset_position(self):
        tower_coords = self.canvas.coords(towers[self.current_tower])
        tower_center_x = (tower_coords[0] + tower_coords[2]) / 2
        new_y = 400 - len(ring_stacks[self.current_tower]) * self.height
        self.canvas.coords(self.item, tower_center_x - self.width / 2, new_y,
                            tower_center_x + self.width / 2, new_y + self.height)

# Function to create towers and initial rings
def initialize_game(num_towers=3, num_rings=5):
    global towers, rings, ring_stacks

    # Clear existing items
    canvas.delete("all")
    towers.clear()
    rings.clear()
    ring_stacks = [[] for _ in range(num_towers)]

    # Create towers
    tower_width = 15
    canvas_width = int(canvas['width'])
    spacing = canvas_width // (num_towers + 1)
    for i in range(num_towers):
        x = (i + 1) * spacing - tower_width / 2
        tower = canvas.create_rectangle(x, 400, x + tower_width, 200, fill="gray", outline="black")
        towers.append(tower)

    # Create rings
    ring_height = 20
    ring_width_step = 20
    ring_width_base = 100
    for i in range(num_rings):
        width = ring_width_base + (num_rings - i - 1) * ring_width_step
        x = spacing - width / 2
        y = 400 - (i + 1) * ring_height
        colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
        ring = DraggableRing(canvas, x, y, ring_height, width, color=colors[i % len(colors)])
        rings.append(ring)
        ring_stacks[0].append(ring.item)  # Place rings on the first tower

# Initialize the game
initialize_game()

root.mainloop()
