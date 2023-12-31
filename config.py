import argparse

def parse_opts():

    parser = argparse.ArgumentParser()
    
    #Paths
    parser.add_argument('--save_dir', default='./output/', type=str, help='Where to save training outputs.')
    parser.add_argument("--sample_path", type=str, default="./TestResults/", help="Path of video for containers, thumbnails, and segments for testing")
    parser.add_argument("--checkpoint_model", type=str, help="Optional path to checkpoint model for testing")
    
    # Dataset
    parser.add_argument('--dataset_path', default='./data/ucf101/', type=str, help='Path to location of dataset images')
    parser.add_argument('--dataset', default='ucf101', type=str, help='Dataset string (ucf13 | ucf101 | hmdb51)')
    parser.add_argument('--num_classes', default=101, type=int, help= 'Number of classes (ucf13: 13, ucf101: 101, hmdb51: 51)')

    # Preprocessing pipeline
    parser.add_argument('--spatial_size', default= 224, type=int, help='Height and width and hight of inputs Inception 299| efficentNet 244')

    # Models (general)
    parser.add_argument('--model', default='convNeXtBase', type=str, help='( inceptionV3 | ConvNeXtBase | resnext | densenet)')
    parser.add_argument('--manual_seed', default=1, type=int, help='Manually set random seed')

    # Optimization
    parser.add_argument('--early_stopping_patience', default=10, type=int, help='Early stopping patience (number of epochs)')
    parser.add_argument('--batch_size', default=64, type=int, help='Batch Size')
    parser.add_argument('--num_epochs', default=1000, type=int, help='Number of epochs to train for')
    parser.add_argument('--learning_rate', default=0.001, type=float, help='Initial learning rate (divided by 10 while training by lr-scheduler)')    
    
    #Misc
    parser.add_argument('--device', default='0',type=str, help='GPU device string number 0|1,2')
    parser.add_argument('--server_ip', default='http://000.000.000.000/dataset/', type=str, help='Server IP address')
    parser.add_argument('--category', default='Soccer',type=str, help='Video genre | Soccer | Baseketball | Boxing | Baseball | Cricket | Tennis')
    
    return parser.parse_args()
