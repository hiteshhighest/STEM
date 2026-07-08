from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import VolunteerApplicationForm  # Ensure this matches your form definition name

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')
        
        # Build clean string email block
        query_email = (
            f"New General Query from STEM for Nepal Home Page:\n\n"
            f"Sender Name: {name}\n"
            f"Sender Email: {email}\n\n"
            f"Message Context:\n{message_content}"
        )
        
        # Dispatch notification email out to default internal recipient parameters
        send_mail(
            subject=f"General Query Sub: {name}",
            message=query_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.RECIPIENT_ADDRESS],
            fail_silently=False,
        )
        
        messages.success(request, "Your query has been sent successfully! Our team will get back to you soon.")
        return redirect('home')
        
    return render(request, 'core/home.html')

from django.shortcuts import render

def programs_view(request):
    programs = [
        {
            "title": "Shikshya Sabailai", 
            "tagline": "Education",
            "description": "Join our flagship initiative to bring quality STEM education to all. Volunteer, donate, or spread awareness to make a real difference in underserved communities through foundational digital and scientific literacy modules.",
            "image": "/static/shikshya_sabailai.jpg"  # Map your asset file pathway configuration string here
        },
    ]
    return render(request, 'core/programs.html', {'programs': programs})

def team_view(request):
    members = [
        {
            "name": "Dolraj P", 
            "role": "President", 
            "image": "pfp.jpg"
        },
        {
            "name": "Ritima G", 
            "role": "VP External", 
            "image": "pfp.jpg"
        },
        {
            "name": "Yogesh D", 
            "role": "VP Internal", 
            "image": "pfp.jpg"
        },
        {
            "name": "Ojashwi J", 
            "role": "Secretary", 
            "image": "pfp.jpg"
        },
        {
            "name": "Grutso L", 
            "role": "Volunteer Manager", 
            "image": "pfp.jpg"
        },
        {
            "name": "Hitesh S", 
            "role": "IT Head", 
            "image": "hitesh.jpg"
        },
        {
            "name": "Omnika B", 
            "role": "Outreach Director", 
            "image": "pfp.jpg"
        },
        {
            "name": "Ngawang T", 
            "role": "Communication & Marketing", 
            "image": "pfp.jpg"
        },
        {
            "name": "Zoey S", 
            "role": "Content Creator", 
            "image": "pfp.jpg"
        },
        {
            "name": "Laxmi P", 
            "role": "Executive Member", 
            "image": "pfp.jpg"
        },
        {
            "name": "Srija A", 
            "role": "Executive Member", 
            "image": "pfp.jpg"
        },
    ]
    return render(request, 'core/team.html', {'members': members})

def volunteer_view(request):
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Extract updated field data directly from your text inputs
            full_name = data.get('full_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            skills = data.get('skills')
            motivation = data.get('motivation')
            
            # Email 1: Detailed Internal Admin Monitoring Message Block
            admin_message = (
                f"New Volunteer Application Received:\n\n"
                f"Name: {full_name}\n"
                f"Email: {email}\n"
                f"Phone Number: {phone_number}\n\n"
                f"Skills & Expertise:\n{skills}\n\n"
                f"Motivation / Statement of Purpose:\n{motivation}"
            )
            
            send_mail(
                subject=f"Volunteer Form Sub: {full_name}",
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.RECIPIENT_ADDRESS],
                fail_silently=False,
            )
            
            # Email 2: Professional Direct Receipt Copy Sent Back To Applicant Inbox
            applicant_message = (
                f"Hi {full_name},\n\n"
                f"Thank you for applying to join STEM for Nepal!\n\n"
                f"Our leadership committee has successfully received your application details. \n\n"
                f"Your profile and follow up with you at this address shortly.\n\n"
                f"Warm regards,\n"
                f"The STEM for Nepal Core Committee"
            )
            
            send_mail(
                subject="We received your application! — STEM for Nepal",
                message=applicant_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return redirect('volunteer_success')
    else:
        form = VolunteerApplicationForm()
        
    return render(request, 'core/volunteer.html', {'form': form})

def volunteer_success(request):
    return render(request, 'core/success.html')
