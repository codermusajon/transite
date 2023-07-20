from django.shortcuts import render
from django.http import HttpResponse
from .models import Lugat
from deep_translator import GoogleTranslator
import requests
import json



def indexuz(request):
    print(request.GET)
    soz = request.GET.get('q', '')
    if len(soz) != 0:
        #lang = detectlanguage.simple_detect(f"{soz}")
        natija = GoogleTranslator(source='uz', target='en').translate(soz)
        print(soz, natija)
    else:
        natija = ''
        soz = ''
    app_id = '7136a8d2'
    app_key = '42a7d7041c8961b94f919acaa28157ac'
    language = 'en-gb'
    word_id = natija
    url = 'https://od-api.oxforddictionaries.com/api/v2/entries/'  + language + '/'  + word_id.lower()
    r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
    res = r.json()
    print(r.status_code)
    try:
        voice = res["results"][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
        audiom = f'{voice}'
    except:
        audiom = 'audio topilmadi!'

    #if soz and soz != '':
    #    natija = Lugat.objects.filter(inglizcha__contains=soz).all()[:3]
    #else:
    #    natija = None
    lang='uz'


    return render(request, 'index.html', {'q':soz, 'natija': natija, 'qu':soz, 'lang':lang, 'audiom':audiom})

def indexen(request):
    soz = request.GET.get('que', '')
    app_id = '7136a8d2'
    app_key = '42a7d7041c8961b94f919acaa28157ac'
    language = 'en-gb'
    word_id = soz
    url = 'https://od-api.oxforddictionaries.com/api/v2/entries/'  + language + '/'  + word_id.lower()
    r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
    res = r.json()
    print(r.status_code)
    senses = ' '
    voice = ' '
    try:
        voice = res["results"][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
        audiom = f'{voice}'
        output = {}
        senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        definitions = []
        for sense in senses:
            print(f"👉 {senses}")
        #output['definitions'] = "\n".join(definitions)
    except:
        audiom = 'audio not found!'
        senses = [{'constructions': [{'text': 'by car'}], 'definitions': ['definitions not found!']}]
        #senses['definitions'] = ['not found!']

        print(senses)


    if len(soz) != 0:
        natija = GoogleTranslator(source='en', target='uz').translate(soz)
        print(soz, natija)
    else:
        natija = ''
        soz = ''
    lang = 'en'
    return render(request, 'indexen.html', {'q':soz, 'natija': natija, 'qu':soz, 'lang':lang, 'audiom':audiom, 'senses':senses})
