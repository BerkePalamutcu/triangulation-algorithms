import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
import numpy as np

# Python Implementation
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
class Region:
    def __init__(self, site, vertices):
        self.site = site
        self.vertices = vertices
 
class Event:
    def __init__(self, point, index, is_site):
        self.point = point
        self.index = index
        self.is_site = is_site
 
    # Custom comparison for event sorting
    def compare_to(self, other):
        if self.point.x == other.point.x:
            return -1 if self.is_site else 1
        return self.point.x - other.point.x
 
def voronoi_sweep_line(points):
    n = len(points)
    regions = [Region(Point(0, 0), []) for _ in range(n)]
 
    # Sort points by their x-coordinates
    points.sort(key=lambda p: (p.x, p.y))
 
    event_queue = set()
 
    # Initialize the event queue with the input points
    for i, point in enumerate(points):
        event_queue.add(Event(point, i, True))
 
    while event_queue:
        # Extract the minimum event from the event queue
        current_event = min(event_queue, key=lambda e: (e.point.x, not e.is_site))
         
        event_queue.remove(current_event)
 
        if current_event.is_site:
            # Handle site event
            pass
        else:
            # Handle circle event
            # Update Voronoi regions as the sweep line encounters circle events
            pass
 
    return regions
 
 
# Sample input points
points = [
    Point(2, 5),
    Point(4, 5),
    Point(7, 2),
    Point(5, 7)
]
 
# Construct Voronoi Diagram
voronoi_regions = voronoi_sweep_line(points)
 
# Display Voronoi regions
for i, region in enumerate(voronoi_regions):
    print(f"Voronoi Region #{i + 1}: Site ({region.site.x}, {region.site.y})")
    for vertex in region.vertices:
        print(f"Vertex ({vertex.x}, {vertex.y})")
    print()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VoronoiApp:
    def __init__(self, master):
        self.master = master
        master.title("Voronoi Diagram Visualizer")

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.draw_button = tk.Button(master, text="Draw Voronoi", command=self.draw_voronoi)
        self.draw_button.pack()

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

        self.points = []
        self.canvas.bind("<Button-1>", self.add_point)
        self.matplotlib_canvas_widget = None

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.draw_point(x, y)

    def draw_point(self, x, y):
        r = 3
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='red')

    def draw_voronoi(self):
        # Clear previous Matplotlib widget
        if self.matplotlib_canvas_widget:
            self.matplotlib_canvas_widget.destroy()

        # Calculate and draw Voronoi diagram
        if len(self.points) > 2:
            points_array = np.array([[p.x, p.y] for p in self.points])
            vor = Voronoi(points_array)

            # Create a new matplotlib figure and axis
            fig, ax = plt.subplots()

            # Manually plot Voronoi diagram
            ax.plot(points_array[:, 0], points_array[:, 1], 'ro')
            for simplex in vor.ridge_vertices:
                simplex = np.asarray(simplex)
                if np.all(simplex >= 0):
                    ax.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1], 'k-')

            # Setting plot limits
            ax.set_xlim([0, 400])
            ax.set_ylim([0, 400])

            # Embed matplotlib plot in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.master)
            self.matplotlib_canvas_widget = canvas.get_tk_widget()
            self.matplotlib_canvas_widget.pack()
            canvas.draw()

    def clear_canvas(self):
        # Clear the Tkinter canvas, Matplotlib widget, and reset points
        self.canvas.delete("all")
        if self.matplotlib_canvas_widget:
            self.matplotlib_canvas_widget.destroy()
            self.matplotlib_canvas_widget = None
        self.points.clear()

# Create and run the application
root = tk.Tk()
app = VoronoiApp(root)
root.mainloop()
