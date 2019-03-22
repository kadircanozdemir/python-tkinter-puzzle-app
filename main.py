import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import Entry, Button, OptionMenu
import random
import cv2
import numpy as np
import os

pos1 = None
pos2 = None

class Tiles():
    def __init__(self):
        self.tiles = []

    def add(self, tile):
        self.tiles.append(tile)

    def shuffle(self):
        random.shuffle(self.tiles)
        i = 0
        for row in range(4):
            for col in range(4):
                self.tiles[i].pos = (row, col)
                i += 1

    def show(self):
        for tile in self.tiles:
            tile.show()

    def createBackwardImage(self):
        new_image = Image.new("RGB", (400, 400))
        for tile in self.tiles:
            row, col = tile.pos
            imageBox = tile.image
            size = 100
            new_image.paste(imageBox, (col * size, row * size))

        return new_image


class Tile(Label):
    def __init__(self, parent, imageTK, image, pos):
        self.label = Label.__init__(self, parent, image=imageTK)

        self.imageTK = imageTK
        self.image = image
        self.pos = pos
        self.parent = parent

    def show(self):
        self.grid(row=self.pos[0], column=self.pos[1])

class Board(Frame):
    BOARD_SIZE = 400

    def __init__(self, parent, image, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.image = self.openImage(image)
        self.tileSize = self.image.size[0] / 4
        self.tiles = self.createTiles()
        self.tiles.shuffle()
        self.tiles.createBackwardImage().save('temp.jpg')
        self.tiles.show()
        bottomFrame = Frame(parent)
        bottomFrame.pack(side=BOTTOM)
        Button(bottomFrame, text='Karıştır', command=self.shuffleButton).grid(column=0, row=5, pady=10)
        self.pos = self.tiles.tiles[0].pos
        self.tiles.tiles..label.bind("<Button-1>", self.clickBox)

    def clickBox(self):
        global pos1, pos2
        if pos1 is None:
            pos1 = self.pos
            print(pos1)
            return
        if pos2 is None:
            pos2 = self.pos
            print(pos2)

    def shuffleButton(self):
        self.tiles.shuffle()
        self.tiles.createBackwardImage().save('temp.jpg')
        self.tiles.show()

    def openImage(self, image):
        image = Image.open(image)
        # if min(image.size) > self.BOARD_SIZE:
        image = image.resize((self.BOARD_SIZE, self.BOARD_SIZE), Image.BOX)
        new_image = Image.new("RGB", (400, 400))
        new_image.paste(image, (0, 0))
        new_image.save('original.jpg')
        # if image.size[0] != image.size[1]:
        #     image = image.crop((0, 9, image.size[0], image.size[0]))
        return image

    def createTiles(self):
        tiles = Tiles()
        for row in range(4):
            for col in range(4):
                x0 = col * self.tileSize
                y0 = row * self.tileSize
                x1 = x0 + self.tileSize
                y1 = y0 + self.tileSize
                image = self.image.crop((x0, y0, x1, y1))
                imageTK = ImageTk.PhotoImage(image)
                tile = Tile(self, imageTK, image, (row, col))
                tiles.add(tile)
        return tiles

    def saveImage(self, image):
        image.save('temp.jpg')


class Main():
    def __init__(self, parent):
        self.parent = parent

        self.image = StringVar()

        self.createWidgets()

    def createWidgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame, text='Puzzle Oyunu', font=('', 50)).pack(padx=10, pady=10)
        frame = Frame(self.mainFrame)
        Label(frame, text='Image').grid(sticky=W)
        Entry(frame, textvariable=self.image, width=50).grid(row=0, column=1, pady=10, padx=10)
        Button(frame, text='Aç', command=self.browse).grid(row=0, column=2, pady=10, padx=10)
        frame.pack(padx=10, pady=10)
        Button(self.mainFrame, text='Başla', command=self.start).pack(padx=10, pady=10)
        self.mainFrame.pack()
        self.board = Frame(self.parent)
        self.winFrame = Frame(self.parent)

    def browse(self):
        self.image.set(filedialog.askopenfilename(title='Please select one (any) frame from your set of images.',
                                                  filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', '.gif',
                                                                              '.tiff', '.tif', '.bmp'])]))

    def start(self):
        image = self.image.get()
        if os.path.exists(image):
            self.board = Board(self.parent, image)
            self.mainFrame.pack_forget()
            self.board.pack()


def chunks(l, n):
    new_array = []
    for i in range(n):
        k = l[0 + i * n:4 + i * n]
        new_array.append(k)
    return new_array


def test_similar(img1, img2):
    h, w, d = img1.shape
    total = h * w * d
    diff = cv2.absdiff(img1, img2)
    num = (diff < 1).sum()
    return num * 100.0 / total


def get_image_piece(img, i, j):
    # if not (0 < i < 5 | 0 < j < 5): error!
    try:
        image_box = img
        h = image_box.shape[0]
        box_length = int(h / 4)
        return image_box[0 + box_length * i:100 + box_length * i, 0 + box_length * j:100 + box_length * j, :]
    except:
        print("slice error!")


def get_ij(arr, ij):
    for i in range(0, 4):
        for j in range(0, 4):
            if arr[i][j] == ij:
                return i, j


def get_shuffled_image(orj_img, indexes):
    shuffle_indexes = np.arange(16)
    random.shuffle(shuffle_indexes)
    shuffled_indexes = chunks(shuffle_indexes, 4)
    orginal_indexes = chunks(indexes, 4)
    # original_image = list()
    for i in range(0, 4):
        for j in range(0, 4):
            point = shuffled_indexes[i][j]
            r, c = get_ij(orginal_indexes, point)
            img_box = get_image_piece(orj_img, r, c)
            # original_image.append(img_box)
            cv2.imshow("aa", img_box)
            cv2.waitKey(0)
    # print(original_image)
    # cv2.imshow("aa", original_image)
    # cv2.waitKey(0)


def main():
    test_image = cv2.imread('karisik1.jpg')
    indexes = np.arange(16)
    print(chunks(indexes, 4))
    get_shuffled_image(test_image, indexes)


if __name__ == "__main__":
    # main()
    root = Tk()
    root.title("Puzzle Oyunu")
    Main(root)
    root.mainloop()
    '''
    https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
    https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    https://www.programcreek.com/python/example/89428/cv2.absdiff
    https://docs.opencv.org/2.4.13.7/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
    '''
