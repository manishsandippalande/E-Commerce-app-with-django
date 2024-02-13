from merchapp import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home ),
    path('register',views.register ),
    path('login',views.userlogin ),
    path('allproducts/<cat>', views.productspage),
    path('productdetails/<pid>', views.productdetails),
    path('cart',views.cartPage ),
    path('addtocart/<productid>',views.addtocart ),
    path('addtowishlist/<productid>',views.addtowishlist ),
    path('delcartitem/<cid>', views.delcartitem),
    path('updatequantity/<incr>/<cartid>',views.cartquantity ),
    path('extrainfo', views.extrainfo),
    path('logout', views.userlogout),
    path('profile', views.accountPage),
    path('sort/<incr>', views.sort),
    path('placeorder', views.placeorder),
    path('wishlist', views.wishlistpage),
    path('makepayment', views.makepayment),
    path('transfercart/<pid>', views.transfercart),
    path('history', views.historypage),
    path('sendemail', views.sendemailto),
    path('otpverify', views.otp_verification),
    path('aboutpage', views.about_page),
    path('contactpage', views.contact_page),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)