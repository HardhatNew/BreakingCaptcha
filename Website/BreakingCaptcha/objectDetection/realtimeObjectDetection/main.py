import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from gtts import gTTS
from playsound import playsound

video = cv2.VideoCapture(1)
labels = []
confidences = []
while True:
    ret, frame = video.read()

    # Check if frame was read successfully
    if not ret:
        video = cv2.VideoCapture(0)
        ret, frame = video.read()

    bbox, label, conf = cv.detect_common_objects(frame)

    # Check if objects were detected
    if label:
        output_image = draw_bbox(frame, bbox, label, conf)

        for i in range(len(label)):
            if label[i] not in labels and conf[i] > 0.85:
                labels.append(label[i])
                confidences.append(conf[i])
                label_text = f"{label[i]}: {conf[i]:.2f}"
                cv2.putText(
                    output_image,
                    label_text,
                    (bbox[i][0], bbox[i][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

                tts = gTTS(text=label[i], lang="en")
                tts.save("output.mp3")
                playsound("output.mp3")

        cv2.imshow("Object Detection", output_image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()

for i in range(len(labels)):
    print(f"detect_{i+1}: {labels[i]}, Confidence: {confidences[i]:.2f}")
