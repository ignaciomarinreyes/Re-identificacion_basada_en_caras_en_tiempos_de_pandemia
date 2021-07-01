import datetime
import argparse
import os
import sys
import cv2


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Script to extract frames from TGC videos')
    parser.add_argument('-input', '-i', help='Video filename', required=True)
    parser.add_argument(
        '-folder', '-f', help='Folder to save frames', required=True)
    parser.add_argument(
        '-prefix', '-p', help='Prefix name for frames', required=True)
    parser.add_argument(
        '-framespersec', '-fps', help='Number of frames to extract for second', required=True)
    args = parser.parse_args()
    return args


def check_files(videofile):
    if not os.path.isfile(videofile):
        print('ERROR: {} not found'.format(videofile))
        return False
    return True


def check_frames_folder(framefolder):
    if not os.path.isdir(framefolder):
        print('ERROR: {} folder not found'.format(framefolder))
        return False
    else:
        return True


def extract_frames(videofile, frames_folder, start_time, num_frames, frames_per_sec, frame_prefix):
    vid = cv2.VideoCapture(videofile)
    if 50 % frames_per_sec != 0:
        print('ERROR: Number of frames per second must be divisor of 50')
        return False
    inc_frames = int(50 / frames_per_sec)
    frame_time = start_time
    i = 0
    while i < num_frames:
        ret, frame = vid.read()
        if not ret:
            print('ERROR reading video {}'.format(videofile))
            return False
        if i % inc_frames == 0:
            frame_name = '{}frame_{}_{:03d}.jpg'.format(frame_prefix,
                                                        frame_time.strftime('%H_%M_%S'),
                                                        int(frame_time.microsecond / 1000))
            print(os.path.join(frames_folder, frame_name))
            cv2.imwrite(os.path.join(frames_folder, frame_name), frame)
        frame_time = frame_time + datetime.timedelta(hours=0, minutes=0, seconds=0.02, milliseconds=0)
        i = i + 1
    return True


def main():
    params = parse_arguments()
    videofile = params.input
    if not check_files(videofile):
        sys.exit(-1)
    if not check_frames_folder(params.folder):
        sys.exit(-1)
    init_time_str = "2020-10-24T15:35:33-0000"
    init_time = datetime.datetime.strptime(
        init_time_str, '%Y-%m-%dT%H:%M:%S%z')
    duration = 27500
    extract_frames(params.input, params.folder, init_time, duration,
                   int(params.framespersec),
                   params.prefix)


if __name__ == '__main__':
    main()

# source /Users/ignacio/PycharmProjects/untitled/venv/bin/activate
# python /Users/ignacio/TFG/TFG/MyAlgorithm/readFrames.py -input /Users/ignacio/Downloads/C0001.mp4 -folder /Users/ignacio/TFG/TFG/data/LPATrail19/ -prefix Salida_ -framespersec 5
# python /Users/ignacio/TFG/TFG/MyAlgorithm/readFrames.py -input /Users/ignacio/VideosTFG/sss -folder /Users/ignacio/TFG/TFG/data/LPATrail21/ -prefix Salida_ -framespersec 5
