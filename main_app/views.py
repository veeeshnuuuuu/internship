from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            print(form.er)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_transaction(request):
    # Calculate current balance
    transactions = Transaction.objects.filter(user=request.user)
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    current_balance = total_income - total_expense

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user

            if transaction.type == 'expense' and transaction.amount > current_balance:
                messages.error(request, f"Insufficient balance! You have only ₹{current_balance:.2f} available.")
            else:
                transaction.save()
                messages.success(request, "Transaction added successfully!")
                return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {
        'form': form,
        'balance': current_balance,
    })

@login_required
def admin_users(request):
    if not request.user.is_staff:
        return redirect('index')
    users = CustomUser.objects.filter(is_superuser=False).order_by('-date_joined')
    return render(request, 'admin_users.html', {'users': users})