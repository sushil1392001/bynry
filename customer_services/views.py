from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer, ServiceRequest
from .forms import ServiceRequestForm, CustomerUpdateForm
from django.utils.timezone import now

# Customer Views
@login_required
def create_service_request(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = Customer.objects.get(user=request.user)
            service_request.save()
            return redirect('track_requests')
    else:
        form = ServiceRequestForm()
    return render(request, 'customer_services/create_service_request.html', {'form': form})


@login_required
def track_service_requests(request):
    customer = Customer.objects.get(user=request.user)
    requests = ServiceRequest.objects.filter(customer=customer).order_by('-submitted_at')
    return render(request, 'customer_services/track_service_requests.html', {'requests': requests})


@login_required
def view_account(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('view_account')
    else:
        form = CustomerUpdateForm(instance=customer)
    return render(request, 'customer_services/view_account.html', {'form': form})

# Support Representative Views
@login_required
def support_dashboard(request):
    if not request.user.groups.filter(name='SupportRepresentatives').exists():
        return redirect('home')

    requests = ServiceRequest.objects.all().order_by('-submitted_at')
    return render(request, 'support_dashboard/dashboard.html', {'requests': requests})


@login_required
def update_service_request(request, request_id):
    if not request.user.groups.filter(name='SupportRepresentatives').exists():
        return redirect('home')

    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.method == "POST":
        status = request.POST.get('status')
        if status in dict(ServiceRequest.STATUS_CHOICES):
            service_request.status = status
            if status == 'Resolved':
                service_request.resolved_at = now()
            service_request.save()
            return redirect('support_dashboard')
    return render(request, 'support_dashboard/update_request.html', {'request': service_request})
