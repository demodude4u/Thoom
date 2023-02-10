__version__ = "0.0.2"
__author__ = "Demod"

import zlib
import gc

try:
    from thumbyGrayscale import Sprite
    gs = True
except ImportError:
    from thumbySprite import Sprite
    gs = False

M_RAW = 0x00
M_PY = 0x01
M_IMG = 0x10
M_IMGM = 0x11
M_IMGGS = 0x12
M_IMGGSM = 0x13


class ZPackFile:
    def __init__(self, file):
        gc.collect()

        zfs = open(file, 'rb')
        zds = zlib.DecompIO(zfs)
        mfs, _ = _rU32(zds.read(4), 0)
        self.mfd = zds.read(mfs)
        mfv = memoryview(self.mfd)
        self.entries = {}

        mfc, o = _rU8(mfv, 0)
        for i in range(mfc):
            k, o = _rStr(mfv, o)
            m, o = _rU8(mfv, o)
            dc, o = _rU8(mfv, o)
            d = []
            for j in range(dc):
                dl, o = _rU32(mfv, o)
                # print("memfree: "+str(gc.mem_free()))
                # print(k+"["+str(j)+"] "+str(dl)+" bytes")
                dba = bytearray(dl)
                zds.readinto(dba)
                d.append(dba)
            e = ZPackEntry(m, d)
            if m & 0x10:
                e.w, o = _rU16(mfv, o)
                e.h, o = _rU16(mfv, o)
            elif m == M_PY:
                e.n, o = _rStr(mfv, o)
            self.entries[k] = e

        gc.collect()

    def metadata(self, key):
        return self.entries[key]

    def raw(self, key):
        e = self.entries[key]
        return e.d[0]

    def bitmap(self, key):
        e = self.entries[key]
        m = e.m
        d = e.d
        if m == M_RAW or m == M_IMG or m == M_IMGM or not gs:
            return d[0]
        if m == M_IMGGS or m == M_IMGGSM:
            return (d[0], d[1])

    def mask(self, key):
        e = self.entries[key]
        m = e.m
        d = e.d
        if m == M_IMGM:
            return d[1]
        if m == M_IMGGSM:
            return d[2]

    def bitmapAndMask(self, key):
        return (self.bitmap(key), self.mask(key))

    def sprite(self, key, w=None, h=None):
        entry = self.entries[key]
        if w is None:
            w = entry.w
        if h is None:
            h = entry.h
        return Sprite(w, h, self.bitmap(key))

    def spriteMask(self, key, w=None, h=None):
        entry = self.entries[key]
        if w is None:
            w = entry.w
        if h is None:
            h = entry.h
        mask = self.mask(key)
        if mask is not None:
            return Sprite(w, h, mask)

    def spriteAndMask(self, key, w=None, h=None):
        return (self.sprite(key), self.spriteMask(key))

    def python(self, key):
        # TODO
        pass


class ZPackEntry:
    def __init__(self, m, d):
        self.m = m
        self.d = d


def _rU8(mv, o):
    return mv[o], o+1


def _rU16(mv, o):
    return (mv[o] << 8) + mv[o+1], o+2


def _rU32(mv, o):
    return (mv[o] << 24) + (mv[o+1] << 16) + (mv[o+2] << 8) + mv[o+3], o+4


def _rStr(mv, o):
    l, o = _rU16(mv, o)
    return str(mv[o:o+l], 'utf8'), o+l


def _rBA(mv, o, l):
    return mv[o:o+l], o+l
