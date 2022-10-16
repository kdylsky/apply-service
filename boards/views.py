import json

from django.db           import transaction
from django.http         import JsonResponse
from django.views        import View

from core.utils          import login_company_decorator
from companies.models    import Company
from boards.models       import Skill, Board

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

