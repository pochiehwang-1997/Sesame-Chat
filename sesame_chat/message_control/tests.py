from rest_framework.test import APITestCase
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from six import BytesIO
from PIL import Image

# Create your tests here.
def create_image(storage, filename, size=(100,100), image_mode="RGB", image_format="PNG"):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

class TestFileUpload(APITestCase):
    file_upload_url = "/message/file-upload"

    def test_file_upload(self):
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file,
        }

        response = self.client.post(self.file_upload_url, data=data)
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["id"], 1)

class TestMessage(APITestCase):
    message_url = "/message/message"
    login_url = "/user/login"

    def setUp(self):
        from user_control.models import CustomUser, UserProfile

        # sender
        payload = {"username":"sender", "password":"sender123", "email":"sender@gmail.com"}
        self.sender = CustomUser.objects._create_user(**payload)
        UserProfile.objects.create(first_name="sender", user=self.sender, caption="sender", about="sender")
        response = self.client.post(self.login_url, data=payload)
        result = response.json()
        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}
        # receiver
        self.receiver = CustomUser.objects._create_user("receiver", "receiver123", "receiver@gmail.com")
        UserProfile.objects.create(first_name="receiver", user=self.receiver, caption="receiver", about="receiver")
    
    def test_post_message(self):
        payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "test message"
        }

        # processing
        response = self.client.post(self.message_url, data=payload, **self.bearer)
        result = response.json()

        # assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["message"], "test message")
        self.assertEqual(result["sender"]["user"]["username"], "sender")
        self.assertEqual(result["receiver"]["user"]["username"], "receiver")
    
    def test_get_message(self):

        response = self.client.get(self.message_url+f"?user_id={self.receiver.id}", **self.bearer)
        result = response.json()

        self.assertEqual(response.status_code, 200)
