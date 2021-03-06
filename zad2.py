from Tkinter import *
import tkFileDialog
from PIL import Image, ImageOps, ImageTk
from multiprocessing.dummy import Pool as ThreadPool
import time
import random


class PixelImage(Canvas):
    def createPixels(self, xCellNum, yCellNum, cellSize):     
        self.xCellNum = xCellNum
        self.yCellNum = yCellNum
        self.cellSize = cellSize

        self.pixelRects = [[0 for x in xrange(xCellNum)] for x in xrange(yCellNum)]
        self.pixelValues =  [[0 for x in xrange(xCellNum)] for x in xrange(yCellNum)]
        self.clear()

    def clear(self, color=None):
        if color == None:
            color = "white"
        self.delete(ALL)
        for x in xrange(self.xCellNum):
            for y in xrange(self.yCellNum):
                cords = [i*self.cellSize for i in [x,y,(x+1),(y+1)]]
                self.pixelRects[x][y] = self.create_rectangle(
                    cords, fill=color, outline=color)
                self.pixelValues[x][y] = 0

##    def mt_clear(self):
##        self.delete(ALL)
##        pool = ThreadPool(4)
##        pool.map(self.clear_line, range(self.xCellNum))
##        pool.close() 
##        pool.join() 
##        
##    def clear_line(self, x):
##        for y in xrange(self.yCellNum):
##            cords = [i*self.cellSize for i in [x,y,(x+1),(y+1)]]
##            self.pixelRects[x][y] = self.create_rectangle(
##                cords, fill="white", outline="white")
##            self.pixelValues[x][y] = 0
                
    def loadImage(self, step, doReload=None):
        if doReload == None:
            doReload = False
        if doReload == False:
            file_path = tkFileDialog.askopenfilename()
            img = Image.open(file_path)
            tmp = ImageOps.fit(img,(self.xCellNum, self.yCellNum), Image.ANTIALIAS)
            self.gray = tmp.convert('L')
        bw = self.gray.point(lambda x: 0 if x<step else 255, '1').load()
        start = time.time()
        for x in xrange(self.xCellNum):
            for y in xrange(self.yCellNum):
                cords = [i*self.cellSize for i in [x,y,(x+1),(y+1)]]
                if bw[x,y] == 0:
                    self.pixelRects[x][y] = self.create_rectangle(
                        cords, fill="black", outline="gray")
                    self.pixelValues[x][y] = 1
                else:
                    self.pixelRects[x][y] = self.create_rectangle(
                        cords, fill="white", outline="white")
                    self.pixelValues[x][y] = 0
        print("Generating pixels",time.time()-start)    
                    
##    def mt_loadImage(self):
##        file_path = tkFileDialog.askopenfilename()
##        img = Image.open(file_path)
##        tmp = ImageOps.fit(img,(self.xCellNum, self.yCellNum), Image.ANTIALIAS)
##        gray = tmp.convert('L')
##        self.bw = gray.point(lambda x: 0 if x<128 else 255, '1').load()
##        
##        start = time.time()
##        pool = ThreadPool(4)
##        pool.map(self.loadImageline, range(self.xCellNum))
##        pool.close() 
##        pool.join()
##        print("Generating pixels",time.time()-start)
##
##    def loadImageline(self,x):
##        for y in xrange(self.yCellNum):
##            cords = [i*self.cellSize for i in [x,y,(x+1),(y+1)]]
##            if self.bw[x,y] == 0:
##                self.pixelRects[x][y] = self.create_rectangle(
##                    cords, fill="black", outline="gray")
##                self.pixelValues[x][y] = 1
##            else:
##                self.pixelRects[x][y] = self.create_rectangle(
##                    cords, fill="white", outline="white")
##                self.pixelValues[x][y] = 0
      
                    
    def changePixel(self,x,y,color, outlineColor, value):
        self.itemconfig(self.pixelRects[x][y], fill=color, outline=outlineColor)
        self.pixelValues[x][y]=value;
        
    def changePixels(self, number):
        rands = random.sample(range(1, self.xCellNum*self.yCellNum), number)
##        for i in rands:
##            x = i%self.xCellNum
##            y = i/self.xCellNum
##            self.itemconfig(self.pixelRects[x][y], fill="gray")
        for i in rands:
            x = i%self.xCellNum
            y = i/self.xCellNum
            if self.pixelValues[x][y] == 0:
                self.itemconfig(self.pixelRects[x][y], fill="black", outline="gray")
                self.pixelValues[x][y] = 1;
            else:
                self.itemconfig(self.pixelRects[x][y], fill="white", outline="white")
                self.pixelValues[x][y] = 0;
    def onclick(self,event):
        self.reversePixel(event.x/10,event.y/10)

    def reversePixel(self, x,y):
        if self.pixelValues[x][y] == 0:
            self.itemconfig(self.pixelRects[x][y], fill="black", outline="gray")
            self.pixelValues[x][y] = 1;
        else:
            self.itemconfig(self.pixelRects[x][y], fill="white", outline="white")
            self.pixelValues[x][y] = 0;
        

class GUI:
    def __init__(self, master, imgWidth, imgHeight):
        self.master, self.imgWidth, self.imgHeight = master, imgWidth, imgHeight
        fWidth, fHeight = 10* imgWidth, 10* imgHeight
        
        frame = Frame(master, width=fWidth, height=fHeight)
        frame.pack(side="left")
        self.inCanvas = PixelImage(frame, width=fWidth, height=fHeight)
        self.inCanvas.bind("<Button-1>", self.inCanvas.onclick)
        self.inCanvas.pack()
        self.inCanvas.createPixels(imgWidth, imgHeight, 10)
        
        frame = Frame(master, width=fWidth, height=fHeight)
        frame.pack(side="right")
        self.outCanvas = PixelImage(frame, width=fWidth, height=fHeight)
        self.outCanvas.pack()
        self.outCanvas.createPixels(imgWidth, imgHeight, 10)

        
        btn = Button(master, text="load", command= lambda: self.loadImage())
        btn.pack()
        e= Entry(master)
        e.pack()
        e.insert(0,'300')
        btn = Button(master, text="Add noise", command= lambda: self.inCanvas.changePixels(int(e.get())))
        btn.pack()
        self.w = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.w.set(128)
        btn = Button(master, text="reload", command= self.reloadImage)
        btn.pack(side="bottom")
        self.w.pack(side="bottom")
        self.isBusy = False
        self.wasImageLoaded = False

        

        #def createButtonDisplay(self, parent, width, height):
    def reloadImage(self):
        if self.isBusy == False and self.wasImageLoaded:
            self.isBusy = True
            self.inCanvas.loadImage(self.w.get(), doReload = True)
            self.isBusy = False
        
    def loadImage(self):
        self.wasImageLoaded = True
        self.inCanvas.loadImage(self.w.get())



root = Tk()
my_gui = GUI(root, 50, 50)
root.mainloop()
