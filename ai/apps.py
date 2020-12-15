from django.apps import AppConfig

class AiConfig(AppConfig):
    name = 'ai'
    # def ready(self):
    #     from ai.my_yolo import YOLO
    #     print('hello')
    #     model_path = 'ai/000/trained_weights_final.h5'
    #     class_path = 'ai/_classes.txt'
    #     yolo = YOLO(model_path=model_path, classes_path=class_path)
    #     print(yolo)

