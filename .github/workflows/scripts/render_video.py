
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
DURATION = 15
FPS = 30

BACKGROUND = "#101B2D"
ACCENT = "#42D6C5"
TEXT = "#F3F6FA"

def rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def get_font(size, bold=False):
    path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    return ImageFont.truetype(path, size)

image = Image.new("RGB", (WIDTH, HEIGHT), rgb(BACKGROUND))
draw = ImageDraw.Draw(image)

draw.ellipse(
    (WIDTH - 440, 190, WIDTH + 180, 810),
    outline=rgb(ACCENT),
    width=8
)
draw.ellipse(
    (WIDTH - 340, 290, WIDTH + 80, 710),
    outline=rgb(ACCENT),
    width=3
)

draw.rounded_rectangle(
    (90, 250, 360, 270),
    radius=10,
    fill=rgb(ACCENT)
)

draw.text(
    (90, 520),
    "LABORATORIO",
    font=get_font(62, True),
    fill=rgb(TEXT)
)

draw.text(
    (90, 610),
    "DE IA",
    font=get_font(112, True),
    fill=rgb(ACCENT)
)

draw.text(
    (95, 810),
    "Automacao em construcao.",
    font=get_font(42),
    fill=rgb(TEXT)
)

draw.text(
    (95, 900),
    "Teste de renderizacao | 9:16",
    font=get_font(30),
    fill=rgb(ACCENT)
)

draw.text(
    (95, HEIGHT - 190),
    "EP. 001 | TECNOLOGIA",
    font=get_font(28, True),
    fill=rgb(TEXT)
)

image_path = OUTPUT / "frame.png"
image.save(image_path)

video_path = OUTPUT / "video_teste.mp4"

command = [
    "ffmpeg", "-y",
    "-loop", "1",
    "-i", str(image_path),
    "-f", "lavfi",
    "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
    "-t", str(DURATION),
    "-r", str(FPS),
    "-vf", f"scale={WIDTH}:{HEIGHT},format=yuv420p",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    str(video_path)
]

subprocess.run(command, check=True)

print(f"Video gerado com sucesso: {video_path}")
