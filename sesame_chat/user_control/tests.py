from rest_framework.test import APITestCase
from .models import CustomUser, UserProfile
from .views import get_access_token, get_random, get_refresh_token
from message_control.tests import create_image, SimpleUploadedFile


class TestGenericFunctions(APITestCase):

    def test_get_random(self):
        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)
        self.assertTrue(rand1)
        self.assertNotEqual(rand1, rand2)
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):
        payload = {"id": 1}
        token = get_access_token(payload)
        self.assertTrue(token)

    def test_get_refresh_token(self):
        token = get_refresh_token()
        self.assertTrue(token)


class TestAuth(APITestCase):

    login_url = "/user/login"
    refresh_url = "/user/refresh"
    register_url = "/user/register"

    def test_register(self):
        payload = {
            "username": "pochiehhh",
            "password": "Sesamechat922!",
            "email": "pochieh0727@gmail.com"
        }
        response = self.client.post(self.register_url, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], "User created.")

    def test_login(self):
        payload = {
            "username": "pochiehhh",
            "password": "Sesamechat922!",
            "email": "pochieh0727@gmail.com"
        }
        self.client.post(self.register_url, data=payload)
        response = self.client.post(self.login_url, data=payload)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):

        payload = {
            "username": "pochiehhh",
            "password": "Sesamechat922!",
            "email": "pochieh0727@gmail.com"
        }
        self.client.post(self.register_url, data=payload)
        response = self.client.post(self.refresh_url, data=payload)
        result = response.json()
        self.assertTrue(result["refresh"])


class TestUserProfile(APITestCase):
    profile_url = "/user/profile"
    file_upload_url = "/message/file-upload"
    login_url = "/user/login"

    def setUp(self):
        payload = {
            "username": "cammy",
            "password": "Cammy922!",
            "email": "cammy922@gmail.com"
        }

        self.user = CustomUser.objects._create_user(**payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}

    def test_post_user_profile(self):

        payload = {
            "user_id": self.user.id,
            "first_name": "Cammy",
            "last_name": "Lee",
            "caption": "All I wanna do is eating and sleeping",
            "about": "Life is hard, so just go to bed"
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Cammy")

    def test_post_user_profile_with_profile_picture(self):

        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file,
        }

        image_response = self.client.post(self.file_upload_url, data=data)
        image_result = image_response.json()

        payload = {
            "user_id": self.user.id,
            "first_name": "Cammy",
            "last_name": "Lee",
            "caption": "All I wanna do is eating and sleeping",
            "about": "Life is hard, so just go to bed",
            "profile_picture_id": image_result["id"]
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Cammy")
        self.assertEqual(result["profile_picture"]["id"], image_result["id"])

    def test_update_user_profile(self):
        # Create user

        payload = {
            "user_id": self.user.id,
            "first_name": "Cammy",
            "last_name": "Lee",
            "caption": "All I wanna do is eating and sleeping",
            "about": "Life is hard, so just go to bed"
        }

        create_result = self.client.post(
            self.profile_url, data=payload, **self.bearer).json()

        payload = {
            "user_id": self.user.id,
            "first_name": "Yi-Chen",
            "last_name": "Lee",
            "caption": "I am hungry",
            "about": "Give me food!"
        }

        response = self.client.patch(
            self.profile_url+"/%s" % create_result["id"], data=payload, **self.bearer)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["first_name"], "Yi-Chen")

    # def test_user_search(self):
    #     UserProfile.objects.create(user=self.user, first_name="Cammy", last_name="Lee",
    #                                caption="All I wanna do is eating and sleeping", about="Life is hard, so just go to bed")
    #     tester = CustomUser.objects._create_user(
    #         username="tester", password="Tester922!", email="tester@gmail.com")
    #     UserProfile.objects.create(user=tester, first_name="Tester", last_name="No1",
    #                                caption="All I wanna do is eating and sleeping", about="Life is hard, so just go to bed")

    #     url = self.profile_url + "?keyword=Lee"

    #     response = self.client.get(url, **self.bearer)
    #     print(response.json())
    #     result = response.json()["results"]

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(result), 1)
    #     self.assertEqual(result[0]["user"]["username"], "cammy")
    #     self.assertEqual(result[0]["message_count"], 0)
