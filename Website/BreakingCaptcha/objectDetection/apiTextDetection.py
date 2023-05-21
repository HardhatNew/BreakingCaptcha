import cv2
import os

credential_path = os.path.abspath("objectDetection/credentials.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path


def detect_document(image):
    print("image", image)
    """Detects document features in an image."""
    from google.cloud import vision
    import io

    client = vision.ImageAnnotatorClient()

    # Convert the NumPy array to bytes
    img_bytes = cv2.imencode(".jpg", image)[1].tobytes()

    # Create an image object from the bytes
    image = vision.Image(content=img_bytes)

    response = client.document_text_detection(image=image)
    # Extract the first text annotation
    all_text = ""  # Initialize all_text to empty string
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print("\nBlock confidence: {}\n".format(block.confidence))

            for paragraph in block.paragraphs:
                print("Paragraph confidence: {}".format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    all_text += word_text + " "
                    # append the word_text to the variable and add a space after it

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    # print the final text variable
    return all_text


# image = cv2.imread("../media/2.png")

# # Pass the image to the detect_document function
# data = detect_document(image)
# print("data =", data)
