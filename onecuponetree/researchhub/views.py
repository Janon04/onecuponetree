from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.urls import reverse
import os
from .forms import PublicationDownloadRequestForm
from .models import PublicationDownloadRequest, ResearchPublication, ResearchCategory
from .models import ResearchSubscriber

# Research & Publications email subscription view
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import ResearchSubscriber

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.shortcuts import redirect
from django.contrib import messages


from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import ResearchPublication, ResearchCategory


def subscribe(request):
	if request.method == 'POST':
		email = request.POST.get('email', '').strip()
		if not email:
			messages.error(request, 'Please enter a valid email address.')
			return redirect(request.META.get('HTTP_REFERER', '/'))
		if ResearchSubscriber.objects.filter(email__iexact=email).exists():
			messages.info(request, 'You are already subscribed to Research & Publications updates.')
		else:
			ResearchSubscriber.objects.create(email=email)
			messages.success(request, 'Thank you for subscribing to Research & Publications updates!')
		return redirect(request.META.get('HTTP_REFERER', '/'))
	return redirect('/')

def subscribe(request):
	if request.method == 'POST':
		email = request.POST.get('email', '').strip()
		try:
			validate_email(email)
		except ValidationError:
			messages.error(request, "Please enter a valid email address.")
			return redirect(request.META.get('HTTP_REFERER', '/'))
		if ResearchSubscriber.objects.filter(email__iexact=email).exists():
			messages.info(request, "You are already subscribed to Research & Publications updates.")
		else:
			ResearchSubscriber.objects.create(email=email)
			messages.success(request, "Thank you for subscribing to Research & Publications updates!")
		return redirect(request.META.get('HTTP_REFERER', '/'))
	return redirect('/')



# List and approve publication download requests (staff only)
@staff_member_required
@csrf_protect
def publication_download_requests(request):
	requests_qs = PublicationDownloadRequest.objects.select_related('publication').order_by('-requested_at')
	if request.method == 'POST' and 'approve_id' in request.POST:
		req_id = request.POST.get('approve_id')
		req = PublicationDownloadRequest.objects.filter(id=req_id, approved=False).first()
		if req:
			req.approved = True
			req.approved_at = timezone.now()
			req.save()
			messages.success(request, f"Request for '{req.publication.title}' by {req.name} approved.")
		return HttpResponseRedirect(reverse('researchhub:publication_download_requests'))
	return render(request, 'researchhub/publication_download_requests.html', {'requests': requests_qs})

def publication_list(request):
	categories = ResearchCategory.objects.filter(is_active=True).order_by('name')
	category_id = request.GET.get('category')
	publications = ResearchPublication.objects.filter(is_active=True)
	if category_id:
		publications = publications.filter(category_id=category_id)
	publications = publications.order_by('-publication_date', '-created_at')
	return render(request, 'researchhub/publication_list.html', {
		'publications': publications,
		'categories': categories,
		'selected_category': int(category_id) if category_id else None,
	})

def publication_detail(request, pk):
	publication = get_object_or_404(ResearchPublication, pk=pk, is_active=True)
	can_download = False
	if request.user.is_authenticated and request.user.is_staff:
		can_download = True
	else:
		# Check if this user (by email) has an approved request
		email = request.session.get('download_email')
		if email:
			approved = PublicationDownloadRequest.objects.filter(publication=publication, email=email, approved=True).exists()
			if approved:
				can_download = True

	if request.method == 'POST' and 'download_request' in request.POST:
		form = PublicationDownloadRequestForm(request.POST)
		if form.is_valid():
			req, created = PublicationDownloadRequest.objects.get_or_create(
				publication=publication,
				email=form.cleaned_data['email'],
				defaults={
					'name': form.cleaned_data['name'],
					'reason': form.cleaned_data['reason'],
				}
			)
			request.session['download_email'] = form.cleaned_data['email']
			if created:
				messages.success(request, 'Your request has been submitted and is pending admin approval.')
			else:
				messages.info(request, 'You have already requested this publication. Please wait for admin approval.')
			form = PublicationDownloadRequestForm()
		else:
			messages.error(request, 'Please correct the errors below.')
	else:
		form = PublicationDownloadRequestForm()

	return render(request, 'researchhub/publication_detail.html', {
		'publication': publication,
		'can_download': can_download,
		'form': form,
	})

def publication_secure_download(request, pk):
	publication = get_object_or_404(ResearchPublication, pk=pk, is_active=True)
	can_download = False
	if request.user.is_authenticated and request.user.is_staff:
		can_download = True
	else:
		email = request.session.get('download_email')
		if email:
			approved = PublicationDownloadRequest.objects.filter(publication=publication, email=email, approved=True).exists()
			if approved:
				can_download = True
	if not can_download or not publication.document:
		raise Http404()
	file_path = publication.document.path
	if not os.path.exists(file_path):
		raise Http404()
	return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

	if request.method == 'POST' and 'download_request' in request.POST:
		form = PublicationDownloadRequestForm(request.POST)
		if form.is_valid():
			req, created = PublicationDownloadRequest.objects.get_or_create(
				publication=publication,
				email=form.cleaned_data['email'],
				defaults={
					'name': form.cleaned_data['name'],
					'reason': form.cleaned_data['reason'],
				}
			)
			request.session['download_email'] = form.cleaned_data['email']
			if created:
				messages.success(request, 'Your request has been submitted and is pending admin approval.')
			else:
				messages.info(request, 'You have already requested this publication. Please wait for admin approval.')
			form = PublicationDownloadRequestForm()
		else:
			messages.error(request, 'Please correct the errors below.')
	else:
		form = PublicationDownloadRequestForm()

	return render(request, 'researchhub/publication_detail.html', {
		'publication': publication,
		'can_download': can_download,
		'form': form,
	})

# Category management view for frontend
@csrf_protect
def category_manage(request):
	categories = ResearchCategory.objects.all().order_by('name')
	if request.method == 'POST':
		if 'toggle_id' in request.POST:
			# Toggle active status
			cat = ResearchCategory.objects.get(id=request.POST['toggle_id'])
			cat.is_active = not cat.is_active
			cat.save()
			return HttpResponseRedirect(reverse('researchhub:category_manage'))
		elif 'name' in request.POST:
			name = request.POST.get('name').strip()
			description = request.POST.get('description', '').strip()
			if name:
				ResearchCategory.objects.get_or_create(name=name, defaults={'description': description, 'is_active': True})
			return HttpResponseRedirect(reverse('researchhub:category_manage'))
	return render(request, 'researchhub/category_manage.html', {'categories': categories})



	@csrf_protect
	def category_manage(request):
		categories = ResearchCategory.objects.all().order_by('name')
		if request.method == 'POST':
			if 'toggle_id' in request.POST:
				# Toggle active status
				cat = ResearchCategory.objects.get(id=request.POST['toggle_id'])
				cat.is_active = not cat.is_active
				cat.save()
				return HttpResponseRedirect(reverse('researchhub:category_manage'))
			elif 'name' in request.POST:
				name = request.POST.get('name').strip()
				description = request.POST.get('description', '').strip()
				if name:
					ResearchCategory.objects.get_or_create(name=name, defaults={'description': description, 'is_active': True})
				return HttpResponseRedirect(reverse('researchhub:category_manage'))
		return render(request, 'researchhub/category_manage.html', {'categories': categories})
