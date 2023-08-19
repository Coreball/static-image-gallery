import csv
import os.path
import subprocess
from PIL import Image
from multiprocessing import Pool

image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
video_extensions = [".mp4"]

thumb_size = 256, 256


def thumbnail(entry):
    filename = entry["Filename"]
    name, extension = os.path.splitext(filename)
    input_path = f"assets/{filename}"
    output_path = f"thumbnails/{name}.thumbnail.jpg"
    if extension in image_extensions:
        with Image.open(input_path) as image:
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.thumbnail(thumb_size)
            image.save(output_path)
    elif extension in video_extensions:
        subprocess.call(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "fatal",
                "-i",
                input_path,
                "-ss",
                "00:00:00.000",
                "-frames:v",
                "1",
                "-filter:v",
                "scale='if(gt(a,1),256,-2)':'if(gt(a,1),-2,256)'",
                output_path,
            ]
        )
    else:
        print("Unknown Extension")


if __name__ == "__main__":
    with open("db.csv", "r", newline="") as db:
        reader = csv.DictReader(db)
        data = list(reader)
    with Pool(8) as pool:
        pool.map(thumbnail, data)
