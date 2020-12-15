from django.apps import AppConfig
from ai.my_yolo import YOLO

class pre_yolo(AppConfig):
    name = 'my_yolo_app'

    print('hello')
    model_path = 'ai/000/trained_weights_final.h5'
    class_path = 'ai/_classes.txt'
    yolo = YOLO(model_path=model_path, classes_path=class_path)
    print(yolo)

