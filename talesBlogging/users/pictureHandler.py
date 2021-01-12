import os
from PIL import Image
from flask import url_for, current_app

def addProfilePic(picUpload, username):

    fileName = picUpload.filename
    extension = fileName.split(".")[-1]
    storageFileName = str(username) + "." + extension

    filePath = os.path.join(current_app.root_path, "static/profilePics", storageFileName)

    outputSize = (200, 200)

    pic = Image.open(picUpload)
    pic.thumbnail(outputSize)
    pic.save(filePath)

    return storageFileName
