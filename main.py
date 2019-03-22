from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import Entry, Button
import random
import os

BOARD_SIZE = 400

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
        new_image = Image.new("RGB", (BOARD_SIZE, BOARD_SIZE))
        for tile in self.tiles:
            row, col = tile.pos
            imageBox = tile.image
            size = int(BOARD_SIZE / 4)
            new_image.paste(imageBox, (col * size, row * size))
        return new_image

    def swipe(self, pos1, pos2):
        row1, col1 = pos1
        row2, col2 = pos2

        temp = self.tiles[row1 * 4 + col1]
        self.tiles[row1 * 4 + col1] = self.tiles[row2 * 4 + col2]
        self.tiles[row2 * 4 + col2] = temp

        tempPos = self.tiles[row1 * 4 + col1].pos
        self.tiles[row1 * 4 + col1].pos = self.tiles[row2 * 4 + col2].pos
        self.tiles[row2 * 4 + col2].pos = tempPos


class Tile(Label):
    def __init__(self, parent, imageTK, image, pos):
        self.label = Label.__init__(self, parent, image=imageTK, borderwidth=2, relief="raised")

        self.imageTK = imageTK
        self.image = image
        self.pos = pos
        self.parent = parent

    def show(self):
        self.grid(row=self.pos[0], column=self.pos[1])


class Board(Frame):

    def __init__(self, parent, image, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.correct_pieces = 0
        self.score = 0
        self.parent = parent
        self.image = self.openImage(image)
        self.tileSize = self.image.size[0] / 4
        self.tiles = self.createTiles()

        self.original_image = self.tiles.createBackwardImage()
        self.original_image.save('original.jpg')

        bottomFrame = Frame(parent)
        bottomFrame.pack(side=BOTTOM)
        self.shuffleState = Label(bottomFrame, text="Karıştır butonuna basınız")
        self.shuffleState.grid(column=0, row=5, pady=10, padx=(0, 50))
        self.shuffleButton = Button(bottomFrame, text='Karıştır', command=self.shuffleButtonClick,
                                    disabledforeground="white")
        self.shuffleButton.grid(column=1, row=5, pady=10)
        self.scoreLabel = Label(bottomFrame, text="Score:")
        self.scoreLabel.grid(column=2, row=5, pady=10, padx=(100, 50))
        # self.tiles.tiles.label.bind("<Button-1>", self.clickBox)

    def clickBox(self, pos, tile):
        global pos1, pos2
        if pos1 is None:
            pos1 = pos
            print(pos1)
            return
        if pos2 is None:
            pos2 = pos
            print(pos2)
            self.changeBoxes()

    def changeBoxes(self):
        global pos1, pos2
        self.tiles.swipe(pos1, pos2)
        self.temp_image = self.tiles.createBackwardImage()
        # result: Doğru parça saysı
        self.result = test_point(self.original_image, self.temp_image)
        # doğru sayısı aynıysa 3 çıkar
        if self.correct_pieces == self.result:
            self.score = self.score - 3.0
        # doğru sayısı arttıysa 6.25*artış kadar ekle
        elif self.correct_pieces < self.result:
            self.score += 6.25 * (self.result - self.correct_pieces)

        self.scoreLabel.configure(text="Score: " + str(self.score))
        self.correct_pieces = self.result
        # kilitlenicek butanları bul ve kitle
        self.locks = test_similar(self.original_image, self.temp_image)
        for i in range(16):
            if self.locks[1][i]:
                self.tiles.tiles[i].unbind("<Button-1>")
                self.tiles.tiles[i].configure(borderwidth=2, relief="solid")
        ##kilitleme
        if self.correct_pieces == 16:
            file1 = open("enyuksekskor.txt", "a")
            scorestr = "Skor: " + str(self.score) + "\n"
            file1.write(scorestr)
            file1.close()
        self.tiles.show()
        pos1, pos2 = None, None

    def shuffleButtonClick(self):
        if self.correct_pieces == 0:
            self.tiles.shuffle()
            self.temp_image = self.tiles.createBackwardImage()
            # result: Doğru parça saysı
            self.result = test_point(self.original_image, self.temp_image)
            self.score += 6.25 * (self.result - self.correct_pieces)
            self.scoreLabel.configure(text="Score: " + str(self.score))
            self.correct_pieces = self.result
            self.shuffleState.destroy()
            # kilitlenicek butanları bul ve kitle
            self.locks = test_similar(self.original_image, self.temp_image)
            for i in range(16):
                if self.locks[1][i]:
                    self.tiles.tiles[i].unbind("<Button-1>")
                    self.tiles.tiles[i].configure(borderwidth=2, relief="solid")
            ##kilitleme bitti
            self.tiles.show()

    def openImage(self, image):
        image = Image.open(image)
        # if min(image.size) > self.BOARD_SIZE:
        image = image.resize((BOARD_SIZE, BOARD_SIZE), Image.NEAREST)

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
                tile.bind("<Button-1>", lambda event, tile=tile: self.clickBox(tile.pos, tile))
                tiles.add(tile)
        return tiles


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


def test_point(img1, img2):
    w, h = img1.size
    total = h * w
    ctr = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            r1, g1, b1 = img1.getpixel((i, j))
            r2, g2, b2 = img2.getpixel((i, j))
            diff = r1 - r2 + g1 - g2 + b1 - b2
            if diff == 0:
                ctr += 1
    num = ctr
    point = int(num * (BOARD_SIZE / 4.0) / total)
    correct_cnt = int(point / 6)
    # return doğru parça sayısı
    return correct_cnt


def test_similar(img1, img2):
    w, h = img1.size
    # total = h * w
    # counter = 0
    corrects = [True] * 16
    for row in range(4):
        for col in range(4):
            for i in range(row * int(BOARD_SIZE / 4), row * int(BOARD_SIZE / 4) + int(BOARD_SIZE / 4)):
                for j in range(col * int(BOARD_SIZE / 4), col * int(BOARD_SIZE / 4) + int(BOARD_SIZE / 4)):
                    r1, g1, b1 = img1.getpixel((i, j))
                    r2, g2, b2 = img2.getpixel((i, j))
                    diff = r1 - r2 + g1 - g2 + b1 - b2
                    if diff != 0:
                        corrects[col * 4 + row] = False
    # for i in range(0, BOARD_SIZE):
    #     for j in range(0, BOARD_SIZE):
    #         r1, g1, b1 = img1.getpixel((i, j))
    #         r2, g2, b2 = img2.getpixel((i, j))
    #         diff = r1 - r2 + g1 - g2 + b1 - b2
    #         if diff == 0:
    #             counter += 1
    # num = counter
    # point = int(num * (BOARD_SIZE / 4.0) / total)
    # return point / 6
    count = corrects.count(True)
    return count, corrects


def main():
    orj = Image.open('original.jpg')
    test = Image.open('temp.jpg')
    print(test_similar(orj, test))
    return
    # indexes = np.arange(16)
    # print(chunks(indexes, 4))
    # get_shuffled_image(test_image, indexes)


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
