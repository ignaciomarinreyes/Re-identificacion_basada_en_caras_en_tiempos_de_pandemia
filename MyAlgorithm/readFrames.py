import xml.etree.ElementTree as ET
import datetime
import argparse
import os
import sys
import subprocess
import cv2

# 1 shows images
debug = 0


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Script to extract frames from TGC videos')
    parser.add_argument('-input', '-i', help='Video filename', required=True)
    # parser.add_argument('-xml', '-x', help='XML filename', required=True)
    parser.add_argument(
        '-folder', '-f', help='Folder to save frames', required=True)
    parser.add_argument(
        '-prefix', '-p', help='Prefix name for frames', required=True)
    parser.add_argument(
        '-framespersec', '-fps', help='Number of frames to extract for second', required=True)
    args = parser.parse_args()
    return args


def check_files(videofile, xmlfile):
    if not os.path.isfile(videofile):
        print('ERROR: {} not found'.format(videofile))
        return False
    #if not os.path.isfile(xmlfile):
    #    print('ERROR: {} not found'.format(xmlfile))
    #    return False
    return True


def check_frames_folder(framefolder):
    if not os.path.isdir(framefolder):
        print('ERROR: {} folder not found'.format(framefolder))
        return False
    else:
        return True


def get_video_time(xmlfile):
    defaultNS = '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.00}'

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for videoframe in root.iter(defaultNS + 'CreationDate'):
        init_time_str = videoframe.attrib['value']

    # check for UTC offset (zulu)
    if init_time_str[-1] == 'Z':
        init_time = datetime.datetime.strptime(
            init_time_str, '%Y-%m-%dT%H:%M:%SZ')
    else:
        # remove : from the timezone
        init_time_str = ''.join(init_time_str.rsplit(':', 1))
        init_time = datetime.datetime.strptime(
            init_time_str, '%Y-%m-%dT%H:%M:%S%z') # 2017-01-12T14:12:06

    for videoframe in root.iter(defaultNS + 'Duration'):
        duration_in_frames = int(videoframe.attrib['value'])

    return init_time, duration_in_frames


def extract_frames(videofile, frames_folder, start_time, num_frames, frames_per_sec, frame_prefix):
    base_videofile = videofile[:videofile.rfind('.')]

    vid = cv2.VideoCapture(videofile)

    if 50 % frames_per_sec != 0:
        print('ERROR: Number of frames per second must be divisor of 50')
        return False

    inc_frames = int(50 / frames_per_sec)  # captured at 50fps

    frame_time = start_time

    i = 0
    while i < num_frames:
        ret, frame = vid.read()
        if not ret:
            print('ERROR reading video {}'.format(videofile))
            return False

        if i % inc_frames == 0:
            # frame_name = '{}_frame_{}:{:03d}.png'.format(frame_prefix,
            frame_name = '{}frame_{}_{:03d}.png'.format(frame_prefix,
                                                         # frame_time.strftime('%H:%M:%S'),
                                                         frame_time.strftime('%H_%M_%S'),
                                                         int(frame_time.microsecond / 1000))
            print(frame_name)

            # time offset from start test FUNCIONA
            # if frame_time > start_time + datetime.timedelta(hours=0, minutes=20, seconds=20, milliseconds=0):
            print(os.path.join(frames_folder, frame_name))
            cv2.imwrite(os.path.join(frames_folder, frame_name), frame)

            if debug == 1:
                cv2.imshow("Image", frame)
                cv2.waitKey(4)

        frame_time = frame_time + \
                     datetime.timedelta(hours=0, minutes=0, seconds=0.02, milliseconds=0)
        i = i + 1

    return True


def main():
    params = parse_arguments()
    # print(params.input)
    # print(params.xml)
    # print(params.folder)
    # print(params.prefix)
    # print(params.chunkdur)

    videofile = params.input
    xml_filename = videofile[:videofile.rfind('.')] + 'M01.XML'

    if not check_files(videofile, xml_filename):
        sys.exit(-1)

    if not check_frames_folder(params.folder):
        sys.exit(-1)

    #init_time, duration = get_video_time(xml_filename)
    # print(init_time)
    # print(duration)
    init_time_str = "2021-05-20T12:00:00-0000"
    init_time = datetime.datetime.strptime(
        init_time_str, '%Y-%m-%dT%H:%M:%S%z')
    duration = 340800

    extract_frames(params.input, params.folder, init_time, duration,
                   int(params.framespersec),
                   params.prefix)


if __name__ == '__main__':
    main()

# source /Users/ignacio/PycharmProjects/untitled/venv/bin/activate
# python /Users/ignacio/TFG/TFG/MyAlgorithm/readFrames.py -input /Users/ignacio/Downloads/C0001.mp4 -folder /Users/ignacio/TFG/TFG/data/LPATrail19/ -prefix Salida_ -framespersec 5