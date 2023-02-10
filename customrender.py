import time
import thumbyGrayscale as thumby
import math

# Defines starting position and direction
SW = 72
SH = 40


class DisplayExtra:
    def __init__(self):
        0


@micropython.viper
def drawBg(bmp, width: int, offset: int):
    sprtptr = ptr8(bmp[0])
    sprtptr2 = ptr8(bmp[1])
    ptr = ptr8(thumby.display.buffer)
    ptr2 = ptr8(thumby.display.shading)
    screenWidth = int(SW)
    height = int(SH) >> 3
    for i in range(screenWidth):
        n = (i+offset) % width
        for j in range(height):
            ptr[j * screenWidth + i] = sprtptr[j * width + n]
            ptr2[j * screenWidth + i] = sprtptr2[j * width + n]


@micropython.viper
def drawWall(bmp, x: int, drawStart: int, height: int, vs: int, m: int, u: int):
    if(height == 0):
        return
    sprtptr = ptr8(bmp[0])
    sprtptr2 = ptr8(bmp[1])
    ptr = ptr8(thumby.display.buffer)
    ptr2 = ptr8(thumby.display.shading)
    screenWidth = int(SW)
    screenHeight = int(SH)
    for y in range(height):
        j = drawStart+y
        i = (j >> 3) * screenWidth + x
        v = (vs+y*m) >> 8
        c = sprtptr[(v >> 3) * 24 + u] & (1 << (v & 0x07))  # 24 i hardcoded
        if c:
            v = 1 << (j & 0x07)
            ptr[i] |= v
        else:
            v = 0xff ^ (1 << (j & 0x07))
            ptr[i] &= v
        v = (vs+y*m) >> 8
        c2 = sprtptr2[(v >> 3) * 24 + u] & (1 << (v & 0x07))  # 24 i hardcoded
        if c2:
            v = 1 << (j & 0x07)
            ptr2[i] |= v
        else:
            v = 0xff ^ (1 << (j & 0x07))
            ptr2[i] &= v

    drawEnd = drawStart + height
    if drawEnd < screenHeight:
        for y in range(drawEnd, screenHeight):
            i = (y >> 3) * screenWidth + x
            if y == drawEnd:
                v = 0xff ^ (1 << (y & 0x07))
                ptr[i] &= v
                ptr2[i] &= v
            else:
                v = 1 << (y & 0x07)
                ptr[i] |= v
                ptr2[i] |= v


@micropython.viper
def drawWall2(bmp, x: int, drawStart: int, height: int, vs: int, m: int, u: int):
    if(height == 0):
        return
    sprtptr = ptr8(bmp[0])
    sprtptr2 = ptr8(bmp[1])
    ptr = ptr8(thumby.display.buffer)
    ptr2 = ptr8(thumby.display.shading)
    screenWidth = int(SW)
    screenHeight = int(SH)
    for y in range(height):
        j = drawStart+y
        i = (j >> 3) * screenWidth + x
        v = (vs+y*m) >> 8
        c = sprtptr[(v >> 3) * 24 + u] & (1 << (v & 0x07))  # 24 i hardcoded
        if c:
            v = 1 << (j & 0x07)
            ptr[i] |= v
            ptr[i+1] |= v
        else:
            v = 0xff ^ (1 << (j & 0x07))
            ptr[i] &= v
            ptr[i+1] &= v
        v = (vs+y*m) >> 8
        c2 = sprtptr2[(v >> 3) * 24 + u] & (1 << (v & 0x07))  # 24 i hardcoded
        if c2:
            v = 1 << (j & 0x07)
            ptr2[i] |= v
            ptr2[i+1] |= v
        else:
            v = 0xff ^ (1 << (j & 0x07))
            ptr2[i] &= v
            ptr2[i+1] &= v

    drawEnd = drawStart + height
    if drawEnd < screenHeight:
        for y in range(drawEnd, screenHeight):
            i = (y >> 3) * screenWidth + x
            if y == drawEnd:
                v = 0xff ^ (1 << (y & 0x07))
                ptr[i] &= v
                ptr[i+1] &= v
                ptr2[i] &= v
                ptr2[i+1] &= v
            else:
                v = 1 << (y & 0x07)
                ptr[i] |= v
                ptr[i+1] |= v
                ptr2[i] |= v
                ptr2[i+1] |= v


