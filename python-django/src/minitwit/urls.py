from . import views

"""minitwit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import sim

urlpatterns = [
    path("", views.front_page_timeline, name="init_timeline"),
    # path("", include("django_prometheus.urls")),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    # path("admin", admin.site.urls),

    path("<str:username>/follow", views.follow_user),
    path("<str:username>/unfollow", views.unfollow_user),
    # Was before
    # path("fllws/<str:username>", views.follow_user),

    path("timeline/<int:amount>", views.main_timeline, name="timeline"),
    path("public/<int:amount>", views.public_timeline, name="public"),
    path("public", views.public_timeline, name="public"),
    path("add_message", views.add_message),

    # TODO / DONE changed this to standardize endpoints
    # path("sim/", include(sim.urls)),
    path("api/", include(sim.urls)),


    path("user/<str:username>", views.user_timeline, name="user_timeline"),
    path("user/<str:username>/<int:amount>",
         views.user_timeline, name="user_timeline"),
    # path("logs/", include("log_viewer.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
