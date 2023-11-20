import os

def get_train_test_lists(version='01'):
    test_file = f'./ucfTrainTestlist/testlist{version}.txt'
    train_file = f'./ucfTrainTestlist/trainlist{version}.txt'

    with open(test_file) as fin:
        test_list = [row.split(' ')[0] for row in fin.readlines()]

    with open(train_file) as fin:
        train_list = [row.split(' ')[0] for row in fin.readlines()]

    return {'train': train_list, 'test': test_list}

def move_files(file_groups):
    for group, videos in file_groups.items():
        for video in videos:
            video = video.strip()
            classname, filename = video.split('/')
    
            dest = f'{group}/{classname}/{filename}'

            if not os.path.exists(dest):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                print(f"Moving {filename} to {dest}")
                os.rename(filename, dest)
            else:
                print(f"{dest} already exists. Skipping.")

    print("Done.")

if __name__ == '__main__':
    groups = get_train_test_lists()
    move_files(groups)
