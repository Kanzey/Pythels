from Tkinter import *
from PIL import Image, ImageOps, ImageTk

class GUI:
    def __init__(self, master, imgWidth, imgHeight):
        self.master, self.imgWidth, self.imgHeight = master, imgWidth, imgHeight
        fWidth, fHeight = 10* imgWidth, 10* imgHeight
        frame = Frame(master, width=fWidth, height=fHeight)
        frame.pack()
        self.btn=[[0 for x in xrange(imgHeight)] for x in xrange(imgWidth)] 
        for x in range(self.imgWidth):
            for y in range(self.imgHeight):
                f = Frame(frame, width=10, height=10)
                f.grid(column=x, row=y)
                f.pack_propagate(0)
                self.btn[x][y] = Button(f, bg="white")
                self.btn[x][y].pack()
        self.loadImage(self.btn, "test2.jpg")
                
    def loadImage(self, target, imageName):   
        img = Image.open(imageName)
        tmp = ImageOps.fit(img,(self.imgWidth, self.imgHeight), Image.ANTIALIAS)
        gray = tmp.convert('L')
        bw = gray.point(lambda x: 0 if x<128 else 255, '1')
        for x in xrange(self.imgWidth):
            for y in xrange(self.imgHeight):
                if bw.getpixel((x,y)) == 0:
                    target[x][y].config(bg="black")
                else:
                    target[x][y].config(bg="white")

root = Tk()
my_gui = GUI(root, 50, 50)
root.mainloop()
