from django.shortcuts import render
from django.views.generic import TemplateView

class DashboardsView(TemplateView):
    template_name = 'dashboards/dashboards.html'