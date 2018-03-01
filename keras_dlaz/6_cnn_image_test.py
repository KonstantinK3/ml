import numpy as np
from keras.preprocessing import image
from keras.models import load_model
classifier = load_model('classifier.h5')

def dogcat(image_name):
    image_name = 'dataset/sp2/' + image_name
    test_image = image.load_img(image_name, target_size = (64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    predict = classifier.predict(test_image)
    if predict[0,0] == 1:
        return 'dog'
    else:
        return 'cat'

for i in range(1,13):
    print ("image {} is a {}".format(i, dogcat(str(i)+'.jpg')))

    


