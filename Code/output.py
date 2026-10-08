#Imports from Libraries:
import tkinter
from PIL import Image, ImageEnhance, ImageTk
from pathlib import Path

_root = None
_canvas = None
_image_item = None
_photo_image = None

def showImage(image_path: str, brightness: int = 255) -> None:
    global _root, _canvas, _image_item, _photo_image

    if not isinstance(brightness, int) or not 0 <= brightness <= 255:
        raise ValueError("brightness must be an integer from 0 to 255")

    if _root is None:
        _root = tkinter.Tk()
        _root.overrideredirect(1)
        screen_width = _root.winfo_screenwidth()
        screen_height = _root.winfo_screenheight()
        _root.geometry(f"{screen_width}x{screen_height}+0+0")
        _canvas = tkinter.Canvas(
            _root,
            width=screen_width,
            height=screen_height,
            borderwidth=0,
            highlightthickness=0,
            background="black",
        )
        _canvas.pack()
        _image_item = _canvas.create_image(
            screen_width / 2,
            screen_height / 2,
            state="hidden",
        )

    if image_path:
        pil_image = Image.open(Path(__file__).resolve().parent / image_path)
        screen_width = _root.winfo_screenwidth()
        screen_height = _root.winfo_screenheight()
        width, height = pil_image.size
        if width > screen_width or height > screen_height:
            ratio = min(screen_width / width, screen_height / height)
            pil_image = pil_image.resize(
                (int(width * ratio), int(height * ratio)),
                Image.Resampling.LANCZOS,
            )
        pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness / 255)
        _photo_image = ImageTk.PhotoImage(pil_image, master=_root)
        _canvas.itemconfigure(_image_item, image=_photo_image, state="normal")
    else:
        _canvas.itemconfigure(_image_item, state="hidden")
    _root.update()
