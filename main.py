# -*- coding: utf-8 -*-

import os
import sys
import json

import cv2
import moviepy.editor as mpe


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


def fix_audio(file_name):
    audio_path = os.path.join(
        os.path.dirname(__file__),
        "input",
        "audio.mp3"
    )
    audioclip = mpe.VideoFileClip(os.path.join(
        os.path.dirname(__file__),
        "input",
        file_name
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
    file_name = sys.argv[1]
    action = sys.argv[2]
    if action == "extract":
        print("Extracting frames.")
        fps = extract_frames(file_name)
        data = {"fps": fps}
        with open(os.path.join(os.path.dirname(__file__), "input", "fps.json"), "w") as f:
            json.dump(data, f)


    elif action == "write":
        with open(os.path.join(os.path.dirname(__file__), "input", "fps.json"), "r") as f:
            data = json.load(f)
        print("Exporting to output video.")
        export_to_video(data["fps"])

        print("Fixing audio.")
        fix_audio(file_name)
