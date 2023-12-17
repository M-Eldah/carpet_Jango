from django.urls import path,include
from product import views

urlpatterns = [
    path('latest-products',views.LatestProductsList.as_view()),
    path('products/search',views.search),
    path('category',views.Category.as_view()),
    path('product/<slug:category_slug>/<slug:product_slug>', views.ProductDetail.as_view()),
    path('productImages/<slug:product_slug>',views.ProductImages.as_view()),
    path('category/<slug:category_slug>', views.CategoryDetail.as_view()),
    path('category',views.Category.as_view()),
    path('Filters',views.FilterData.as_view()),
    path('Filters/<slug:category_slug>/<slug:material_slug>',views.FilterProduct.as_view())
]