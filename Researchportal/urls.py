from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import re_path
from django.views.static import serve

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from usr_val.api.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api/projects/', include('posts.urls')),
#     path('users/', include('usr_val.urls')),

    # API URLs
    path('api/user/', include('usr_val.api.urls', namespace='user_api')),

    # JWT
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="usr_val/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="usr_val/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="usr_val/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="usr_val/password_reset_done.html"),
         name="password_reset_complete"),

    # workaround for media

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    ## Api Documentation

    path('docs/', include_docs_urls(title='RpBackendAPI')),
    path('schema/', get_schema_view(
        title="RpBackendAPI",
        description="API for the Research Portal",
        version="1.0.0"
    ), name='openapi-schema'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
