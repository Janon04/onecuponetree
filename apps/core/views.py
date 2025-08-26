from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Homepage view with hero section and impact statistics"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Mock impact statistics (in production, these would come from the database)
        context.update({
            'trees_planted': 15420,
            'youth_trained': 342,
            'coffee_cups_sold': 8750,
            'co2_saved': 2340,  # in kg
        })
        
        return context


class AboutView(TemplateView):
    """About us page with mission, vision, and story"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'mission': "To create a sustainable coffee ecosystem that empowers farmers, trains youth, and restores our environment through innovative tree planting initiatives.",
            'vision': "A world where every cup of coffee contributes to environmental restoration and economic empowerment of local communities.",
            'values': [
                {
                    'name': 'Sustainability',
                    'description': 'We prioritize environmental conservation and sustainable farming practices.'
                },
                {
                    'name': 'Education',
                    'description': 'We believe in empowering youth through comprehensive barista training and skills development.'
                },
                {
                    'name': 'Empowerment',
                    'description': 'We support coffee farmers with resources, training, and market access.'
                },
                {
                    'name': 'Innovation',
                    'description': 'We use technology and creative solutions to maximize our environmental impact.'
                }
            ]
        })
        
        return context
