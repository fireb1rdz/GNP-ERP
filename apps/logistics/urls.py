from django.urls import path, include
from .views import ConferenceCreateView, ConferenceListView

app_name = "logistics"
urlpatterns = [
    path('conferencia/criar', ConferenceCreateView.as_view(), name='conference_create'),
    path('conferencia/listar', ConferenceListView.as_view(), name='conference_list'),
]
