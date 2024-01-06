from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                    path('', views.HomeView.as_view(), name="home"),
                    path('contactus/', views.ContactUsView.as_view(), name="contactus"),
                    path('checkoutcart/', views.CheckOutCartView.as_view(), name="checkoutcart"),
                    path('checkoutcomplete/', views.CheckOutCompleteView.as_view(), name="checkoutcomplete"),
                    path('checkoutpayment/', views.CheckOutPaymentView.as_view(), name="checkoutpayment"),
                    path('checkoutinfo/', views.CheckOutInfoView.as_view(), name="checkoutinfo"),
                    path('faq/', views.FaqView.as_view(), name="faq"),
                    path('Mobiles/', views.MobilesView.as_view(), name="mobiles"),
                    path('tablets/', views.TabletView.as_view(), name="tablets"),
                    path('iphones/', views.IphonesView.as_view(), name="iphones"),
                    path('applewatches/', views.AppleWatchesView.as_view(), name="applewatches"),
                    path('appleaccessories/', views.AppleAccessoriesView.as_view(), name="appleaccessories"),
                    path('macbooks/', views.MacbooksView.as_view(), name="macbooks"),
                    path('productlist/', views.ProductListView.as_view(), name="product"),
                    path('search/', views.SearchView.as_view(), name="search"),
                    path('myaccount/', views.MyAccountView.as_view(), name="myaccount"),
                    path('index/', views.IndexView.as_view(), name="index"),
                    path('aboutus/', views.AboutUsView.as_view(), name="aboutus"),
                    path('addproducts/', views.AddProductsView.as_view(), name="addproducts"),
                    path('login/', views.LoginView.as_view(), name="login"),
                    path('logout/', views.LogoutView.as_view(), name="logout"),
                    path('signup/', views.SignUpView.as_view(), name="signup"),
                    # path('review/', views.ReviewView.as_view(), name="review"),
                    path('productdetail/<slug:product_name>/', views.ProductDetailView.as_view(), name="productdetail"),
                    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
                    path('remove_from_cart/<int:product_id>/', views.delete_cart_item, name='remove_from_cart')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
