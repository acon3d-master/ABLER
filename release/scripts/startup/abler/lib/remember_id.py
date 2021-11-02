import bpy, pickle, os


path = bpy.utils.resource_path("USER")
path_cookiesFolder = os.path.join(path, "cookies")
path_cookiesID = os.path.join(path_cookiesFolder, "userID")  #'userID'에 저장
path_cookiescheck = os.path.join(path_cookiesFolder, "checkbox")


def remember_id(username):

    cookiesID = open(path_cookiesID, "wb")
    pickle.dump(username, cookiesID)  # username을 파일에 저장
    cookiesID.close()


def read_remembered_id():
    if os.path.isfile(path_cookiesID):  # 파일이 있는지 없는지 확인
        with open(path_cookiesID, "rb") as fr:
            data = pickle.load(fr)
        return data
    else:
        return ""


def remember_checkbox(remember_username):

    cookiescheck = open(path_cookiescheck, "wb")
    pickle.dump(remember_username, cookiescheck)  # 체크박스 상태를 파일에 저장
    cookiescheck.close()


def read_remembered_checkbox():
    if os.path.isfile(path_cookiescheck):  # 파일이 있는지 없는지 확인
        with open(path_cookiescheck, "rb") as fr:
            data = pickle.load(fr)
        return data
    else:
        return True  # 파일이 없을때(맨 처음 시작시) 체크박스 켜진 상태로
