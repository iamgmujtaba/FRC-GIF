import json as simplejson
import os
import time
import shutil
####################################################################
####################################################################
# Print training configuration
def print_config(config):
    print('#'*60)
    print('Training configuration:')
    for k,v  in vars(config).items():
        print('  {:>20} {}'.format(k, v))
    print('#'*60)

# Write configuration to JSON file
def write_config(config, json_path):
    with open(json_path, 'w') as f:
        f.write(simplejson.dumps(vars(config), indent=4, sort_keys=True))

# Generate subdirectory for output
def output_subdir(config):
    prefix = time.strftime("%Y_%m_%d_%H%M")
    subdir = "{}_{}_{}".format(prefix, config.dataset, config.model)
    return os.path.join(config.save_dir, subdir)

# Prepare output directories
def prepare_output_dirs(config):
    config.save_dir = output_subdir(config)
    config.checkpoint_dir = os.path.join(config.save_dir, 'checkpoints')
    config.log_dir = os.path.join(config.save_dir, 'logs')

    os.makedirs(config.save_dir, exist_ok=True)
    os.makedirs(config.checkpoint_dir, exist_ok=True)
    os.makedirs(config.log_dir, exist_ok=True)
    return config

####################################################################
####################################################################
# Create directories for HLS server files download
def prepare_walter_dirs(vid_server_dir, video_title):
    prefix = time.strftime("%Y_%m_%d")
    subdir = "{}_{}".format(prefix, video_title)
    main_video_dir = os.path.join(vid_server_dir, subdir)

    vid_container_dir = os.path.join(main_video_dir, 'containers')
    vid_thumbnail_dir = os.path.join(main_video_dir, 'thumbnails')
    vid_segment_dir = os.path.join(main_video_dir, 'segments')

    os.makedirs(main_video_dir, exist_ok=True)
    os.makedirs(vid_container_dir, exist_ok=True)
    os.makedirs(vid_thumbnail_dir, exist_ok=True)
    os.makedirs(vid_segment_dir, exist_ok=True)

    return main_video_dir, vid_container_dir, vid_thumbnail_dir, vid_segment_dir
