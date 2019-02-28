def rgb_to_cmyk(r, g, b):
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    k = min(c, m, y)

    if k == 1:
        return 100.0, 100.0, 100.0, 100.0

    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)

    return c * 100.0, m * 100.0, y * 100.0, k * 100.0


def cmyk_to_rgb(c, m, y, k):
    c /= 100
    m /= 100
    y /= 100
    k /= 100
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return round(r), round(g), round(b)


def rgb_to_xyz(r, g, b):
    def func(param):
        if param >= 0.04045:
            return ((param + 0.055) / 1.055) ** 2.4
        else:
            return param / 12.92

    rn = func(r / 255) * 100
    gn = func(g / 255) * 100
    bn = func(b / 255) * 100

    x = 0.412453 * rn + 0.357580 * gn + 0.180423 * bn
    y = 0.212671 * rn + 0.715160 * gn + 0.072169 * bn
    z = 0.019334 * rn + 0.119193 * gn + 0.950227 * bn

    return x, y, z


def xyz_to_rgb(x, y, z):
    def func(param):
        if param < 0.0031308:
            return param * 12.92 * 255
        else:
            return (1.055 * (param ** (1 / 2.4)) - 0.055) * 255

    x = x / 100
    y = y / 100
    z = z / 100

    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    b = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z

    r = func(r)
    g = func(g)
    b = func(b)

    return round(r), round(g), round(b)


def xyz_to_lab(x, y, z, xn=95.047, yn=100, zn=108.883):
    def func(param):
        if param > (6 / 29) ** 3:
            return param ** (1 / 3)
        else:
            return param / (3 * (2 / 29) ** 2) + 4 / 29

    l = 116 * func(y / yn) - 16
    a = 500 * (func(x / xn) - func(y / yn))
    b = 200 * (func(y / yn) - func(z / zn))

    return l, a, b


def lab_to_xyz(l, a, b, xn=95.047, yn=100, zn=108.883):
    def func(param):
        if param > 6 / 29:
            return param ** 3
        else:
            return 3 * (6 / 29) ** 2 * (param - 4 / 29)

    x = xn * func((l + 16) / 116 + a / 500)
    y = yn * func((l + 16) / 116)
    z = zn * func((l + 16) / 116 - b / 200)

    return x, y, z


def rgb_to_lab(r, g, b):
    xyz = rgb_to_xyz(r, g, b)
    return xyz_to_lab(*xyz)


def lab_to_rgb(l, a, b):
    xyz = lab_to_xyz(l, a, b)
    return xyz_to_rgb(*xyz)
