from __future__ import unicode_literals, absolute_import
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.conf.urls.static import static
from django_private_chat2.models import User
from django.http import JsonResponse
from django.contrib.auth.models import AbstractBaseUser
from typing import List
from django.contrib.auth import authenticate, login as auth_login, logout
# from rest_framework.views import APIView, Response
# from rest_framework.generics import ListAPIView, RetrieveAPIView
# from django.http import HttpResponse, JsonResponse



UserModel = get_user_model()


# class UsersListView(LoginRequiredMixin, ListView):
#     http_method_names = ['get', ]
#
#     def get_queryset(self):
#         #return UserModel.objects.all().exclude(id=self.request.user.id)
#         return UserModel.objects.all().exclude(username=self.request.user.username)
#
#     def render_to_response(self, context, **response_kwargs):
#         users: List[AbstractBaseUser] = context['object_list']
#
#         data = [{
#             #"username": user.get_username(),
#             "username": f"{user.first_name}-({user.last_name}) + {user.position} + ({user.department})",
#             "pk": str(user.pk)
#         } for user in users]
#         return JsonResponse(data, safe=False, **response_kwargs)



# class UsersListView(APIView):
#     def get(self, request):
#         try:
#             user = User.objects.all()
#             serializers = RealEstateSerializers(user, many=True, context={"request":self.request})
#             return Response({"data": serializers.data})
#
#         except Exception as a:
#             print(a)
#
#         return Response({"status": status.HTTP_404_NOT_FOUND})
#


def UsersListView(request):
    users = User.objects.all()
    data = [{
             "username": f"{user.first_name}-({user.last_name}) + {user.position} + ({user.department})",
             "pk": str(user.pk)

            } for user in users]
    return JsonResponse(data, safe=False)



def logout_view(request):
    logout(request)
    return redirect('home')


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('django_private_chat2.urls', namespace='django_private_chat2')),

    path('users/', UsersListView, name='users_list'),
    path('', login_required(TemplateView.as_view(template_name='base.html')), name='home'),
    path('logout/', logout_view, name='logout'),



    # path('silk/', include('silk.urls', namespace='silk')),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


##### webchat
#### 1234.
