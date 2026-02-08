# tracker/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Max
from django.utils import timezone
from .models import Expense
from .forms import ExpenseForm, LoginForm 
from datetime import timedelta
from dateutil.relativedelta import relativedelta 
import json

# AUTH IMPORTS (Para sa Signup/Login)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
# Tinanggal ang: from django.contrib.auth.decorators import login_required 


# Helper function (no changes)
def get_summary_and_chart_data(expenses):
    """Calculates summary metrics (total, highest) and category breakdown."""
    
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0 
    today = timezone.now().date() 
    today_total = expenses.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0 
    highest = expenses.aggregate(Max('amount'))['amount__max'] or 0 
    
    chart_data = []
    max_value = 0 
    
    for category_slug, category_label in Expense.CATEGORY_CHOICES:
        total_for_category = expenses.filter(category=category_slug).aggregate(Sum('amount'))['amount__sum'] or 0 
        
        if total_for_category > max_value:
            max_value = total_for_category
            
        chart_data.append({ 
            'slug': category_slug, 
            'label': category_label,
            'total': float(total_for_category) 
        })
    
    return {
        'total': total,
        'today_total': today_total,
        'highest': highest,
        'chart_data': chart_data,
        'max_value': float(max_value),
        'has_expenses': any(item['total'] > 0 for item in chart_data),
    }

# === AUTHENTICATION VIEWS (Pinananatili) ===

def user_signup(request):
    """Handles new user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = UserCreationForm()
        
    return render(request, 'tracker/pages/signup.html', {'form': form})

def user_login(request):
    """Handles user login."""
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST) 
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('tracker')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
        
    return render(request, 'tracker/pages/login.html', {'form': form})

def user_logout(request):
    """Handles user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login') 


# === CORE TRACKER VIEWS (Inalis ang User Filtering) ===

Since you are now using the base.html we just created—which includes a "Financial Reports" link and a "Dashboard" link—we should make sure the tracker_view is solid and consistent with those features.

The code below includes the Safety Check (redirecting guests), the Integrity Fix (attaching the user), and ensures your dashboard remains the "Source of Truth" for your expenses.

Python
# tracker/views.py

def tracker_view(request):
    """Displays the main expense tracking dashboard."""
    
    # 1. Safety check: Protect the dashboard from unauthenticated access
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # 2. CREATE the object in memory, but don't save to database yet
            expense = form.save(commit=False)
            
            # 3. MANUALLY link the expense to the currently logged-in user
            # This fixes the NotNullViolation (IntegrityError)
            expense.user = request.user 
            
            # 4. SAVE the expense now that it has a valid user_id
            expense.save()
            
            messages.success(request, 'Expense added successfully!')
            return redirect('tracker')
    else:
        form = ExpenseForm()
    
    # 5. Fetch expenses. 
    # Use Expense.objects.filter(user=request.user) if you want users 
    # to see ONLY their own data. Otherwise, .all() shows everything to everyone.
    expenses = Expense.objects.all().order_by('-date') 
    
    # 6. Calculate summary metrics and chart data using your helper function
    summary_data = get_summary_and_chart_data(expenses)
    
    context = {
        'form': form,
        'expenses': expenses,
        'categories': Expense.CATEGORY_CHOICES,
        **summary_data, # Spreads total, today_total, highest, chart_data, etc.
    }
    return render(request, 'tracker/pages/tracker.html', context)

def edit_expense(request, pk):
    """Handles editing an existing expense."""
    # Hindi na kailangang i-check kung ang user ang may-ari ng expense
    expense = get_object_or_404(Expense, pk=pk) 
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Expense updated successfully!')
            return redirect('tracker')
    else:
        form = ExpenseForm(instance=expense)
    
    expenses = Expense.objects.all()
    summary_data = get_summary_and_chart_data(expenses)
    
    context = {
        'form': form,
        'expenses': expenses,
        'categories': Expense.CATEGORY_CHOICES,
        'is_editing': True,
        'expense': expense,
        **summary_data,
    }
    return render(request, 'tracker/pages/tracker.html', context)

def delete_expense(request, pk):
    """Handles deleting an expense."""
    expense = get_object_or_404(Expense, pk=pk) 
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
    return redirect('tracker')


def report_view(request):
    """Displays financial reports based on filters."""
    
    today = timezone.now().date()
    filter_type = request.GET.get('filter') 
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    range_type = request.GET.get('range', 'monthly') 

    # Base Query: Kumuha ng LAHAT ng expenses (walang user filtering)
    base_expenses_query = Expense.objects.all() 
    
    # ... (Rest of date logic is the same)
    if filter_type == 'today':
        start_date = today
        end_date = today
        range_type = 'custom' 
    elif start_date_str and end_date_str:
        try:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = today.replace(day=1)
            end_date = today
    
    else:
        if range_type == 'weekly':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        
        elif range_type == 'yearly':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
            
        else: # monthly (default)
            start_date = today.replace(day=1)
            end_date = start_date + relativedelta(months=1) - timedelta(days=1)

    expenses = base_expenses_query.filter(
        date__gte=start_date,
        date__lte=end_date
    ).order_by('-date') 
    
    summary_data = get_summary_and_chart_data(expenses) 
    highest_expense_obj = expenses.order_by('-amount').first() 
    
    context = {
        'expenses': expenses, 
        'start_date': start_date.strftime('%Y-%m-%d'), 
        'end_date': end_date.strftime('%Y-%m-%d'),     
        'range_type': range_type,                      
        'filter_type': filter_type,                    
        'highest_expense_obj': highest_expense_obj,  
        
        **summary_data, 
    }
    
    return render(request, 'tracker/pages/reports.html', context)