# import the necessary packages
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications import Xception  # TensorFlow ONLY
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("--model", "--model", type=str, default="vgg16",
                help="name of the pre-trained network to use")
ap.add_argument("-o", "--output", type=str, help="path to the output image")
args = vars(ap.parse_args())


# define a dictionary that maps model names to their classes
# inside Keras

MODELS = {
    "vgg16": VGG16,
    "vgg19": VGG19,
    "inception": InceptionV3,
    "xception": Xception,
    "resnet": ResNet50
}

# ensure a valid model name was supplied via command line argument
if args["model"] not in MODELS.keys():
    raise AssertionError(
        "The --model command line argument should be a key in the 'MODELS' dictionary")


# initialize the input image shape (224x224 pixels) along with
# the preprocessing function (this might need to be changed
# based on which model we use to calssify our image)
inputShape = (224, 224)
preprocess = imagenet_utils.preprocess_input

# if we are using the inceptionV3 or Xception networks,
# then we need to set the input shape to (299x299) [rather than (224x224)]
# and use a different image pre-processing function
if args["model"] in ("inception", "xception"):
    inputShape = (299, 299)
    preprocess = preprocess_input


# load our network weights from the disk
print("[INFO] loading {}...".format(args["model"]))
Network = MODELS[args["model"]]
model = Network(weights="imagenet")

# load the input image using the Keras helper utility while ensuring
# the image is resized to 'inputShape', the required input dimensions
# for the imageNet pre=trained network
print("[INFO] loading and pre-processing image...")
image = load_img(args["image"], target_size=inputShape)
image = img_to_array(image)

# our input image is now represented as a NumPy array of shape
# (inputShape[0], inputShape[1], 3) however we need to expand the
# dimension by making the shape (1, inputShape[0], inputShape[1], 3)
# so we can pass it through the network
image = np.expand_dims(image, axis=0)

# pre-process the image using the appropriate function based on
# the model that has been loaded (i.e., mean subtraction, scaling, etc.)
image = preprocess(image)

# classify the image
print("[INFO] classifying image with '{}'...".format(args["model"]))
preds = model.predict(image)
p = imagenet_utils.decode_predictions(preds)

# loop over the predictions and display the rank-5 predictions +
# probabilities to our terminal
# Also load the image via openCV, draw the top prediction on the image,
# and display the image to our screen
orig = cv2.imread(args["image"])

cv2.putText(orig, "Model: {}".format(args["model"]), (20, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)


x, y = 20, 60


for (i, (imagenetID, label, prob)) in enumerate(p[0]):
    print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))
    (imagenetID, label, prob) = p[0][i]
    text = "{}. {}: {:.2f}%\n".format(
        i+1, label, prob * 100)

    for j, line in enumerate(text.split('\n')):
        cv2.putText(orig, line, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    y = y + 30


# Saving the image if the output argument is passed
if args["output"]:
    cv2.imwrite(args["output"], orig)

cv2.imshow("Classification", orig)
cv2.waitKey(0)