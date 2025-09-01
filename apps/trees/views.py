from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from .models import Tree
from .forms import TreeTrackingForm, PlantTreeForm, TreePlantingInitiativeForm

def track_tree(request):
    if request.method == 'POST':
        form = TreeTrackingForm(request.POST)
        if form.is_valid():
            tree_id = form.cleaned_data['tree_id']
            try:
                tree = Tree.objects.get(tree_id=tree_id)
                return render(request, 'trees/tracking_result.html', {'tree': tree})
            except Tree.DoesNotExist:
                messages.error(request, _("Tree ID not found. Please check and try again."))
    else:
        form = TreeTrackingForm()
    return render(request, 'trees/track.html', {'form': form})

def plant_tree(request):
    from .models import TreePlantingSubmission
    if request.method == 'POST':
        form = TreePlantingInitiativeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            submission = TreePlantingSubmission(
                tree_type=data['tree_type'],
                quantity=data['quantity'],
                country=data['country'],
                province=data['province'],
                district=data['district'],
                sector=data['sector'],
                cell=data['cell'],
                village=data['village'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                planting_date=data['planting_date'],
                contribution_type=data['contribution_type'],
                full_name=data['full_name'],
                contact=data['contact'],
                reason=data.get('reason', ''),
                agreement=data['agreement']
            )
            if form.cleaned_data.get('photo'):
                submission.photo = form.cleaned_data['photo']
            submission.save()
            messages.success(request, _("Thank you for joining the green movement! Your submission has been received."))
            return redirect('trees:plant_tree')
    else:
        form = TreePlantingInitiativeForm()
    return render(request, 'trees/plant.html', {'form': form})

class TreeListView(ListView):
    model = Tree
    template_name = 'trees/list.html'
    context_object_name = 'trees'
    paginate_by = 10
    
    def get_queryset(self):
        return Tree.objects.filter(is_active=True).order_by('-planted_date')

class TreeDetailView(DetailView):
    model = Tree
    template_name = 'trees/detail.html'
    context_object_name = 'tree'
    
    def get_queryset(self):
        return Tree.objects.filter(is_active=True)