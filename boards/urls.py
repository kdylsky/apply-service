from django.urls import path

from boards.views import BoardView

urlpatterns = [
    path("", BoardView.as_view())
]
