from __future__ import unicode_literals, absolute_import
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.contrib.auth.models import AbstractBaseUser

from typing import List

UserModel = get_user_model()


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Chat API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]

    def get_queryset(self):
        return UserModel.objects.all().exclude(id=self.request.user.id)

    def render_to_response(self, context, **response_kwargs):
        users: List[AbstractBaseUser] = context['object_list']

        data = [{
            "username": user.get_username(),
            "pk": str(user.pk)
        } for user in users]
        return JsonResponse(data, safe=False, **response_kwargs)




urlpatterns = [
    # re_path('admin/', admin.site.urls),
    # re_path(r'', include('django_private_chat2.urls', namespace='django_private_chat2')),

    path('admin/', admin.site.urls),
    path('', include('django_private_chat2.urls', namespace='django_private_chat2')),

    path('users/', UsersListView.as_view(), name='users_list'),
    path('', login_required(TemplateView.as_view(template_name='base.html')), name='home'),

    path('silk/', include('silk.urls', namespace='silk')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

