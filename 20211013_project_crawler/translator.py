from googletrans import Translator

# text="測試"
text=['步行到Dongholi', '公車 開往양양고속시외버스터미널', '步行到襄阳长途综合客运站', '公車 開往江陵长途汽车客运站', '步行到강릉시외.고속터미널', '公車 開往江门', '步行到898-18 Ponam 1(il)-dong, Gangneung, Gangwon-do, 南韓']
text2 = '양양고속시외버스터미널'
translator = Translator()
for texts in text:
    de = translator.detect(texts)
    result2 = translator.translate(text2,src='ko', dest='en').text
    # result = translator.translate(texts,src='zh-cn', dest='zh-tw').text
    # result2 = translator.translate(result,src='ko', dest='zh-cn').text
    print(result2)
    