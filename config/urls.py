from django.contrib import admin
from django.urls import path
from core.views import dashboard_view, line_chart_json
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('dashboard/', admin.site.urls),
    path('statistics/', dashboard_view, name='dashboard_view'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)