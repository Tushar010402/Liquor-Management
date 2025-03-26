from django.urls import path
from .views import (
    LoginView, LogoutView, TokenRefreshView,
    PasswordResetRequestView, PasswordResetConfirmView,
    TokenVerificationView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerificationView.as_view(), name='token_verify'),
    path('password/reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]