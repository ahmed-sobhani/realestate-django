from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.InvestmentListView.as_view()),
    path('<int:pk>/', views.InvestmentDetailView.as_view()),
    path('<int:pk>/documents/', views.InvestmentDocumentListView.as_view()),
    path('<int:inv>/documents/<int:pk>/', views.InvestmentDocumentDetailView.as_view()),

    path('profile/', include([
        path('', views.ProfileInvestmentListView.as_view()),
        path('<int:pk>/', views.ProfileInvestmentDetailView.as_view()),
        path('entities/', views.InvestmentEntitiesListView.as_view()),
        path('entities/<int:pk>/', views.InvestmentEntitiesDetailView.as_view()),
        path('overview/', views.InvestorProfileOverviewView.as_view()),
    ])),

    path('admin/', include([
        path('', views.AdminInvestmentListView.as_view()),
        path('<int:pk>/', views.AdminInvestmentDetailView.as_view()),
        path('<int:pk>/documents/', views.AdminInvestmentDocumentListView.as_view()),
        path('<int:inv>/documents/<int:pk>/', views.AdminInvestmentDocumentDetailView.as_view()),
        path('profile/user/<int:pk>/', include([
            path('entities/', views.AdminInvestmentEntitiesListView.as_view()),
            path('overview/', views.AdminInvestorProfileOverviewView.as_view()),
        ])),
    ])),
]
