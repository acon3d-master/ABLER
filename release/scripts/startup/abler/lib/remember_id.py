import bpy, pickle, os


path = bpy.utils.resource_path("USER")
path_cookiesFolder = os.path.join(path, "cookies")
path_cookiesID = os.path.join(path_cookiesFolder, "userID")


def remember_id(username):

    cookiesID = open(path_cookiesID, "wb")
    pickle.dump(username, cookiesID)
    cookiesID.close()


def read_remembered_id():
    if os.path.isfile(path_cookiesID):
        with open(path_cookiesID, "rb") as fr:
            data = pickle.load(fr)
        return data
    else:
        return ""


def delete_remembered_id():
    if os.path.isfile(path_cookiesID):
        os.remove(path_cookiesID)


def read_remembered_checkbox():
    if os.path.isfile(path_cookiesID):
        return True
    else:
        return False
