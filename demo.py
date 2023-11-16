import os
import time
import operator 
import csv
import numpy as np
from pathlib import Path
from shutil import copyfile

from config import parse_opts
from utils.lib_createDir import prepare_walter_dirs
from utils.lib_hls import get_container_csv, download_containers, download_segments
from utils.lib_hls import natural_keys
from utils.lib_thumbnails import extract_thumbnails, process_image
from utils.lib_ucf import UCFDataSet
from models.convNeXt import create_model

# Parse configurations
config = parse_opts()

# Define video lists for different genres
soccer_video_list = ['Brazil_v_Belgium_2018', 'France_v_Croatia_2018']
baseket_video_list = []
boxing_video_list = []
baseball_video_list = []
cricket_video_list = []
tennis_video_list = []

# Set environment variables
os.environ["TF_GPU_THREAD_MODE"] = "gpu_private"
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = config.device

model_path = './output/2022_07_27_1136_ucf101_ConvNeXtBase_best/checkpoints/236-0.44.hdf5'
model = create_model()
model.load_weights(model_path)

ucf_data = UCFDataSet()

# Function for event recognition using thumbnails
def event_recognition(thumbnail_dir, detect_thumb_csv):
    threshold = 0.80
    scenes_data = []

    # Loop through thumbnails
    for fileName in os.listdir(thumbnail_dir):
        img_fileName = os.path.join(thumbnail_dir, fileName)
        image_arr = process_image(img_fileName, (config.spatial_size, config.spatial_size, 3))
        image_arr = np.expand_dims(image_arr, axis=0)

        predictions = model.predict([image_arr])
        label_predictions = {label: pred for label, pred in zip(ucf_data.classes, predictions[0])}
        sorted_lps = sorted(label_predictions.items(), key=operator.itemgetter(1), reverse=True)

        for i, class_prediction in enumerate(sorted_lps):
            if float(class_prediction[1]) >= threshold:
                scenes_data.append([img_fileName, class_prediction[0]])

    with open(detect_thumb_csv, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(scenes_data, key=natural_keys))

# Function to personalize thumbnails based on video genre
def get_personlize_thumbnails(detect_thumb_csv, process_thumb_csv, video_genre):
    count = 0
    video_data = []
    with open(detect_thumb_csv, 'r') as fin:
        reader = csv.reader(fin)
        for row in reader:
            if video_genre == 'Soccer':
                if row[1] == 'SoccerJuggling' or row[1] == 'SoccerPenalty':
                    src = row[0]
                    folder_path = Path(row[0]).parts[1]
                    dst = os.path.join(config.sample_path, folder_path, 'per_thumb',os.path.basename(row[0]))
                    print(src, dst)
                    copyfile(src, dst)
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif video_genre == 'Baseketball':
                if row[1] == 'Basketball' or row[1] == 'BasketballDunk':
                    src = row[0]
                    folder_path = Path(row[0]).parts[1]
                    dst = os.path.join(config.sample_path, folder_path, 'per_thumb',os.path.basename(row[0]))
                    print(src, dst)
                    copyfile(src, dst)
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif video_genre == 'Boxing':
                if row[1] == 'BoxingPunchingBag' or row[1] == 'BoxingSpeedBag' or row[1] == 'Punch':
                    src = row[0]
                    folder_path = Path(row[0]).parts[1]
                    dst = os.path.join(config.sample_path, folder_path, 'per_thumb',os.path.basename(row[0]))
                    print(src, dst)
                    copyfile(src, dst)
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif video_genre == 'Baseball':
                if row[1] == 'BaseballPitch':
                    src = row[0]
                    folder_path = Path(row[0]).parts[1]
                    dst = os.path.join(config.sample_path, folder_path, 'per_thumb',os.path.basename(row[0]))
                    print(src, dst)
                    copyfile(src, dst)
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif video_genre == 'Cricket':
                if row[1] == 'CricketBowling'or row[1] == 'CricketShot':
                    src = row[0]
                    folder_path = Path(row[0]).parts[1]
                    dst = os.path.join(config.sample_path, folder_path, 'per_thumb',os.path.basename(row[0]))
                    print(src, dst)
                    copyfile(src, dst)
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif video_genre == 'Tennis':
                if row[1] == 'TennisSwing':
                    src = row[0]
                    folder_path = Path(row[0]).parts[1]
                    dst = os.path.join(config.sample_path, folder_path, 'per_thumb',os.path.basename(row[0]))
                    print(src, dst)
                    copyfile(src, dst)
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            else:
                print('Error: No category selected')

    with open(process_thumb_csv, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(video_data, key=natural_keys))

    print('Number of personalized thumbnails: {}'.format(count))
    return count


def get_vidSeg_timestamp(segment_csv, detect_thumbs_csv):
    with open(segment_csv, 'w') as f2:
        with open(detect_thumbs_csv) as f:
            reader = csv.reader(f)
            for rows in reader:
                            
                fileName = " ".join(rows)
                tempName = fileName.split("_")
                frameNumber = int(tempName[1])*25+int (tempName[2].split(".")[0])

                segment_no = int(frameNumber/10)
                segment_name = "out"+ '{:02}'.format(segment_no)+".ts"
                
                f2.write(str(segment_name)+"\n")

def remove_dublicate_row_csv (csv_file):
    count = 0
    with open(csv_file, 'r') as fin:
        lines = fin.readlines()
        lines = [line.strip() for line in lines]
        lines = list(set(lines))
        # lines = sorted(lines)
        lines.sort(key=natural_keys)
        with open(csv_file, 'w') as fout:
            for line in lines:
                fout.write(line + '\n')
                count += 1

    print('Number of detect segments: {}'.format(count))
    return count

