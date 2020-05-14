from django.urls import path
from . import views

urlpatterns =[
	path('',views.index,name='index'),
	path('outcome',views.outcome,name='outcome'),
	path('WebDriverCall',views.WebDriverCall,name='WebDriverCall'),
	path('FindClassStatic',views.FindClassStatic,name='FindClassStatic'),
	path('downloadCSV',views.downloadCSV,name='downloadCSV')
]