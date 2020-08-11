import tkinter as tk

window = tk.Tk()
frame = tk.Frame()
frame.pack()

label = tk.Label(master=frame, text='test')
label.pack()
frame.pack()

window.mainloop()
