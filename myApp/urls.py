
from django.urls import path,include
from myApp.views import *
from django.conf import settings
from django.conf.urls.static import static
#from myApp.middlewares.auth import auth_middleware


#app_name = 'myApp'
urlpatterns = [
   #error page path
    path('404', Error404, name='404'),
    path('base/', BASE, name='base'),
    path('', HOME.as_view(), name='home'),
   
   path('product_detail/<slug:slug>/', Product_Detail, name='product_detail'),


    #('product_detail/<slug:slug>', Product_Detail, name='product_detail'),
    path('account/my_account/', My_Account, name='my_account'),
    path('account/register/', Register, name='handleregister'),
    path('account/login/', Login, name='handlelogin'),
    path('profile/', Profile, name='profile'),
    path('profile/update/', Profile_Update, name='profile_update'),
    
    
    #path('logout/', Logout , name='logout'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('product/', Products, name='product'),
    path('product/filter-data',Filter_Data,name="filter-data"),
    
    #add to cart
    
    path('cart/',Cart,name='cart'),
    path('check_out/',auth_middleware(Check_Out), name='check_out'),
    path('orders/',auth_middleware(Orders), name='orders'),
    path('item_clear/<int:id>',Item_Clear,name='item_clear'),
    path('payment_get_way/',payment_get_way,name='payment_get_way'),
    path('payment_status/',payment_status, name='payment_status'),
  #django inbuilt password reset funtionalitys 
    path('accounts/', include('django.contrib.auth.urls')),





]
    
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
   

    
    

    
    
    
    

