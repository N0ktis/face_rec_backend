from .face_recognition_driver import get_encodings
from .models import User,TimeTracking


def get_image():
    pass


def compare(img):
    input_encodings = get_encodings(img)
    users = User.objects.all().values_list('avatar_encodings')





