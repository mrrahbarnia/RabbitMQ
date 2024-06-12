from django.urls import path

from . import apis

urlpatterns = [
    path('insert-data/', apis.InsertDataApi.as_view(), name='insert_data'),
    path('list-data/', apis.ListDataApi.as_view(), name='list_data'),
]