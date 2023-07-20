import xml.etree.ElementTree as ET
import json
import struct
from array import array
from PIL import Image
import os


class PackWriter:
    def __init__(self, root=""):
        self.data = b''
        self.root = root
        self.cd = ""

    def writeSection(self, data):
        size = len(data)
        sizeBytes = struct.pack('H', size)
        self.data += sizeBytes + data
        print("\t", size, " bytes")

    def imgGSM(self, filePath):
        print("imgGSM", filePath)
        image = Image.open(self.root+self.cd+filePath).convert("RGBA")

        buf1 = bytearray()
        buf2 = bytearray()
        bufMask = bytearray()

        pixels = image.getdata()
        for y in range(0, image.height, 8):
            for x in range(image.width):
                value1 = 0
                value2 = 0
                valueMask = 0
                for j in range(7, -1, -1):
                    if y + j < image.height:
                        r, g, b, a = pixels[(y + j) * image.width + x]
                    else:
                        r, g, b, a = 0, 0, 0, 0
                    alpha = a >= 128
                    if alpha:
                        gray2Bit = round((r + g + b) / 256)
                    else:
                        gray2Bit = 0
                    value1 <<= 1
                    value2 <<= 1
                    valueMask <<= 1
                    if gray2Bit in (2, 3):
                        value1 |= 1
                    if gray2Bit in (1, 2):
                        value2 |= 1
                    if alpha:
                        valueMask |= 1
                buf1.append(value1)
                buf2.append(value2)
                bufMask.append(valueMask)
        self.writeSection(struct.pack(
            'HH', image.width, image.height) + buf1 + buf2 + bufMask)

    def imgGS(self, filePath):
        print("imgGS", filePath)
        image = Image.open(self.root+self.cd+filePath).convert("RGB")

        buf1 = bytearray()
        buf2 = bytearray()

        pixels = image.getdata()
        for y in range(0, image.height, 8):
            for x in range(image.width):
                value1 = 0
                value2 = 0
                for j in range(7, -1, -1):
                    if y + j < image.height:
                        r, g, b = pixels[(y + j) * image.width + x]
                    else:
                        r, g, b = 0, 0, 0
                    gray2Bit = round((r + g + b) / 256)
                    value1 <<= 1
                    value2 <<= 1
                    if gray2Bit in (2, 3):
                        value1 |= 1
                    if gray2Bit in (1, 2):
                        value2 |= 1
                buf1.append(value1)
                buf2.append(value2)
        self.writeSection(struct.pack(
            'HH', image.width, image.height) + buf1 + buf2)

    def save(self, filePath):
        with open(self.root+self.cd+filePath, 'wb') as file:
            file.write(self.data)
        print("Saved", filePath)


root = os.path.dirname(os.path.realpath(__file__)) + os.sep
pack = PackWriter(root)

pack.cd = "../ThoomArt/"
pack.imgGS("Title.png")
pack.imgGS("BG.png")

pack.cd = "../ThoomArt/wall/"
pack.imgGS("NormWall.png")
pack.imgGS("DoorWall.png")
pack.imgGS("IconWall.png")
pack.imgGS("IconWall2.png")
pack.imgGS("IconWallD.png")
pack.imgGS("IconWallB.png")
pack.imgGS("DangerWall.png")
pack.imgGS("HexoWall.png")
pack.imgGS("BrickWall.png")
pack.imgGS("SpecialWall.png")

pack.cd = "../ThoomArt/shotgun/"
pack.imgGSM("shotgun.png")
pack.imgGSM("shotgunIdle.png")
pack.imgGSM("shotgunBlast.png")
pack.imgGSM("shotgunReload.png")

pack.cd = "../ThoomArt/imp/"
pack.imgGSM("imp32.png")
pack.imgGSM("imp24.png")
pack.imgGSM("imp18.png")
pack.imgGSM("imp14.png")
pack.imgGSM("imp10.png")
pack.imgGSM("imp6.png")
pack.imgGSM("imp32B.png")
pack.imgGSM("imp24B.png")
pack.imgGSM("imp18B.png")
pack.imgGSM("imp14B.png")
pack.imgGSM("imp10B.png")
pack.imgGSM("imp32D.png")
pack.imgGSM("imp24D.png")
pack.imgGSM("imp18D.png")
pack.imgGSM("imp14D.png")

pack.cd = "../ThoomArt/demon/"
pack.imgGSM("demon32.png")
pack.imgGSM("demon24.png")
pack.imgGSM("demon18.png")
pack.imgGSM("demon14.png")
pack.imgGSM("demon10.png")
pack.imgGSM("demon6.png")
pack.imgGSM("demon32B.png")
pack.imgGSM("demon24B.png")
pack.imgGSM("demon18B.png")
pack.imgGSM("demon14B.png")
pack.imgGSM("demon10B.png")
pack.imgGSM("demon32D.png")
pack.imgGSM("demon24D.png")
pack.imgGSM("demon18D.png")
pack.imgGSM("demon14D.png")

pack.cd = "../ThoomArt/key/"
pack.imgGSM("key16.png")
pack.imgGSM("key12.png")
pack.imgGSM("key8.png")

pack.cd = "../ThoomArt/ui/"
pack.imgGSM("keyUI.png")
pack.imgGS("pressUI.png")

pack.cd = "../ThoomArt/fireball/"
pack.imgGSM("fireball.png")
pack.imgGSM("explosion.png")
pack.imgGSM("explosion2.png")

pack.cd = "../ThoomArt/guy/"
pack.imgGSM("guyLeft.png")
pack.imgGSM("guyRight.png")
pack.imgGSM("guyHurt.png")
pack.imgGSM("guyDie.png")

pack.cd = "../"
pack.save("Thoom.pack")
