import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation, GlobalAveragePooling2D
from tensorflow.keras.optimizers import  SGD

from modules.vortexPooling import vortex_pooling
from modules.tripletAttention import TripletAttention

def create_model(img_size =224, num_classes =101, learning_rate = 0.001, show_summary = False):
    base_model = tf.keras.applications.ConvNeXtBase(
                                model_name='convnext_base',
                                include_top=False,
                                include_preprocessing=False,
                                weights='imagenet',
                                input_tensor=None,
                                input_shape=(img_size,img_size, 3),
                                pooling=None,
                                classes=num_classes,
                                classifier_activation='softmax')

    # last_output = base_model.output
    last_output = base_model.get_layer('tf.__operators__.add_35').output
      
    tripAtt = TripletAttention()
    trip_layer = tripAtt.forward(last_output)

    layer1 = GlobalAveragePooling2D(name="avg_pool")(trip_layer)

    # Rebuild top    
    layer1 = Dense(512, activation='relu')(layer1)
    layer1 = Dropout(0.2)(layer1)

    layer2 = Dense(512) (layer1)
    layer2 = BatchNormalization() (layer2)
    layer2 = Activation("relu") (layer2)
    layer2 = Dropout(rate = 0.2 ) (layer2)

    predictions = Dense(num_classes, activation='softmax', name="classifier")(layer2)

    # Compile
    model = tf.keras.Model(base_model.input, predictions)

    optimizer = SGD(learning_rate)
    model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["acc"])
    
    if show_summary:
        model.summary()
    return model