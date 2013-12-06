#!/usr/bin/env python

# Requires pil library
# Which is not available yet for python 3

import Image, ImageDraw, ImageEnhance


class PunchcardReader():

    def __init__(self, filename, debug = False):
        self.debug = debug
        im = Image.open(filename)
        self.xmax = 100
        self.ymax = 100
        self.radius = 5
        self.threshold = 10
        self.out = im.transform((self.xmax,self.ymax), Image.EXTENT, (400,700,1800,1400))

    def get_area(self, x, y, radius):
        black = 0
        for rx in range(x-self.radius, x+self.radius):
            for ry in range(y-self.radius, y+self.radius):
                if self.out.getpixel((rx,ry)) == 0:
                    black += 1

        verdict = "black" if black > self. threshold else "white"

        print("%s/%s : %s\n" %(str(x), str(y), verdict))
        pass

    def get_values(self, xlines, ylines):
        """
        @param xlines: x values of vertical lines where punches should be
        @param ylines: y values of horizontal lines where punches should be
        """
        enhancer = ImageEnhance.Brightness(self.out)
        self.out = enhancer.enhance(2)
        if not self.debug:
            self.out = self.out.convert("1")
            for y in ylines:
                for x in xlines:
                    self.get_area(x,y,self.radius)
        else:
            for y in ylines:
                for x in xlines:
                    draw = ImageDraw.Draw(self.out)
                    draw.rectangle(((x-self.radius,y-self.radius), (x+self.radius,y+self.radius)), outline=(255,0,0))

    def display(self):
        self.out.show()

if __name__ == "__main__":
    p = PunchcardReader("../data/image.jpg", False)
    p.get_values([5,20,30,45,55,68,80,90],[10,50,90])
    p.display()
