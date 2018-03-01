
# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

classifier = Sequential()
#Для тензорфлоу входной формат 64, 64, 3. Для Theano наоборот - 3, 64, 64.
#сверточных слоев может быть больше
classifier.add(Conv2D(32, (3, 3), activation="relu", input_shape=(64, 64, 3)))
classifier.add(MaxPooling2D(pool_size=(2 ,2)))

#второй сверточный слой
classifier.add(Conv2D(32, (3, 3), activation="relu"))
classifier.add(MaxPooling2D(pool_size=(2 ,2)))

##третий сверточный слой - детекторов вдвое больше. И так далее
#classifier.add(Conv2D(64, (3, 3), activation="relu"))
#classifier.add(MaxPooling2D(pool_size=(2 ,2)))

classifier.add(Flatten())
#полные слои - 128 нод для такого кол-ва сверток норм
classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=1, activation='sigmoid'))
#компилияция
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics = ['accuracy'])

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
        'dataset/training_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

test_set = test_datagen.flow_from_directory(
        'dataset/test_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

classifier.fit_generator(
        training_set,
        steps_per_epoch=8000, #кол-во картинок на тренировку
        epochs=2,
        validation_data=test_set,
        validation_steps=2000) #картинок на валидацию

classifier.save('classifier1.h5')


