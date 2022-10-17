from django.urls import path

from users.views import SignInView, SignUpView, ApplyListView

urlpatterns = [
    path("/signup", SignUpView.as_view()),
    path("/signin", SignInView.as_view()),
    path("/applylist", ApplyListView.as_view())
]
