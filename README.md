# FRC-GIF: Frame Ranking-based Personalized Artistic Media Generation Method for Resource Constrained Devices

<p align="center">
  <a href="https://gmujtaba.com/frcweb/"><strong>Project Page</strong></a>, <a href="https://ieeexplore.ieee.org/document/10336393/"><strong>Paper PDF</strong></a>, 
</p>

This repository contains the original implementation of the paper [**FRC-GIF: Frame Ranking-based Personalized Artistic Media Generation Method for Resource Constrained Devices**](https://ieeexplore.ieee.org/document/10336393/), published in the regular issue of IEEE Transactions on Big Data 2023.

## Prerequisite
- Linux
- Python 3.6
- CPU or NVIDIA GPU + CUDA CuDNN

## Getting Started
### Installation
- Clone this repo:
```bash
git clone https://github.com/iamgmujtaba/FRC-GIF.git
cd FRC-GIF

```
- To create conda environment and install cuda toolkit, run the following command:
```bash
conda create -n frcgif cudatoolkit=11.3 cudnn=8.2.1 python=3.9 -y
conda activate frcgif
```
- Installoath packages, run the following command 
```bash
pip install -r requirements.txt
```

- The system paths will be automatically configured when you activate this conda environment [ref](https://www.tensorflow.org/install/pip).

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

## Preparing the data
1. Create train and test folders
```bash
cd data && cd ucf101 && mkdir train && mkdir test
```

2. Download the dataset from UCF into the data folder:
```bash
wget wget https://www.crcv.ucf.edu/data/UCF101/UCF101.rar --no-check-certificate
```

3. Extract UCF101.rar file in the data folder
```bash
unrar e UCF101.rar
```

4.  Run the scripts in the data folder to move the videos to the appropriate folders
```bash
python 1_move_files_ucf101.py 
```

5. Run the scripts in the data folder to extract video frames in the train/test folders and make the CSV file. The CSV file will be used in the rest of the code references
```bash
python 2_extract_files_ucf101.py
```

- Note: You need FFmpeg installed to extract frames from videos. 

## Train and evaluate
To train the model, run the following command.

```bash
python train.py --dataset_path /path/to/UCF101 --model_name convNeXtBase --batch_size 32 --epochs 1000 --learning_rate 0.001 --num_classes 101 --save_model_path /path/to/save/model
```
Check [config.py](config.py) for the list of all the parameters.

- In order to evaluate the proposed method, you have to configure [hls-server](https://github.com/iamgmujtaba/hls-server).
- Use [vid2tc](https://github.com/iamgmujtaba/vid2tc) to generate thumbnail contaienrs from videos. For more information, please refer to the [paper](https://ieeexplore.ieee.org/document/9902992).
- - Download the pretrained model from [google drive](https://drive.google.com/drive/folders/1jZeBNrdhs8tOwgu8EiErW68Ul3rOEmtV?usp=sharing).
- Place the pretrained model in the [output](output) folder.
- Run the following command to test the proposed method.

```bash
python demo.py --category soccer 
```

## Experimental Results
### Preview of generated thumbnails using proposed and baseline methods.
![fig4](https://github.com/iamgmujtaba/FRC-GIF/assets/33286377/43d513bd-169f-44a2-b618-7166505bba7d)

### Preview of generated GIFs using proposed and baseline methods.
https://github.com/iamgmujtaba/FRC-GIF/assets/33286377/d085f7d3-02d8-4fd7-bc0b-177b6ae3645b



## Citation
If you use this code for your research, please cite our paper.
```
@ARTICLE{mujtabafrc,
  author={Mujtaba, Ghulam and Khowaja, Sunder Ali and Jarwar, Muhammad Aslam and Choi, Jaehyuk and Ryu, Eun-Seok},
  journal={IEEE Transactions on Big Data}, 
  title={FRC-GIF: Frame Ranking-Based Personalized Artistic Media Generation Method for Resource Constrained Devices}, 
  year={2023},
  volume={},
  number={},
  pages={1-14},
  doi={10.1109/TBDATA.2023.3338012}} 
```


