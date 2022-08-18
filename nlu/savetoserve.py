from tensorflow.keras.models import load_model
model = load_model('nlu\models\model.h5')
model.save('nlu\models\savedmodels\\2', save_format='tf')
