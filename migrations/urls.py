from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_collections, name='create_collections'),
    path("upload/",views.sample_data_uploader,name="sampleinsert" ),
    path("delete/",views.delete_all,name="delete_all" )
]