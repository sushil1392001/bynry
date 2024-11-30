from django.urls import path
from . import views

urlpatterns = [
    # Customer URLs
    path('submit-request/', views.create_service_request, name='submit_request'),
    path('track-requests/', views.track_service_requests, name='track_requests'),
    path('account/', views.view_account, name='view_account'),

    # Support Representative URLs
    path('dashboard/', views.support_dashboard, name='support_dashboard'),
    path('update-request/<int:request_id>/', views.update_service_request, name='update_request'),
]
