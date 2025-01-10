for stack in ring_stacks:
            if self.item in stack and stack[-1] != self.item:
                return
        self.x, self.y = self.canvas.coords(self.item)[:2]
