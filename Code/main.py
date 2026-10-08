from artnet import receive_dmx
import tkinter
from PIL import Image, ImageTk


def showPIL(pilImage):
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+0+0")
    canvas = tkinter.Canvas(root, width=w, height=h, borderwidth=0, highlightthickness=0)
    canvas.pack()
    canvas.configure(background='black')

    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w / imgWidth, h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.Resampling.LANCZOS)

    image = ImageTk.PhotoImage(pilImage)
    canvas.create_image(w / 2, h / 2, image=image)
    root.mainloop()

def main():
    pilImage = Image.open("image.png")
    showPIL(pilImage)

main()