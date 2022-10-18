import json
import jwt
import bcrypt

from django.test import TestCase, Client
from django.conf import settings

from companies.models import Company
from boards.models import Board, Skill, Apply
from users.models import User
from core.models import Region
from core.models import Country

# Create your tests here.
class SignUpViewTest(TestCase):
    def setUp(self):
        korea = Country.objects.create(name = "korea")
        japan = Country.objects.create(name = "japan")
        china = Country.objects.create(name = "china")

        seoul       = Region.objects.create(name = "seoul", country = korea)
        gyeonggi_do = Region.objects.create(name = "gyeonggi_do", country = korea)
        gangwon_do  = Region.objects.create(name = "gangwon_do", country = korea)

        tokyo       = Region.objects.create(name = "tokyo", country = japan)
        kyoto       = Region.objects.create(name = "kyoto", country = japan)
        okinawa     = Region.objects.create(name = "okinawa", country = japan)

        beijing     = Region.objects.create(name = "beijing", country = china)
        shanghai    = Region.objects.create(name = "shanghai", country = china)
        company     = Company.objects.create(id=1, name="naver", password = bcrypt.hashpw("naver12345!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), regions = seoul)
        
    def tearDown(self):
        Country.objects.all().delete()
        Region.objects.all().delete()
        Company.objects.all().delete()
    
    def test_sign_up_success_post(self):
        client = Client()
        data = {
            "name" : "google",
            "password": "google12345!",
            "region" : "kyoto"
        }

        response    = client.post('/companies/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {"message": "success"})
        self.assertEqual(response.status_code, 201)

    def test_sign_up_fail_key_error_post(self):
        client = Client()
        data = {
            "name" : "google",
            "password": "google12345!"
            # "region" : "tokyo"
        }

        response    = client.post('/companies/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {"mssage": "key_error"})
        self.assertEqual(response.status_code, 400)

    def test_sign_up_fail_region_not_exist_post(self):
        client = Client()
        data = {
            "name" : "google",
            "password": "google12345!",
            "region" : "jeju"
        }

        response    = client.post('/companies/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {"message": "region_does_not_exist"})
        self.assertEqual(response.status_code, 400)

    
    def test_sign_up_fail_duplicate_name_post(self):
        client = Client()
        data = {
            "name" : "naver",
            "password": "naver12345!",
            "region" : "seoul"
        }

        response    = client.post('/companies/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {"message": "duplicate_company_name"})
        self.assertEqual(response.status_code, 400)

class SignInViewTest(TestCase):
    def setUp(self):
        korea = Country.objects.create(name = "korea")
        japan = Country.objects.create(name = "japan")
        china = Country.objects.create(name = "china")

        seoul       = Region.objects.create(name = "seoul", country = korea)
        gyeonggi_do = Region.objects.create(name = "gyeonggi_do", country = korea)
        gangwon_do  = Region.objects.create(name = "gangwon_do", country = korea)

        tokyo       = Region.objects.create(name = "tokyo", country = japan)
        kyoto       = Region.objects.create(name = "kyoto", country = japan)
        okinawa     = Region.objects.create(name = "okinawa", country = japan)

        beijing     = Region.objects.create(name = "beijing", country = china)
        shanghai    = Region.objects.create(name = "shanghai", country = china)
        company     = Company.objects.create(id=1, name="naver", password = bcrypt.hashpw("naver12345!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), regions = seoul)
        
    def tearDown(self):
        Country.objects.all().delete()
        Region.objects.all().delete()
        Company.objects.all().delete()
    
    def test_sign_in_success_post(self):
        client = Client()

        body = {
            "name"     : "naver",
            "password"  : "naver12345!"
        }
        
        token = jwt.encode({'id': Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_AUTHORIZATION": token}
        response = client.post('/companies/signin', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(), {"message": "login_success","access_token"  : token})
        self.assertEqual(response.status_code, 200)
    
    def test_sign_in_key_error_post(self):
        client = Client()
        
        body = {
            # "name"     : "naver",
            "password"  : "kim12345!"
        }
        
        token = jwt.encode({'id': Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_AUTHORIZATION": token}
        response = client.post('/companies/signin', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(), {"message": "key_error"})
        self.assertEqual(response.status_code, 400)
    
    def test_sign_in_company_not_exist_post(self):
        client = Client()
        
        body = {
            "name"     : "google",
            "password"  : "google12345!"
        }
        
        token = jwt.encode({'id': Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_AUTHORIZATION": token}
        response = client.post('/companies/signin', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(), {"message": "company_does_not_exist"})
        self.assertEqual(response.status_code, 400)
    
    def test_sign_in_user_password_invalid_post(self):
        client = Client()
        
        body = {
            "name"     : "naver",
            "password"  : "naver12345"
        }
        
        token = jwt.encode({'id': Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_AUTHORIZATION": token}
        response = client.post('/companies/signin', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(), {"message": "invaild_user"})
        self.assertEqual(response.status_code, 400)

class BoardListViewTest(TestCase):
    def setUp(self):
        korea = Country.objects.create(id = 1, name = "korea")
        japan = Country.objects.create(id = 2, name = "japan")
        china = Country.objects.create(id = 3, name = "china")

        seoul       = Region.objects.create(id = 1, name = "seoul", country = korea)
        gyeonggi_do = Region.objects.create(id = 2, name = "gyeonggi_do", country = korea)
        gangwon_do  = Region.objects.create(id = 3, name = "gangwon_do", country = korea)

        tokyo       = Region.objects.create(id = 4, name = "tokyo", country = japan)
        kyoto       = Region.objects.create(id = 5, name = "kyoto", country = japan)
        okinawa     = Region.objects.create(id = 6, name = "okinawa", country = japan)

        beijing     = Region.objects.create(id = 7, name = "beijing", country = china)
        shanghai    = Region.objects.create(id = 8, name = "shanghai", country = china)

        skillpython = Skill.objects.create(id= 1, name ="python")
        skilljava   = Skill.objects.create(id= 2, name ="java")

        naver       = Company.objects.create(id=1, name="naver", password = bcrypt.hashpw("naver12345!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), regions = seoul)
        board       = Board.objects.create(id = 1, company = naver, money = 100000, descrtption = "네이버구직", position = "master")
        board2       = Board.objects.create(id = 2, company = naver, money = 200000, descrtption = "네이버구직2", position = "junior")

        board.skills.add(skilljava)
        board.skills.add(skillpython)
        board2.skills.add(skilljava)
        

        
    def tearDown(self):
        Country.objects.all().delete()
        Region.objects.all().delete()
        Board.objects.all().delete()
        Skill.objects.all().delete()
        Company.objects.all().delete()
     
    def test_show_boardlist_success_get(self):
        client = Client()
        
        token       = jwt.encode({'id': Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        response    = client.get('/companies/boardlist', **headers, content_type='application/json')

        body =  {
                "result" :[
                {
                    "채용공고_id"       : 1
                },
                {
                    "채용공고_id"       :2
                }
                ]
            }
        self.assertEqual(response.json(), body)
        self.assertEqual(response.status_code, 200)