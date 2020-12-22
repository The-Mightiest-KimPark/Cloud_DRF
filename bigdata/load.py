from django.apps import AppConfig
from .models import IntentModel, Preprocess

class pre_intent(AppConfig):
    name = 'my_intent_app'

    model_path = './bigdata/chatbot/intent_model_21.h5'
    p = Preprocess(word2index_dic='./bigdata/chatbot/chatbot_dict_21.bin', userdic='./bigdata/chatbot/user_dic_v1.tsv')
    intent = IntentModel(model_name='./bigdata/chatbot/intent_model_21.h5', proprocess=p)
    print('pre_intent 실행중')