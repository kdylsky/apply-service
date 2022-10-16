from django.urls import path

from boards.views import BoardView, DetailBoardView

urlpatterns = [
    path("", BoardView.as_view()),
    path("/<int:board_id>", DetailBoardView.as_view())
]
