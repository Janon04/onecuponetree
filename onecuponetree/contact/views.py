from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

def contact_view(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		# Save to database
		ContactMessage.objects.create(
			name=name,
			email=email,
			subject=subject,
			message=message
		)
		# Send notification email
		print('Attempting to send contact notification email...')
		send_mail(
			f'New Contact Message: {subject}',
			f'From: {name} <{email}>\n\nMessage:\n{message}',
			settings.DEFAULT_FROM_EMAIL,
			[settings.CONTACT_NOTIFICATION_EMAIL]
		)
		print('Contact notification email sent (if no error above).')
		return redirect('contact:thanks')
	return render(request, 'contact/contact.html')
