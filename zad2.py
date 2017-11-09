from Tkinter import *
from PIL import Image, ImageOps, ImageTk

class GUI:
    def __init__(self, master):
        self.master = master
        basewidth = 50
        img = Image.open('test2.jpg')
        tmp = ImageOps.fit(img,(basewidth,basewidth), Image.ANTIALIAS)
        gray = tmp.convert('L')
        bw = gray.point(lambda x: 0 if x<128 else 255, '1')
        frame = Frame(master, width=500, height=500)
        frame.pack()
        for i in range(50):
            for k in range(50):
                f = Frame(frame, width=10, height=10)
                f.grid(column=i, row=k)
                f.pack_propagate(0)
                if bw.getpixel((i,k)) == 0:
                    btn = Button(f, bg="black")
                else:
                    btn = Button(f, bg="white")
                btn.pack()

                

root = Tk()
my_gui = GUI(root)
root.mainloop()