def get_seg_file(seg_path):
    return [f for f in os.listdir(seg_path) if os.path.isfile(os.path.join(seg_path, f)) and f.endswith('.ts')]

def generate_GIF(segments_dest, gif_dest):
    files = get_seg_file(segments_dest)
    # print(files)
    for segment_no in files:
        print(os.path.join(segments_dest,segment_no))
        segment = os.path.join(segments_dest,segment_no)
        segment_name = segment_no.split(".")[0]
        pal_cmd = ("ffmpeg -y -t 5 -i " + segment + " -vf fps=10,scale=320:-1:flags=lanczos,palettegen " + os.path.join(gif_dest, segment_name)+"_palette.png")
        gif_cmd = ("ffmpeg -y -t 5 -i " + segment + " -i "+ os.path.join(gif_dest, segment_name) +"_palette.png " +" -lavfi \"fps=15,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse\" " + os.path.join(gif_dest, segment_name) +"_first.gif")
        os.system(pal_cmd)
        os.system(gif_cmd)

def main(video_genre):
    count = 1
    if video_genre == 'Soccer':
        video_list = soccer_video_list
    elif video_genre == 'Baseketball':
        video_list = baseket_video_list
    elif video_genre == 'Boxing':
        video_list = boxing_video_list
    elif video_genre == 'Baseball':
        video_list = baseball_video_list
    elif video_genre == 'Cricket':
        video_list = cricket_video_list
    elif video_genre == 'Tennis':
        video_list = tennis_video_list
    else:
        print('Error 404: No category found')

    for file_name in video_list:
        print('-'*80)
        print('{}: {}'.format(count, file_name))
        count += 1

        # Create paths for the videos
        main_video_dir, vid_container_dir, vid_thumbnail_dir, vid_segment_dir = prepare_walter_dirs(config.sample_path, file_name)
        print(main_video_dir, vid_container_dir, vid_thumbnail_dir, vid_segment_dir)

        text_file = open(os.path.join(main_video_dir,'process.txt'), "w")
        text_file.write(main_video_dir + '\n\n')

        containers_csv_url = os.path.join(config.server_ip, file_name, 'container_list.csv')   
        containers_url = os.path.join(config.server_ip,file_name,'thumbnails/')
        seg_movie_url = os.path.join(config.server_ip, file_name, 'segments')
        
        detect_thumb_csv = os.path.join(main_video_dir, 'detect_thumbs.csv')
        process_thumb_csv = os.path.join(main_video_dir, file_name+'_thumbs.csv')
        segmnets_csv = os.path.join(main_video_dir, file_name+'_segment.csv')
        
        select_thumb_path = os.path.join(main_video_dir, 'per_thumb')
        select_gifs_path = os.path.join(main_video_dir, 'per_gif')
        
        if not os.path.exists(select_thumb_path):
            os.makedirs(select_thumb_path)

        if not os.path.exists(select_gifs_path):
            os.makedirs(select_gifs_path)      

        # ==================================================
        start1 = time.time()
        get_container_csv(containers_csv_url, main_video_dir)
        download_containers(containers_url, main_video_dir, vid_container_dir)
        end1 = time.time()
        text_file.write('Download TCs seconds: ' + str(round(end1 - start1, 2)) + '----- mintues: ' + str(round (end1 - start1, 2)/60) +'\n')
        # ==================================================

        # ==================================================
        start2 = time.time()
        extract_thumbnails(vid_container_dir, vid_thumbnail_dir)
        end2 = time.time()
        text_file.write('Extract thumbnail seconds: ' + str(round(end2 - start2, 2)) + '----- mintues: ' + str(round (end2 - start2, 2)/60) +'\n')
        # ==================================================

        # ==================================================
        start3 = time.time()
        event_recognition(vid_thumbnail_dir, detect_thumb_csv)
        end3 = time.time()
        text_file.write('Event recognize seconds: ' + str(round(end3 - start3, 2)) + '----- mintues: ' + str(round (end3 - start3, 2)/60) +'\n')
        # ==================================================


        # ==================================================
        start4 = time.time()
        numb_thumbnails = get_personlize_thumbnails(detect_thumb_csv, process_thumb_csv, video_genre)    
        get_vidSeg_timestamp(segmnets_csv, process_thumb_csv)
        numb_segments = remove_dublicate_row_csv(segmnets_csv)

        # number of segments to download in order to generate gifs, if you numb_segments all the segments will be downloaded
        download_segments(seg_movie_url, segmnets_csv, vid_segment_dir, num_segments = numb_segments)
        end4 = time.time()
        text_file.write('Get timestamp: seconds: ' + str(round(end4 - start4, 2)) + '----- mintues: ' + str(round (end4 - start4, 2)/60)+'\n')
        # ==================================================


        # ==================================================
        start5 = time.time()
        generate_GIF(vid_segment_dir, select_gifs_path)
        end5 = time.time()
        text_file.write('Generate GIF sec: ' + str(round(end5 - start5, 2)) + ' mint: ' + str(round (end5 - start5, 2)/60) + '\n\n')

        text_file.write('Number of personalized thumbnails: ' + str(numb_thumbnails) +'\n')
        text_file.write('Number of detect segments: ' + str(numb_segments) +'\n')
        text_file.close()


if __name__ == "__main__":
    main(video_genre = config.category)
