from django.urls import path, include
from .views import ConferenceCreateView, ConferenceListView, ConferenceActionView, ConferenceAddPackageView, ConferenceRemovePackageView

app_name = "logistics"
urlpatterns = [
    path('conferencia/criar', ConferenceCreateView.as_view(), name='conference_create'),
    path('conferencia/listar', ConferenceListView.as_view(), name='conference_list'),
    path('conferencia/acao/<int:conference_id>/', ConferenceActionView.as_view(), name='conference_action'),
    path('conferencia/adicionar_volume/<int:conference_id>/', ConferenceAddPackageView.as_view(), name='conference_add_package'),
    path('conferencia/remover_volume/<int:conference_id>/', ConferenceRemovePackageView.as_view(), name='conference_remove_package'),
]
