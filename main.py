# -*- coding: utf-8 -*-

import math
import os
import shutil

import cv2
import moviepy.editor as mpe
from PIL import Image

FILE_NAME = ""


def empty_frames():
    path = os.path.join(os.path.dirname(__file__), "images")
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def extract_frames(file_name):
    video = cv2.VideoCapture(
        os.path.join(
            os.path.dirname(__file__),
            "input",
            file_name
        )
    )

    count = 0
    success = 1
    while success:
        success, image = video.read()

        if image is None:
            break

        file_name = "frame_{}.png".format(count)

        cv2.imwrite(
            os.path.join(os.path.dirname(__file__), "images", file_name),
            image
        )
        print("Extracted {}".format(file_name))
        count += 1

    return video.get(cv2.CAP_PROP_FPS)


def outline(image_path):
    image = Image.open(image_path)
    out = Image.new("I", image.size, 0xffffff)
    width, height = image.size
    for x in range(1, width):
        for y in range(1, height):
            r1, g1, b1 = image.getpixel((x, y))
            r2, g2, b2 = image.getpixel((x - 1, y - 1))
            diff = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
            if diff > 5:
                out.putpixel((x, y), 0)
    out.save(image_path)


def export_to_video(_fps):
    image_path = os.path.join(os.path.dirname(__file__), "images")
    images = [os.path.join(image_path, "frame_{}.png".format(j)) for j in range(0, len(os.listdir(image_path)))]
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape
    out = cv2.VideoWriter(
        os.path.join(os.path.dirname(__file__), "output", "output.avi"),
        0,
        _fps,
        (width, height)
    )
    for counter, image in enumerate(images):
        print("Processing frame_{}.png".format(counter))
        im = cv2.imread(image)
        out.write(im)

    cv2.destroyAllWindows()
    out.release()


def fix_audio():
    audio_path = os.path.join(
        os.path.dirname(__file__),
        "input",
        "audio.mp3"
    )
    audioclip = mpe.VideoFileClip(os.path.join(
        os.path.dirname(__file__),
        "input",
        FILE_NAME
    ))
    audioclip.audio.write_audiofile(
        audio_path
    )
    videoclip = mpe.VideoFileClip(os.path.join(os.path.dirname(__file__), "output", "output.avi"))
    audio_background = mpe.AudioFileClip(audio_path)

    new_audioclip = mpe.CompositeAudioClip([audio_background])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(os.path.join(os.path.dirname(__file__), "output", "final.mp4"))


if __name__ == "__main__":
    print("Emptying frames.")
    empty_frames()

    print("Extracting frames.")
    fps = extract_frames(FILE_NAME)

    print("Outlining frames.")
    image_paths = os.path.join(os.path.dirname(__file__), "images")
    for i in range(len(os.listdir(image_paths))):
        _file_name = "frame_{}.png".format(i)
        _image_path = os.path.join(image_paths, _file_name)
        print("Outlining {}".format(_file_name))
        outline(_image_path)

    print("Exporting to output video.")
    export_to_video(fps)

    print("Fixing audio.")
    fix_audio()
