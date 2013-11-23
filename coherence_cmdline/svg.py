__author__ = 'Thorsten Sick'

import svgwrite


class Card():

    def __init__(self, size=("105cm","148cm")):
        self.size = size
        # Cards are 105 x 148

        svg_document = svgwrite.Drawing(filename = "test-svgwrite.svg",
                                        size = (size[0], size[1]))

        svg_document.add(svg_document.rect(insert = (0, 0),
                                           size = ("200px", "100px"),
                                           stroke_width = "1",
                                           stroke = "black",
                                           fill = "rgb(255,255,0)"))

        svg_document.add(svg_document.text("Hello World",
                                           insert = (210, 110)))

        print(svg_document.tostring())

        svg_document.save()
