import cv2
import typing
import numpy as np
import os
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder, get_cer
from mltu.configs import BaseModelConfigs


class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shape[:2][::-1])

        image = image.astype(np.float32)  # Convert to float type

        image_pred = np.expand_dims(image, axis=0)

        preds = self.model.run(None, {self.input_name: image_pred})[0]

        text = ctc_decoder(preds, self.char_list)[0]

        return text


def breakingCaptcha(imagePath):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    model_dir = os.path.join(parent_dir, "captcha/model")
    model_path = os.path.join(model_dir, "model.onnx")

    if not os.path.exists(model_path):
        raise Exception(f"Model file ({model_path}) does not exist")

    model_configs = BaseModelConfigs.load(os.path.join(model_dir, "configs.yaml"))

    model = ImageToWordModel(model_path=model_path, char_list=model_configs.vocab)
    # /Users/as_alkinani/Downloads/Learning/Masyter Cyber Security/TeamProject B/website/BreakingCapthca/BreakingCaptchanew/media/_2023-05-09_22-03-22.png
    image_path = model_dir = os.path.join(parent_dir, imagePath)
    # Load the image
    if not os.path.exists(image_path):
        raise Exception(f"Image file ({image_path}) does not exist")
    image = cv2.imread(image_path)
    label = image_path.split("/")[-1].split(".")[0]  # Extract label from image path
    prediction_text = model.predict(image)

    print(f"Prediction: {prediction_text}")
    return prediction_text
