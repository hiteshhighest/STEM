from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VolunteerApplicationForm
import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY

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
        
        resend.Emails.send({
            "from": "STEM for Nepal <temp@resend.dev>",
            "to": ["hiteshhighest122@gmail.com"],
            "subject": f"General Query Sub: {name}",
            "text": query_email,
        })
        
        messages.success(request, "Your query has been sent successfully! Our team will get back to you soon.")
        return redirect('home')
        
    return render(request, 'core/home.html')


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
        {
            "name": "Parin B", 
            "role": "Executive Member", 
            "image": "pfp.jpg"
        },
    ]
    return render(request, 'core/team.html', {'members': members})

def volunteer_view(request):
    if request.method == "POST":
        form = VolunteerApplicationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            full_name = data.get("full_name")
            email = data.get("email")
            phone_number = data.get("phone_number")
            skills = data.get("skills")
            motivation = data.get("motivation")

            # ==============================================================================
            # EMAIL TO STEM FOR NEPAL
            # ==============================================================================

            admin_message = (
                f"New Volunteer Application Received\n\n"
                f"Name: {full_name}\n"
                f"Email: {email}\n"
                f"Phone Number: {phone_number}\n\n"
                f"Skills & Expertise:\n"
                f"{skills}\n\n"
                f"Motivation / Statement of Purpose:\n"
                f"{motivation}"
            )

            resend.Emails.send({
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [settings.RECIPIENT_ADDRESS],
                "subject": f"Volunteer Form Submission: {full_name}",
                "text": admin_message,
            })

            # ==============================================================================
            # CONFIRMATION EMAIL TO APPLICANT
            # ==============================================================================

            applicant_message = (
                f"Hi {full_name},\n\n"
                f"Thank you for applying to volunteer with STEM for Nepal!\n\n"
                f"We have successfully received your application.\n\n"
                f"Our team will carefully review your submission and "
                f"contact you as soon as possible.\n\n"
                f"We truly appreciate your interest in supporting STEM education "
                f"across Nepal.\n\n"
                f"Best regards,\n\n"
                f"STEM for Nepal"
            )

            resend.Emails.send({
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [email],
                "subject": "We've received your volunteer application!",
                "text": applicant_message,
            })

            messages.success(
                request,
                "Your volunteer application has been submitted successfully!"
            )

            return redirect("volunteer_success")

    else:
        form = VolunteerApplicationForm()

    return render(request, "core/volunteer.html", {"form": form})

def volunteer_success(request):
    return render(request, 'core/success.html')
