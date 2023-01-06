
from fastapi import APIRouter, File, UploadFile
import tensorflow as tf
from tensorflow import keras
import pickle
import uuid


img_model_router = APIRouter(
    prefix='/img',
    tags=['img_model']
)

# Alex net
pickle_a = open("alex.pickle", "rb")
classifier_alex = pickle.load(pickle_a)
IMAGE_SIZE_A = [227, 227]


@img_model_router.post("/predict-alex/")
async def create_file(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    with open(file.filename, "wb") as f:
        f.write(contents)
    img = keras.preprocessing.image.load_img(
        file.filename, target_size=IMAGE_SIZE_A
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)
    prediction = classifier_alex.predict(img_array)
    label_dict = {0: "building", 1: "forest",
                  2: "glacier", 3: "mountain", 4: "sea", 5: "street"}
    for i in range(len(prediction[0])):
        if prediction[0][i] == max(prediction[0]):
            return {"label ": label_dict[i]}


# VGG 16
pickle_v = open("vgg16.pickle", "rb")
classifier_vgg = pickle.load(pickle_v)
IMAGE_SIZE_V = [64, 64]


@img_model_router.post("/predict-vgg16/")
async def create_file(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    with open(file.filename, "wb") as f:
        f.write(contents)
    img = keras.preprocessing.image.load_img(
        file.filename, target_size=IMAGE_SIZE_V
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)
    prediction = classifier_vgg.predict(img_array)
    label_dict = {0: "building", 1: "forest",
                  2: "glacier", 3: "mountain", 4: "sea", 5: "street"}
    for i in range(len(prediction[0])):
        if prediction[0][i] == max(prediction[0]):
            return {"label ": label_dict[i]}