@micropython.viper
def capture():
    ptr = ptr8(thumby.display.buffer)
    ptr2 = ptr8(thumby.display.shading)
    res = bytearray(thumby.display.buffer)
    res2 = bytearray(thumby.display.shading)
    return [res, res2]


@micropython.viper
def drawMeltScreen(bmp, mapptr: ptr8, offset: int):
    sprtptr = ptr8(bmp[0])
    sprtptr2 = ptr8(bmp[1])
    ptr = ptr8(thumby.display.buffer)
    ptr2 = ptr8(thumby.display.shading)
    screenWidth = int(thumby.display.width)
    screenHeight = int(thumby.display.height)

    for x in range(screenWidth):
        o = mapptr[x]+offset
        if(o < 0):
            o = 0
        for y in range(screenHeight):
            dy = y+o
            if dy >= screenHeight:
                break
            if(sprtptr[(y >> 3) * screenWidth + x] & (1 << (y & 0x07))):
                ptr[(dy >> 3) * screenWidth + x] |= 1 << (dy & 0x07)
            else:
                ptr[(dy >> 3) * screenWidth + x] &= 0xff ^ (1 << (dy & 0x07))
            if(sprtptr2[(y >> 3) * screenWidth + x] & (1 << (y & 0x07))):
                ptr2[(dy >> 3) * screenWidth + x] |= 1 << (dy & 0x07)
            else:
                ptr2[(dy >> 3) * screenWidth + x] &= 0xff ^ (1 << (dy & 0x07))


# @micropython.native
# def drawScaled(bmpM, d: float, x: int, y: int, width: int, height: int, pixelWidth: int, pixelHeight: int):
#     bmp, mask = bmpM
#     sprtptr = ptr8(bmp[0])
#     #sprtptr2 = ptr8(bmp[1])
#     maskptr = ptr8(mask)
#     global depthMap
#     screenWidth = int(SW)
#     screenHeight = int(SH)

#     for i in range(width):
#         dx = x+i
#         if(dx < 0):
#             continue
#         elif (dx >= screenWidth):
#             break
#         w = int(i*pixelWidth/width)
#         for j in range(height):
#             dy = y+j
#             if(dy < 0):
#                 continue
#             elif (dy >= screenHeight):
#                 break
#             if(depthMap[dx] < d):
#                 continue
#             _drawPixel(thumby.display.buffer, sprtptr, maskptr, dx, dy, w, int(
#                 j*pixelHeight/height), pixelWidth, screenWidth)

# @micropython.viper
# def drawPixel(ptr: ptr8, sprtptr: ptr8, maskptr: ptr8, x: int, y: int, u: int, v: int, width: int, screenWidth: int):
#     p = (v >> 3) * width + u
#     if(maskptr[p] & (1 << (v & 0x07))):
#         if(sprtptr[p] & (1 << (v & 0x07))):
#             ptr[(y >> 3) * screenWidth + x] |= 1 << (y & 0x07)
#         else:
#             ptr[(y >> 3) * screenWidth + x] &= 0xff ^ (1 << (y & 0x07))


@micropython.viper
def negativeEffect():
    ptr = ptr8(thumby.display.buffer)
    screenWidth = int(thumby.display.width)
    screenHeight = int(thumby.display.height)

    for i in range(int(len(thumby.display.buffer))):
        ptr[i] = 0xff ^ ptr[i]


