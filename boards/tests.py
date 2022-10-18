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

class BoardViewTest(TestCase):
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
     
    def test_success_create_board_post(self):
        client = Client()
        
        token       = jwt.encode({'id': Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        body =  {
                "money"         :10000,
                "descrtption"   :"test설명",
                "position"      : "master",
                "skills"         : ["java"]
            }
        
        response    = client.post('/boards',  json.dumps(body), content_type='application/json', **headers)

       
        self.assertEqual(response.json(),{"message":"SUCCESS"} )
        self.assertEqual(response.status_code, 201)
    
    def test_fail_create_board_key_error_post(self):
        client = Client()

        token   = jwt.encode({'id':Company.objects.get(id= 1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        body =  {
                "money"         :10000,
                "descrtption"   :"test설명",
                # "position"      : "master",
                "skills"         : ["java"]
            }
        
        response    = client.post('/boards',  json.dumps(body), content_type='application/json', **headers)

       
        self.assertEqual(response.json(),{"mssage":"key_error"} )
        self.assertEqual(response.status_code, 400)
    
    def test_fail_create_board_skills_not_exist_post(self):
        client = Client()

        token   = jwt.encode({'id':Company.objects.get(id= 1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        body =  {
                "money"         :10000,
                "descrtption"   :"test설명",
                "position"      : "master",
                "skills"         : ["kotlin"]
            }
        
        response    = client.post('/boards',  json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"skill_does_not_exist"} )
        self.assertEqual(response.status_code, 400)
    
    def test_success_show_all_board_get(self):
        client = Client()

        response = client.get('/boards', content_type='application/json')

        body = {
            "result": [{
                "채용공고_id"     : 1,
                "회사_id"        : 1,
                "회사_이름"       : "naver",
                "채용포지션"       : "master",
                "채용보상금"       : 100000,
                "채용내용"        : "네이버구직",
                "사용기술"        : ["python","java"]
            },
            {
                "채용공고_id"     : 2,
                "회사_id"        : 1,
                "회사_이름"       : "naver",
                "채용포지션"       : "junior",
                "채용보상금"       : 200000,
                "채용내용"        : "네이버구직2",
                "사용기술" :["java"]
            }
            ]
        }

        self.assertEqual(response.json(),body)
        self.assertEqual(response.status_code, 200)

    def test_success_show_search_skill_board_get(self):
        client = Client()

        response = client.get('/boards?search=python', content_type='application/json')

        body = {
            "result": [{
                "채용공고_id"     : 1,
                "회사_id"        : 1,
                "회사_이름"       : "naver",
                "채용포지션"       : "master",
                "채용보상금"       : 100000,
                "채용내용"        : "네이버구직",
                "사용기술"        : ["python","java"]
            }
            ]
        }

        self.assertEqual(response.json(),body)
        self.assertEqual(response.status_code, 200)

    def test_success_show_search_comapny_name_board_get(self):
        client = Client()

        response = client.get('/boards?search=google', content_type='application/json')

        body = {
            "result": [
            ]
        }

        self.assertEqual(response.json(),body)
        self.assertEqual(response.status_code, 200)

    def test_success_show_search_position_board_get(self):
        client = Client()

        response = client.get('/boards?search=master', content_type='application/json')

        body = {
            "result": [{
                "채용공고_id"     : 1,
                "회사_id"        : 1,
                "회사_이름"       : "naver",
                "채용포지션"       : "master",
                "채용보상금"       : 100000,
                "채용내용"        : "네이버구직",
                "사용기술"        : ["python","java"]
            }
            ]
        }

        self.assertEqual(response.json(),body)
        self.assertEqual(response.status_code, 200)

    def test_success_show_search_description_board_get(self):
        client = Client()

        response = client.get('/boards?search=네이버', content_type='application/json')

        body = {
            "result": [{
                "채용공고_id"     : 1,
                "회사_id"        : 1,
                "회사_이름"       : "naver",
                "채용포지션"       : "master",
                "채용보상금"       : 100000,
                "채용내용"        : "네이버구직",
                "사용기술"        : ["python","java"]
            },
            {
                "채용공고_id"     : 2,
                "회사_id"        : 1,
                "회사_이름"       : "naver",
                "채용포지션"       : "junior",
                "채용보상금"       : 200000,
                "채용내용"        : "네이버구직2",
                "사용기술" :["java"]
            }
            ]
        }

        self.assertEqual(response.json(),body)
        self.assertEqual(response.status_code, 200)

class DetailBoardViewTest(TestCase):
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

        user        = User.objects.create(id = 1, name = "kim", email = "kim@naver.com", password = bcrypt.hashpw("kim12345!".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), regions = seoul)
        naver       = Company.objects.create(id=1, name="naver", password = bcrypt.hashpw("naver12345!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), regions = seoul)
        google      = Company.objects.create(id=2, name="google", password = bcrypt.hashpw("google12345!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), regions = seoul)
        
        board       = Board.objects.create(id = 1, company = naver, money = 100000, descrtption = "네이버구직", position = "master")
        board2      = Board.objects.create(id = 2, company = naver, money = 200000, descrtption = "네이버구직2", position = "junior")
        board3      = Board.objects.create(id = 3, company = google, money = 200000, descrtption = "구글구직", position = "junior")
            
    
        board.skills.add(skilljava)
        board.skills.add(skillpython)
        board2.skills.add(skilljava)

        apply       = Apply.objects.create(id=1 , user = user, board = board2)

    def tearDown(self):
        Country.objects.all().delete()
        Region.objects.all().delete()
        Board.objects.all().delete()
        Skill.objects.all().delete()
        Company.objects.all().delete()
        Apply.objects.all().delete()
        User.objects.all().delete()

    def test_success_show_detail_board_get(self):
        client = Client()

        response = client.get('/boards/1', content_type='application/json')

        body = {
            "result": {
                "채용공고_id"     :1,
                "회사_id"        : 1,
                "회사_name"       : "naver",
                "국가"           :"korea",
                "지역"           :"seoul",
                "채용포지션"       : "master",
                "채용보상금"       : 100000,
                "채용내용"        : "네이버구직",
                "사용기술"        : ["python","java"],
                "회사에가올린다른채용공고":[2]
            }
        }

        self.assertEqual(response.json(),body)
        self.assertEqual(response.status_code, 200)
    
    def test_fail_show_detail_board_get(self):
        client = Client()
        
        response = client.get('/boards/10', content_type='application/json')

        self.assertEqual(response.json(),{"message" :"board_does_not_exist"})
        self.assertEqual(response.status_code, 400)

    def test_success_user_apply_board_post(self):
        client      = Client()
        token       = jwt.encode({'id':User.objects.get(id= 1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        response = client.post('/boards/1',content_type='application/json', **headers)
        
        self.assertEqual(response.json(),{"message":"apply_success"})
        self.assertEqual(response.status_code, 201)

    def test_fail_user_already_apply_board_post(self):
        client      = Client()
        token       = jwt.encode({'id':User.objects.get(id= 1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        response = client.post('/boards/2',content_type='application/json', **headers)
        
        self.assertEqual(response.json(),{"message":"already apply company"})
        self.assertEqual(response.status_code, 400)
    
    def test_fail_user_apply_not_exist_board_post(self):
        client      = Client()
        token       = jwt.encode({'id':User.objects.get(id= 1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        response = client.post('/boards/10',content_type='application/json', **headers)
        
        self.assertEqual(response.json(),{"message":"board_does_not_exist"})
        self.assertEqual(response.status_code, 400)

    def test_success_company_delete_board_delete(self):
        client = Client()
        token  = jwt.encode({"id":Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.delete('/boards/1', content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"delete_success"})
        self.assertEqual(response.status_code, 200)

    def test_fail_company_delete_not_comany_board_delete(self):
        client = Client()
        token  = jwt.encode({"id":Company.objects.get(id=2).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.delete('/boards/1', content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"is not your board"})
        self.assertEqual(response.status_code, 400)

    def test_fail_company_delete_not_exist_board_delete(self):
        client = Client()
        token  = jwt.encode({"id":Company.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.delete('/boards/5', content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"board_does_not_exist"})
        self.assertEqual(response.status_code, 400)

    def test_success_company_all_update_patch(self):
        client = Client()
        
        body = {
            "money": 2000,
            "position":"senior",
            "skills":["python"]
        }
        
        token = jwt.encode({"id":Company.objects.get(id = 1).id},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.patch('/boards/1', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"patch_success"})
        self.assertEqual(response.status_code, 200)

    def test_success_company_money_update_patch(self):
        client = Client()
        
        body = {
            "money": 2000
        }
        
        token = jwt.encode({"id":Company.objects.get(id = 1).id},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.patch('/boards/1', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"patch_success"})
        self.assertEqual(response.status_code, 200)

    def test_success_company_position_update_patch(self):
        client = Client()
        
        body = {
            "postition": "test"
        }
        
        token = jwt.encode({"id":Company.objects.get(id = 1).id},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.patch('/boards/1', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"patch_success"})
        self.assertEqual(response.status_code, 200)

    def test_success_company_skills_update_patch(self):
        client = Client()
        
        body = {
            "skills": ["python"]
        }
        
        token = jwt.encode({"id":Company.objects.get(id = 1).id},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.patch('/boards/1', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"patch_success"})
        self.assertEqual(response.status_code, 200)

    def test_fail_company_not_company_board_patch(self):
        client = Client()
        
        body = {
            "money": 2000,
            "position":"senior",
            "skills":["python"]
        }
        
        token = jwt.encode({"id":Company.objects.get(id = 1).id},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.patch('/boards/3', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"is not your board"})
        self.assertEqual(response.status_code, 400)

    def test_fail_company_skill_does_not_exist_patch(self):
        client = Client()
        
        body = {
            "money": 2000,
            "position":"senior",
            "skills": ["kotlin","docker"]
        }
        
        token = jwt.encode({"id":Company.objects.get(id = 1).id},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization": token}
        response = client.patch('/boards/1', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.json(),{"message":"skill_does_not_exist"})
        self.assertEqual(response.status_code, 400)