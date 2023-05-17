from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import datetime
import pytz
from django.core.files.storage import FileSystemStorage
import cv2
from objectDetection import apiTextDetection
import json
from .models import BCaptcha


def home(request):
    captchas = BCaptcha.objects.all()
    context = {"captchas": captchas}
    return render(request, "home.html", context)


def objectDetection(request):
    return render(request, "objectDetection.html")


def textDetection(request):
    return render(request, "textDetection.html")


def googleTextDetection(request):
    return render(request, "APITextDetection.html")


def voiceDetection(request):
    return render(request, "voiceDetection.html")


# Define new_filename as public variable
new_filename = ""
Username = ""


@csrf_exempt
def uploadFile(request):
    global new_filename, Username  # Declare new_filename as a global variable
    if request.method == "POST":
        uploaded_file = request.FILES["file"]
        print(uploaded_file.name)
        print(uploaded_file.size)
        Username = request.user.username
        # replace with your timezone
        local_tz = pytz.timezone("Australia/Sydney")
        date = datetime.datetime.now(local_tz).strftime("%Y-%m-%d_%H-%M-%S")
        filename, file_extension = os.path.splitext(uploaded_file.name)
        new_filename = f"{Username}_{date}{file_extension}"
        print(new_filename)
        # Do something with the uploaded file here, e.g. save it to a folder or database
        fs = FileSystemStorage()
        fs.save(new_filename, uploaded_file)
        # Load the image using OpenCV

        return HttpResponse(status=200)


def APITextDetection(request):
    if request.method == "GET":
        # Load the image using OpenCV
        imagePath = f"../BreakingCaptcha/media/{new_filename}"
        print("imagePath", imagePath)
        image = cv2.imread(imagePath)

        # Pass the image to the detect_document function
        data = apiTextDetection.detect_document(image)
        print(Username, new_filename, data)

        comment = BCaptcha.create(
            username=Username,
            image_path=new_filename,
            text_solution=data,
            stars_rate=0,
            comments="null",
        )

        create_BC_id = comment.id
        print("id: ", create_BC_id)
        # Return the result as a JSON response
        response_data = {"id": create_BC_id, "data": data}
        return JsonResponse(response_data, status=200, safe=False)


def commentUpdate(request):
    if request.method == "POST":
        data = json.load(request)
        id = data.get("comment_id")
        stRating = data.get("stRating")
        comment = data.get("comment")
        updateComment = BCaptcha.objects.get(pk=id)
        updateComment.stars_rate = stRating
        updateComment.comments = comment
        updateComment.save()
        print("Updated comment:")
        print("ID:", updateComment.username)
        print("Rating:", updateComment.stars_rate)
        print("Comment:", updateComment.comments)
        return HttpResponse(status=200)
