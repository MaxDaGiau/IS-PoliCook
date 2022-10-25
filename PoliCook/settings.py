import base64
with open("static/images/default_profile_picture.png", "rb") as f:
    data = f.read()

DEFAULT_PROFILE_PICTURE = base64.b64encode(data).decode('ascii')