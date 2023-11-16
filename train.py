from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard, CSVLogger, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

from config import parse_opts
from utils.lib_ucf import UCFDataSet
from utils.lib_createDir import prepare_output_dirs, print_config, write_config
from utils.lib_visdata import save_history
from models.convNeXt import create_model

# Parse configurations
config = parse_opts()
config = prepare_output_dirs(config)

# Display and write config
print_config(config)
write_config(config, os.path.join(config.save_dir, 'config.json'))

# Set CUDA environment variables
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = config.device

# Load UCF data
ucf_dataset = UCFDataSet()

# Callbacks for training
model_checkpoint = ModelCheckpoint(
    filepath=os.path.join(config.checkpoint_dir, '{epoch:03d}-{val_loss:.2f}.hdf5'),
    verbose=1,
    save_best_only=True)

csv_logger = CSVLogger(os.path.join(config.log_dir, 'training.log'))

early_stopping = EarlyStopping(patience=config.early_stopping_patience)

tensorboard = TensorBoard(log_dir=config.log_dir)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

# Define train and test directories
train_directory = os.path.join(config.dataset_path, 'train/')
test_directory = os.path.join(config.dataset_path, 'test/')

# Data generators
def get_data_generators():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        rotation_range=30.,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_directory,
        target_size=(config.spatial_size, config.spatial_size),
        color_mode='rgb',
        classes=ucf_dataset.classes,
        batch_size=config.batch_size)

    validation_generator = test_datagen.flow_from_directory(
        test_directory,
        target_size=(config.spatial_size, config.spatial_size),
        color_mode='rgb',
        classes=ucf_dataset.classes,
        batch_size=config.batch_size)

    return train_generator, validation_generator

if __name__ == "__main__":
    # Create and display model summary
    model = create_model(
        img_size=config.spatial_size,
        num_classes=config.num_classes,
        learning_rate=config.learning_rate,
        show_summary=True)
    print('\nModel created...\n')

    # Get data generators
    generators = get_data_generators()
    train_data_generator, validation_data_generator = generators

    # Model training
    history = model.fit(
        train_data_generator,
        steps_per_epoch=100,
        validation_data=validation_data_generator,
        validation_steps=10,
        epochs=config.num_epochs,
        workers=4,
        callbacks=[model_checkpoint, early_stopping, tensorboard, csv_logger, reduce_lr])

    # Save the final model and training history visualization
    model.save(os.path.join(config.save_dir, 'final_model.h5'))
    save_history(history, os.path.join(config.save_dir, 'evaluate.png'))
