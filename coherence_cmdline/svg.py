__author__ = 'Thorsten Sick'

import svgwrite


class Card():

    def __init__(self, offset=(0,0), size=(105,148), lines = 8, punchbox=((0,75),(100,140))):
        """ A Punchcard

        @param offset: Offset onsheet. That way I can print several cards on one sheet. Maybe later laser cut them
        @param size: Size of the card itself. in mm
        @param lines: Number of lines of holes. Each one will be 8 holes wide. That is 8 Bytes total for 8 lines
        @param punchbox: Coordinates for the box that contains the punch holes. In mm
        """
        self.size = size
        self.offset = offset
        self.lines = lines
        self.punchbox = punchbox
        self.svg_document = None

    def draw_hole(self, center = (0,0), radius="2mm"):
        """ Draw a hole at the center point (in cm)

        @param center: center position in mm
        @param radius: Radius of the hole
        """

        px1 = str(center[0]) + "mm"
        py1 = str(center[1]) + "mm"
        self.svg_document.add(self.svg_document.circle(center = (px1, py1),
                                           r = radius,
                                           stroke_width = "1",
                                           stroke = "black",
                                           #fill = "rgb(255,255,0)"
                                        )
                                        )

    def draw_punch_line(self, number, holes=0, radius = "2mm"):
        """ Draws a line of holes

        @param number: Number of the line. 8 lines, 0-7
        @param holes: id that should be printed. Max. 255
        """

        if (holes>255) or (holes < 0):
            #error
            return

        hstr = bin(holes)[2:]
        hstr = "0"*(8-len(hstr))+hstr
        print (hstr)

        vsize = self.punchbox[1][1] - self.punchbox[0][1]
        hsize = self.punchbox[1][0] - self.punchbox[0][0]
        vdist = vsize / 9
        hdist = hsize / 9
        y = self.punchbox[0][1] + self.offset[1] + vdist * (number + 1)
        for i in range (0,8):
            x = self.punchbox[0][0] + self.offset[0] + hdist * (i + 1)
            if hstr[i] == "1":
                self.draw_hole((x,y), radius)

    def print_text(self, text, pos, pixel="12px", font="Arial"):
        self.svg_document.add(self.svg_document.text(text,
                                           insert = (pos[0], pos[1]),
                                           style = "font-size:%s; font-family:%s"%(pixel, font)))

    def print_heading(self, text, pixel="20px", font="1942 report"):
        """ Print Heading

        """
        self.print_text(text, ("5mm","10mm"), pixel, font)


    def print_playlist(self, text, pixel="12px", font = "1942 report"):
        """ A list of strings printed at the left side of the card

        @param text: A list of strings. each item is a line.
        """
        y = 15
        offset = 3
        for line in text:
            self.print_text(line, ("10mm", str(y) + "mm"), pixel=pixel, font = font)
            y += offset


    def generate(self, card):
        self.svg_document = svgwrite.Drawing(filename = card["filename"],
                                        size = (str(self.size[0])+"mm", str(self.size[1])+"mm"))

        # Draw punchbox
        px1 = str(self.offset[0] + self.punchbox[0][0]) + "mm"
        py1 = str(self.offset[1] + self.punchbox[0][1]) + "mm"
        pxsize = str(self.punchbox[1][0] - self.punchbox[0][0]) + "mm"
        pysize = str(self.punchbox[1][1] - self.punchbox[0][1]) + "mm"

        # Draw first hole

        line = 0
        for i in card["ids"]:
            self.draw_punch_line(line,i)
            line += 1

        self.print_heading("%s  %s  %s" % (card["genre"], card["artist"], card["album"]))
        self.print_playlist(card["songs"])

        print(self.svg_document.tostring())

        self.svg_document.save()


card = { "album":"S&M",
         "artist":"Metallica",
         "genre": "Metal",
         "songs":["Enter Sandman","Nothing Else Matters", "Call of Kthulhu"],
         "ids":[255,2,3,4,5,6,7,8],
         "filename": "test-svgwrite.svg"
}

c = Card()
c.generate(card)