@micropython.viper
def blitScaledWithMask(bmpM, x: int, y: int, width: int, height: int, mirrorX: int, minX: int, maxX: int, scale: int, realWidth: int):
    if(x+width < 0 or x > 71):
        return
    if(y+height < 0 or y > 39):
        return

    bmp, mask = bmpM

    if isinstance(bmp, (tuple, list)):
        gs = True
        sprtptr = ptr8(bmp[0])
        sprtptr2 = ptr8(bmp[1])
    else:
        gs = False
        sprtptr = ptr8(bmp)
        sprtptr2 = ptr8(0)

    maskptr = ptr8(mask)

    xStart = int(x)
    yStart = int(y)
    ptr = ptr8(thumby.display.buffer)
    ptr2 = ptr8(thumby.display.shading)

    yFirst = 0-yStart
    blitHeight = height
    if yFirst < 0:
        yFirst = 0
    if yStart+height > 40:
        blitHeight = 40-yStart

    y = yFirst

    xFirst = minX-x
    blitWidth = maxX-x

    while y < blitHeight:
        x = xFirst
        while x < blitWidth:
            sy = ((y*scale) >> 8)
            i = (sy >> 3) * realWidth + \
                (((width-1-x if mirrorX == 1 else x)*scale) >> 8)
            if(maskptr[i] & (1 << ((sy) & 0x07))):
                if(sprtptr[i] & (1 << ((sy) & 0x07))):
                    ptr[((yStart+y) >> 3) * int(72) +
                        xStart+x] |= 1 << ((yStart+y) & 0x07)
                else:
                    ptr[((yStart+y) >> 3) * int(72) + xStart +
                        x] &= 0xff ^ (1 << ((yStart+y) & 0x07))
                if(gs and sprtptr2[i] & (1 << ((sy) & 0x07))):
                    ptr2[((yStart+y) >> 3) * int(72) +
                         xStart+x] |= 1 << ((yStart+y) & 0x07)
                else:
                    ptr2[((yStart+y) >> 3) * int(72) + xStart +
                         x] &= 0xff ^ (1 << ((yStart+y) & 0x07))
            x += 1
        y += 1


@micropython.viper
def blitWithMask(bmpM, x: int, y: int, width: int, height: int, mirrorX: int, minX: int, maxX: int):
    if(x+width < 0 or x > 71):
        return
    if(y+height < 0 or y > 39):
        return

    bmp, mask = bmpM

    if isinstance(bmp, (tuple, list)):
        gs = True
        sprtptr = ptr8(bmp[0])
        sprtptr2 = ptr8(bmp[1])
    else:
        gs = False
        sprtptr = ptr8(bmp)
        sprtptr2 = ptr8(0)

    maskptr = ptr8(mask)

    xStart = int(x)
    yStart = int(y)
    ptr = ptr8(thumby.display.buffer)
    ptr2 = ptr8(thumby.display.shading)

    yFirst = 0-yStart
    blitHeight = height
    if yFirst < 0:
        yFirst = 0
    if yStart+height > 40:
        blitHeight = 40-yStart

    y = yFirst

    xFirst = minX-x
    blitWidth = maxX-x
    while y < blitHeight:
        x = xFirst
        while x < blitWidth:
            i = ((y) >> 3) * width + (width-1-x if mirrorX == 1 else x)
            if(maskptr[i] & (1 << ((y) & 0x07))):
                if(sprtptr[i] & (1 << ((y) & 0x07))):
                    ptr[((yStart+y) >> 3) * int(72) +
                        xStart+x] |= 1 << ((yStart+y) & 0x07)
                else:
                    ptr[((yStart+y) >> 3) * int(72) + xStart +
                        x] &= 0xff ^ (1 << ((yStart+y) & 0x07))
                if(gs and sprtptr2[i] & (1 << ((y) & 0x07))):
                    ptr2[((yStart+y) >> 3) * int(72) +
                         xStart+x] |= 1 << ((yStart+y) & 0x07)
                else:
                    ptr2[((yStart+y) >> 3) * int(72) + xStart +
                         x] &= 0xff ^ (1 << ((yStart+y) & 0x07))
            x += 1
        y += 1
