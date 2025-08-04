def site_settings(request):
    """
    Context processor to make site settings available in all templates.
    """
    return {'site_settings': {'site_name': 'One Cup One Tree'}}

