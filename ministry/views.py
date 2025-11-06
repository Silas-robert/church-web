# my views 
from django.shortcuts import render
from .models import Sermon
from django.utils import timezone
from .models import Event
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DonationForm
from .models import Devotion
from .models import Testimony
from .forms import TestimonyForm
from .forms import PrayerRequestForm
from .models import Gallery
from .forms import MembershipForm
from .models import Ministry
from .forms import ContactForm
from .models import LiveStream
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os
from django.core.paginator import Paginator

def home(request):
    return render(request, 'ministry/index.html')
    
def aboutUs(request):
    return render(request, 'ministry/aboutUs.html')   


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us! Your message is received!.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct your datails and try again.")
    else:
        form = ContactForm()
    return render(request, 'ministry/contact.html', {'form': form})

def visit(request):
    return render(request, 'ministry/visit.html')

def sermons(request):
    sermons = Sermon.objects.all().order_by('-date')
    return render(request, 'ministry/sermons.html', {'sermons': sermons})

def events(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    past_events = Event.objects.filter(date__lt=timezone.now().date()).order_by('-date')
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    }
    return render(request, 'ministry/events.html', context)

def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your generous donation!")
            return redirect('donate')  # reload page or redirect to another success page
    else:
        form = DonationForm()

    return render(request, 'ministry/donate.html', {'form': form})


def blog(request):
    query = request.GET.get('q')  # Get the search query
    devotions = Devotion.objects.all().order_by('-date_posted')

    if query:
        devotions = devotions.filter(
            title__icontains=query
        ) | devotions.filter(
            author__icontains=query
        ) | devotions.filter(
            category__icontains=query
        )

    paginator = Paginator(devotions, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'ministry/blog.html', context)


def download_pdf(request, pk):
    devotion = get_object_or_404(Devotion, pk=pk)

    if not devotion.pdf_file:
        raise Http404("No PDF file found for this devotion.")

    file_path = devotion.pdf_file.path
    file_name = os.path.basename(file_path)

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


def gallery_view(request):
    gallery_items = Gallery.objects.all().order_by('-uploaded_at')
    return render(request, 'ministry/gallery.html', {'gallery_items': gallery_items})

def join(request):
    if request.method == "POST":
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your membership details have been submitted successfully!")
            return redirect('join')  # Stay on same page to show popup
        else:
            messages.error(request, "There was an error. Please check your details and try again.")
    else:
        form = MembershipForm()
    return render(request, 'ministry/join.html', {'form': form})


def live_stream(request):
    try:
        stream = LiveStream.objects.filter(is_active=True).latest('created_at')
        stream_url = stream.url
        is_live = True
    except LiveStream.DoesNotExist:
        stream_url = None
        is_live = False

    return render(request, 'ministry/live-stream.html', {
        'stream_url': stream_url,
        'is_live': is_live,
    })

def testimony(request):
    testimonies = Testimony.objects.filter(approved=True)
    form = TestimonyForm()
    if request.method == 'POST':
        form = TestimonyForm(request.POST, request.FILES)
        if form.is_valid():
            new_testimony = form.save(commit=False)
            new_testimony.approved = False  # require admin approval
            new_testimony.save()
            form = TestimonyForm()  # reset form after submit
            success = True
        else:
            success = False
    else:
        success = None

    return render(request, 'ministry/testimonies.html', {
        'testimonies': testimonies,
        'form': form,
        'success': success
    })


def prayer_list(request):
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your prayer need is received seccessful!.")
            return redirect('prayer_list')
        else:
            messages.error(request, "Please correct your datails and try again.")
    else:
        form = PrayerRequestForm()
    return render(request, 'ministry/prayer_list.html', {'form': form})


def ministries(request):
    ministries = Ministry.objects.all().order_by('-created_at')
    return render(request, 'ministry/ministries.html', {'ministries': ministries})


def search_event(request):
    results = None

    if request.method == 'GET' and any(param in request.GET for param in ['date', 'location', 'keyword']):
        keyword = request.GET.get('keyword', '').strip()
        date = request.GET.get('date', '').strip()
        location = request.GET.get('location', '').strip()

        # Start with all events, then filter step by step
        query = Event.objects.all()

        if keyword:
            query = query.filter(title__icontains=keyword)

        if location:
            query = query.filter(location__icontains=location)

        if date:
            query = query.filter(date=date)  # only filter if date is valid and filled

        results = query

        if not results.exists():
            messages.info(request, "No result match!")
    return render(request, 'ministry/events.html', {'results': results})


def home(request):
    stats = {
        'events': Event.objects.count(),
        'ministries': Ministry.objects.count(),
        'devotions': Devotion.objects.count(),
        'gallery': Gallery.objects.count(),
    }

    return render(request, 'ministry/index.html', {'stats': stats})






