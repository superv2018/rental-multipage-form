from django.urls import path



from . import views
from .forms import NewRentalPropertyForm, NewContractForm

urlpatterns = [
    path('', views.HomeView.as_view(), name="home" ),
    path('<int:pk>/',views.DetailView.as_view(), name='detail'),
    path('new_rental/<int:pk>', views.new_rental, name='new_rental'),
    #path('new_contract/', views.CreateContractView.as_view(), name='new_contract'),
    path('update/<int:pk>', views.UpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.DeleteView.as_view(), name='delete'),
] 
