from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import uuid

class Imagize(object):
    font = "resources/HelveticaNeue-Light.ttf"
    font_size = 24
    image_height = 150
    image_width = 600
    color = "#000"
    bgcolor = "#FFF"
    left_padding = 6
    right_padding = 6
    width = 600

    def __init__(self):
        pass

    def generate(self, text):
        replacement_character = u'\uFFFD'
        newline_replacement_string = ' ' + replacement_character + ' '

        # prepare linkback
        linkback = "generated via @ReplyXL"
        fontlinkback = ImageFont.truetype(self.font, int(float(self.font_size) / 1.1))
        linkbackx = fontlinkback.getsize(linkback)[0]
        linkback_height = fontlinkback.getsize(linkback)[1]
        # end of linkback

        font = ImageFont.truetype(self.font, self.font_size)
        text = text.replace('\n', newline_replacement_string)

        lines = []
        line = u""

        for word in text.split():
            if word == replacement_character: # give a blank line
                lines.append( line[1:] ) # slice the white space in the beginning of the line
                line = u""
                lines.append( u"" ) # the blank line
            elif font.getsize(line + ' ' + word)[0] <= (self.width - self.right_padding - self.left_padding):
                line += ' ' + word
            else: # start a new line
                lines.append( line[1:] ) # slice the white space at the beginning of the line
                line = u""
                line += ' ' + word # for now, assume no word alone can exceed the line width

        if len(line) != 0:
            lines.append( line[1:] ) # add the last line

        line_height = font.getsize(text)[1]
        img_height = int(line_height * (len(lines) + 1.2))

        img = Image.new("RGBA", (self.width, img_height), self.bgcolor)
        draw = ImageDraw.Draw(img)

        y_coord_line_start = 0
        for line in lines:
            draw.text( (self.left_padding, y_coord_line_start), line, self.color, font=font)
            y_coord_line_start += line_height

        # add linkback at the bottom
        draw.text( (self.width - linkbackx, img_height - linkback_height), linkback, self.color, font=fontlinkback)

        img = img.resize((int(float(self.width)/1.02), int(float(img_height)/1.02)), Image.ANTIALIAS)

        filename = "static/" + str(uuid.uuid4()) + ".png"
        img.save(filename, 'PNG', quality=100)
        return filename