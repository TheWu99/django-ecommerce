from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def register(request):
    """
    User registration view using custom UserCreationForm.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """
    User login view using Django's AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                # Redirect to next page if specified, otherwise to home
                next_page = request.GET.get('next', 'shop:product_list')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('shop:product_list')


@login_required
def profile(request):
    """
    User profile view (requires login).
    """
    from orders.models import Order
    
    # Get recent orders for the user
    recent_orders = Order.objects.filter(user=request.user)[:5]
    
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'recent_orders': recent_orders
    })
