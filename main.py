import cv2
import imutils
from dataclasses import dataclass
from time import sleep


@dataclass
class Pixel:
    x: int
    y: int
    rgb: tuple[int,int,int]


class Image:
    def __init__(self) -> None:
        self.CHARACTERS_1 = " .°*oO#@"
        self.CHARACTERS_2 = """ .'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"""
        self.MAX_CHANNEL_VALUES = 255*3
    
    def pixel_intensity(self, pixel: Pixel) -> float:
        return sum(pixel.rgb) / self.MAX_CHANNEL_VALUES
    
    def map_character(self, intensity: float, mode=0) -> str:
        if mode == 0: return self.CHARACTERS_1[round(intensity*(len(self.CHARACTERS_1)-1))]
        else: return self.CHARACTERS_2[round(intensity*(len(self.CHARACTERS_2)-1))]
    
    
class Draw:
    def img_to_char(self, img) -> str:
        rows, cols, _ = img.shape
        cl = Image()
        curr_string = ""
        
        # we skip every second line on the y-axís
        # because of font height
        for y in range(0, rows, 2):
            for x in range(cols):
                (b,g,r) = img[y,x]
                k = cl.pixel_intensity(Pixel(x,y,(r,g,b)))
                char = cl.map_character(k, 0)
                curr_string += char
            curr_string += "\n"
        return curr_string
    
    def draw_image(self, img_ascii):
        print(img_ascii)

   
def video_ascii_art(file_path: str):
    frames = []
    cap = cv2.VideoCapture(file_path)
    ret, frame = cap.read()
    height, width, _ = frame.shape
    dr = Draw()
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False: break
        frame = imutils.resize(frame, width=150, height=150)
        frames.append(frame)
    
    frame_strings = []
    for i in range(len(frames)):
        frame_strings.append(dr.img_to_char(frames[i]))
    
    for frame in frame_strings:
        dr.draw_image(frame) 
        sleep(0.05)
        # not a good way to "clear" the console
        # os.system('cls') causes flickering
        print("\n"*height)
    

def img_ascii_art(file_path):
    img = cv2.imread(file_path)
    imgr = imutils.resize(img, width=150, height=150)
    dr = Draw()
    arr = dr.img_to_char(imgr)
    dr.draw_image(arr)
