import random
import simpy
import tkinter as tk
from Point import Point


class Display_Robot:
    def __init__(self, canvas, point, unit_size,  name):
        self.point = point
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.robot = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red", tags=name)
        self.robot_id = canvas.create_text(((self.x2 - self  .x1) / 2 + self.x1),
                                          ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

    def move_robot(self, point):
        # print(f'Moving from {self.point.x, self.point.y} to: {point.x, point.y}')

        # Move Left
        if self.point.x > point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * unit_size, 0)
            # print(f'Move Left {(point.x - self.point.x) * unit_size} Units')

        # Move Right
        if self.point.x < point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * unit_size, 0)
             # print(f'Move Right {(point.x - self.point.x) * unit_size} Units')

        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * unit_size)
            # print(f'Move Up {(point.y - self.point.y) * unit_size} Units')

        # Move Down
        if self.point.x == point.x and self.point.y < point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * unit_size)
            # print(f'Move Down {(point.y - self.point.y) * unit_size} Units')

        self.canvas.update()

class Display_Shelf:
    def __init__(self, canvas, point, unit_size,  name):
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.robot = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="yellow", tags=name)
        self.robot_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                          ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

    def move_shelf(self, point):
        # print(f'Moving from {self.point.x, self.point.y} to: {point.x, point.y}')

        # Move Left
        if self.point.x > point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * unit_size, 0)
            # print(f'Move Left {(point.x - self.point.x) * unit_size} Units')

        # Move Right
        if self.point.x < point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * unit_size, 0)
            # print(f'Move Right {(point.x - self.point.x) * unit_size} Units')

        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * unit_size)
            # print(f'Move Up {(point.y - self.point.y) * unit_size} Units')

        # Move Down
        if self.point.x == point.x and self.point.y < point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * unit_size)
            # print(f'Move Down {(point.y - self.point.y) * unit_size} Units')

        self.canvas.update()


def checkered(canvas, line_distance):
    # Vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance, canvas_width, line_distance):
        canvas.create_line(x, 0, x, canvas_height, fill="#476042")

    # Horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance, canvas_height, line_distance):
        canvas.create_line(0, y, canvas_width, y, fill="#476042")

# Setup Canvas ------------------------------------------------------
master = tk.Tk()

HEIGHT = 600
WIDTH = 500

main_canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT)


lower_frame = tk.Frame(master, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

# ------ For Grid Canvas
canvas_width = 400
canvas_height = 400
unit_size = 40

canvas = tk.Canvas(lower_frame, width=canvas_width, height=canvas_height)

master.title("Amazon Warehouse")
canvas.pack()
main_canvas.pack()
# -------------------------------------------------------------------

shelf = Display_Shelf(canvas, Point(3, 3), unit_size, 'S1')

robot = Display_Robot(canvas, Point(1, 1), unit_size, 'P1')





checkered(canvas, unit_size)

master.mainloop()