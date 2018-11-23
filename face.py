import base64
import requests
import simplejson
from json import JSONDecoder



key = "FM-iEHF0gNjCtVRgzO8r5Tlts4dSwAad"
secret = "his7nm8xyDAL15atNqcPHVDomR5Axo1Z"

def face(path):
    print("finding")
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key": key, "api_secret": secret, "image_url": path, "return_landmark": 1}
    files = {"image_file": open(path, "rb")}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)

    this_json = simplejson.dumps(req_dict)
    this_json2 = simplejson.loads(this_json)

    faces = this_json2['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']

    return rectangle

# 模板图片地址 合成图片地址 生成图片地址 合成指数0-100
def add(img1,img2,img_url,number):

    ff1 = face(img1)
    ff2 = face(img2)

    rectangle1 = str(str(ff1['top']) + ","
                     + str(ff1['left']) + "," + str(ff1['width']) +
                     "," + str(ff1['height']))
    rectangle2 = str(ff2['top']) + "," + str(ff2['left']) + \
                 "," + str(ff2['width']) + "," + str(ff2['height'])


    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"

    f1 = open(img1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(img2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()
    data = {"api_key": key, "api_secret": secret,
            "template_base64": f1_64,
            "template_rectangle": rectangle1,
            "merge_base64": f2_64, "merge_rectangle": rectangle2,
            "merge_rate": number}

    response = requests.post(url_add, data=data)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    print(req_dict)

    result = req_dict['result']
    imgdata = base64.b64decode(result)
    file = open(img_url, 'wb')
    file.write(imgdata)
    file.close()

def add_many(list_face):

    print("正在合成第1-2张")
    image_now = r'1.jpg'
    add(list_face[0], list_face[1], image_now, 50)

    for index in range(2,len(list_face)):
        print("正在合成第"+str(index+1)+"张")
        add(image_now, list_face[index], image_now, 50)

# 单独两张照片的合成示例

img1 = r"7.jpg"
img2 = r"1.jpg"
img_url = r'result.jpg'
add(img1,img2,img_url,50)

# 多张照片合成的示例
#
# list = []
# list.append(r"1.jpg")
# list.append(r"2.jpg")
# list.append(r"3.jpg")
# list.append(r"4.jpg")
# add_many(list)



#参考链接https://console.faceplusplus.com.cn/documents/5672647
#https://blog.csdn.net/u014365862/article/details/74149097