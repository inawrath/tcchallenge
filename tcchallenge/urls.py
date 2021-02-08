"""tcchallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.views import (
    AssetDataList,
    AssetDetail,
    AssetList,
    ScraperDetail,
    ScraperList,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('asset/', AssetList.as_view(), name='asset_list'),
    path('asset/<int:pk>/', AssetDetail.as_view(), name='asset_detail'),
    path('asset/<str:name>/detail/', AssetDataList.as_view(), name='asset_data'),
    path('scraper/', ScraperList.as_view(), name='scraper_list'),
    path('scraper/<int:pk>/', ScraperDetail.as_view(), name='scraper_detail'),
]
