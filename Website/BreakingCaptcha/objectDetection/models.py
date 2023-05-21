from django.db import models


class BCaptcha(models.Model):
    username = models.CharField(max_length=100)
    image_path = models.CharField(max_length=200)
    text_solution = models.TextField()
    stars_rate = models.DecimalField(max_digits=2, decimal_places=1)
    comments = models.TextField()

    @classmethod
    def create(cls, username, image_path, text_solution, stars_rate, comments):
        text_detection = cls(
            username=username,
            image_path=image_path,
            text_solution=text_solution,
            stars_rate=stars_rate,
            comments=comments,
        )
        text_detection.save()
        return text_detection
