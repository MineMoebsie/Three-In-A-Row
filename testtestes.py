from tkinter import *

tk = Tk()

global polygon_lijst
global polygon_object

def polygon_toevoegen(event,polygon_lijst,polygon_object):
   polygon_lijst.append([event.x,event.y])
   polygon_object = canvas.create_polygon(polygon_lijst,fill="",outline="black")
   canvas.delete(polygon_object-1)

canvas = Canvas(width=500,height=500)
canvas.bind("<Button-1>", lambda event: polygon_toevoegen(event,polygon_lijst,polygon_object))
canvas.pack()

polygon_lijst = []
polygon_object = canvas.create_polygon(0,0,1000,1000,fill="",outline="black")
canvas.delete(polygon_object)
tk.mainloop()
