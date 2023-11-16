import csv
import glob
import os
import os.path
from subprocess import call
from concurrent.futures import ThreadPoolExecutor

def extract_images_from_video(video_path):
    video_parts = get_video_parts(video_path)
    train_or_test, classname, filename_no_ext, filename = video_parts

    if not check_already_extracted(video_parts):
        src = train_or_test + '/' + classname + '/' + filename
        dest = train_or_test + '/' + classname + '/' + filename_no_ext + '-%04d.jpg'
        call(["ffmpeg", "-i", src, dest])

    nb_frames = get_nb_frames_for_video(video_parts)
    return [train_or_test, classname, filename_no_ext, nb_frames]

def extract_files_with_threads():
    data_file = []
    folders = ['./train/', './test/']

    with ThreadPoolExecutor(max_workers=32) as executor:
        for folder in folders:
            class_folders = glob.glob(folder + '*')

            for vid_class in class_folders:
                class_files = glob.glob(vid_class + '/*.avi')

                # video_parts_list = [get_video_parts(video) for video in class_files]

                results = list(executor.map(extract_images_from_video, class_files))

                for result in results:
                    data_file.append(result)
                    print("Generated %d frames for %s" % (result[3], result[2]))

    with open('data_file.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_file)

    print("Extracted and wrote %d video files." % (len(data_file)))

def get_nb_frames_for_video(video_parts):
    train_or_test, classname, filename_no_ext, _ = video_parts
    generated_files = glob.glob(train_or_test + '/' + classname + '/' +
                                filename_no_ext + '*.jpg')
    return len(generated_files)

def get_video_parts(video_path):
    parts = video_path.split('/')
    filename = parts[3]
    filename_no_ext = filename.split('.')[0]
    classname = parts[2]
    train_or_test = parts[1]

    return train_or_test, classname, filename_no_ext, filename

def check_already_extracted(video_parts):
    train_or_test, classname, filename_no_ext, _ = video_parts
    return bool(os.path.exists(train_or_test + '/' + classname +
                               '/' + filename_no_ext + '-0001.jpg'))

if __name__ == '__main__':
    extract_files_with_threads()
