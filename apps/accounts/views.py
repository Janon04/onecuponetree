from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'accounts/profile.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    """User dashboard view"""
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Add role-specific dashboard data
        context.update({
            'user_role': user.role,
            'is_admin': user.is_admin(),
            'is_partner': user.is_partner(),
            'is_donor': user.is_donor(),
            'is_volunteer': user.is_volunteer(),
            'is_student': user.is_student(),
        })
        
        return context
