# Program to detect the convex hull of an image

from PIL import Image, ImageDraw


def preprocess(img):

    points = []

    for i in range(img.width):
        for j in range(img.height):
            if img.getpixel((i, j)):
                points.append((i, j))

    return points


def left_point(points):
    l = 0

    for i in range(1, len(points)):
        if points[i][0] < points[l][0]:
            l = i
        elif points[i][0] == points[l][0]:
            if points[i][1] > points[l][1]:
                l = i

    return l


def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def convex_hull(points):

    l = left_point(points)

    hull = []
    n = len(points)

    p, q = l, 0

    while True:

        hull.append(points[p])
        q = (p + 1) % n

        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        if p == l:
            break

    return hull


def draw_polygon(img, points, fill_color):
    drawing_ctx = ImageDraw.Draw(img)
    drawing_ctx.polygon(points, fill=fill_color)


def difference(img1, img2):
    if img1.size != img2.size:
        raise ValueError("img1 and img2 must have same size")

    result = Image.new("L", (img1.width, img1.height))

    for i in range(img1.width):
        for j in range(img1.height):
            result.putpixel((i, j), abs(img1.getpixel((i, j)) - img2.getpixel((i, j))))

    return result


if __name__ == "__main__":

    img_file = input("Image filename: ").strip()
    img = Image.open(img_file).convert("1")

    points = preprocess(img)

    hull = convex_hull(points)

    hull_img = Image.new("L", (img.width, img.height))
    fill_color = 50
    draw_polygon(hull_img, hull, fill_color)

    diff = difference(hull_img, img.convert(("L")))
    diff = diff.point(
        lambda p: 255 if p == 255 - fill_color else (128 if p == fill_color else 0)
    )

    diff.save('difference.png')

    hull_img = hull_img.point(
        lambda p: 255 if p == fill_color else 0
    )

    hull_img.save('convex_hull.png')