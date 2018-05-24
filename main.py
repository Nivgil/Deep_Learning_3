from keras import Sequential
from keras.layers import Dense, Conv2D, BatchNormalization, Activation, AveragePooling2D, Flatten
from keras.datasets import mnist, cifar10
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import LearningRateScheduler
import keras

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

model = Sequential()

model.add(Conv2D(16, kernel_size=3, input_shape=x_train.shape[1:], use_bias=False, strides=(1, 1), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(32, kernel_size=3, use_bias=False, strides=(2, 2), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(32, kernel_size=3, use_bias=False, strides=(1, 1), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(32, kernel_size=3, use_bias=False, strides=(1, 1), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(64, kernel_size=3, use_bias=False, strides=(2, 2), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(AveragePooling2D((8, 8)))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))

sgd = keras.optimizers.SGD(lr=0.1, decay=5e-4, momentum=0.9, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['acc'])

model.summary()


datagen = ImageDataGenerator(
    featurewise_center=True,  # set input mean to 0 over the dataset
    samplewise_center=False,  # set each sample mean to 0
    featurewise_std_normalization=True,  # divide inputs by std of the dataset
    samplewise_std_normalization=False,  # divide each input by its std
    zca_whitening=False,  # apply ZCA whitening
    rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
    width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
    height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
    horizontal_flip=True,  # randomly flip images
    vertical_flip=False)  # randomly flip images

# Compute quantities required for feature-wise normalization
# (std, mean, and principal components if ZCA whitening is applied).
datagen.fit(x_train)


lr_cb = LearningRateScheduler(lambda epoch: 0.1 ** (epoch < 60 and 1 or
                                                    epoch < 120 and 2 or
                                                    epoch < 160 and 3 or
                                                    4))
# Fit the model on the batches generated by datagen.flow().
model.fit_generator(datagen.flow(x_train, y_train, batch_size=128), epochs=200, validation_data=(x_test, y_test),
                    workers=4, callbacks=[lr_cb])