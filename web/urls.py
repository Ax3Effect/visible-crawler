from django.urls import path

from web.views import get_name_view

app_name = "crawl"
urlpatterns = [path("", view=get_name_view, name="crawl")]
