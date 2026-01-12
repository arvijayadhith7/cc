from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("offerings/", views.offerings, name="offerings"),
    path("categories/",views.category,name="category"),
    path("categories/<str:tname>/act/",views.acts,name="act"),
    path("categories/<str:tname>/act/<str:act>/chapter_list/",views.chapter,name="chapter"),
    path("categories/<str:tname>/act/<str:act>/chapter_list/chapter/<int:no>/",views.section,name="section"),
    path("categories/<str:tname>/act/<str:act>/chapter_list/chapter/<int:cno>/law/<int:lno>/", views.law_detail, name="lawdetails"),
    path("chatbot/", views.chatbot_response, name="chatbot"),
]