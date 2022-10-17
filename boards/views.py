import json

from django.db           import transaction
from django.http         import JsonResponse
from django.views        import View
from django.db.models    import Q 

from core.utils          import login_company_decorator, login_user_decorator
from companies.models    import Company
from boards.models       import Skill, Board, Apply

class BoardView(View):
    @login_company_decorator
    @transaction.atomic()
    def post(self, request):
        try:
            data            = json.loads(request.body)
            company         = Company.objects.get(id = request.user.id)
            money           = data["money"]
            descrtption     = data["descrtption"]
            position        = data["position"]
            skills          = data.get("skills")
            
            board = Board.objects.create(
                    company = company, 
                    money = money, 
                    descrtption = descrtption, 
                    position = position, 
            )
            
            for skill in skills:
                board.skills.add(Skill.objects.get(name = skill))

            return JsonResponse({"message": "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"mssage":"key_error"}, status=400)

        except Skill.DoesNotExist:
            return JsonResponse({"message" :"skill_does_not_exist"}, status=400)

        except Company.DoesNotExist:
            return JsonResponse({"message" :"company_does_not_exist"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message"  :"json_decode_error"}, status = 400)

    def get(self, request):
        try:
            search = request.GET.get("search")
            
            if search:
                boards = Board.objects.filter(
                    Q(company__name__icontains          = search)|
                    Q(descrtption__icontains            = search)|
                    Q(position__icontains               = search)|
                    Q(skills__name__icontains           = search)|
                    Q(company__regions__name__icontains = search)
                    ).distinct()
            else:
                boards = Board.objects.all()        
            
            result = [{
                "채용공고_id"     : board.id,
                "회사_id"        : board.company.id,
                "회사_이름"       : board.company.name,
                "채용포지션"       : board.position,
                "채용보상금"       : board.money,
                "채용내용"        : board.descrtption,
                "사용기술"        : [skill.name for skill in board.skills.all()]
            }for board in boards]        

            return JsonResponse({"result": result}, status = 200)

        except KeyError:
            return JsonResponse({"mssage":"key_error"}, status=400)

        except Board.DoesNotExist:
            return JsonResponse({"message" :"board_does_not_exist"}, status=400)

        except Skill.DoesNotExist:
            return JsonResponse({"message" :"skill_does_not_exist"}, status=400)

class DetailBoardView(View):
    def get(self, request, board_id):
        try:
            board = Board.objects.select_related('company').prefetch_related('skills').get(id = board_id)
            
            result = {
                "채용공고_id"        : board.id,
                "회사_id"           : board.company.id,
                "회사_name"         : board.company.name,
                "국가"              : board.company.regions.country.name,
                "지역"              : board.company.regions.name,
                "채용포지션"          : board.position,
                "채용보상금"          : board.money,
                "채용내용"            : board.descrtption,
                "사용기술"            : [skill.name for skill in board.skills.all()],
                "회사에가올린다른채용공고" : [post.id for post in Board.objects.filter(company = board.company).exclude(id=board_id)]
            }
            
            return JsonResponse({"result": result}, status = 200)
        
        except Board.DoesNotExist:
            return JsonResponse({"message" :"board_does_not_exist"}, status=400)

    @login_user_decorator
    def post(self, request, board_id):
        try:
            user = request.user
            board = Board.objects.get(id = board_id)
            
            apply, created = Apply.objects.get_or_create(user = user, board= board)

            if not created:
                return JsonResponse({"message":"already apply company"}, status = 400)

            return JsonResponse({"message":"apply_success"}, status = 201)
        
        except Board.DoesNotExist:
            return JsonResponse({"message" :"board_does_not_exist"}, status=400)


