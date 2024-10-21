from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Participant, User, Expenses 
from .forms import  ExpenseForm, ParticipantForm
import csv
from django.http import HttpResponse


def home(request, expenses_details=None):
    if request.method == 'POST':
        
        title = request.POST['title']
        total_amount = request.POST['total_amount']
        split_method = request.POST['split_method']
        description = request.POST.get('description', '')

        
        expense = Expenses.objects.create(
            title=title,
            total_amount=total_amount,
            split_method=split_method,
            description=description,
            created_by=User.objects.get(id=request.session['user_id'])
        )

        
        num_participants = int(request.POST['num_participants'])

        
        for i in range(1,num_participants+1):
            participant_name = request.POST[f'participant_{i}_name']
            participant_email = request.POST[f'participant_{i}_email']
            amount_owed = request.POST.get(f'participant_{i}_amount_owed', 0)
            percentage = request.POST.get(f'participant_{i}_percentage', 0)

            
            try:
                user = User.objects.get(email=participant_email)
            except User.DoesNotExist:
                
                user = User.objects.create(email=participant_email, name=participant_name, added_by=User.objects.get(id=request.session['user_id']))
                user.save()
            
            Participant.objects.create(
                expense=expense,
                user=user,
                amount_owed=amount_owed,
                percentage=percentage
            )

        return redirect('home')
    if not 'user_id' in request.session:
        return redirect ('login')
    
    myparticipations = Participant.objects.filter(user=User.objects.get(id=request.session['user_id']))
    user = User.objects.get(id=request.session['user_id'])
    
    content = {'username': user.name, 'email': user.email, 'myparticipations': myparticipations}
    if expenses_details:
        participations = Participant.objects.filter(expense=expenses_details)
        expense = Expenses.objects.get(id=expenses_details)
        content['expense'] = expense
        content['participations'] = participations
    return render(request, 'expenses/home.html', content)


def balance_sheet(request):
    if not 'user_id' in request.session:
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])
    myparticipations = Participant.objects.filter(user=user)

    users = set()
    expenses = set()
    amount_paid = {}
    amount_owed = {}

    for participation in myparticipations:
        expenses.add(participation.expense)
    for expense in expenses:
        participations = Participant.objects.filter(expense=expense)
        for participation in participations:
            users.add(participation.user)
            if participation.user.id not in amount_paid:
                amount_paid[participation.user.id] = 0
            if participation.user.id not in amount_owed:
                amount_owed[participation.user.id] = 0
            amount_owed[participation.user.id] += participation.amount_owed
        amount_paid[expense.created_by.id] += expense.total_amount

    user_list = list(users)

    balance_sheet = []
    for user in user_list:
        bs = {}
        bs['name'] = user.name
        bs['email'] = user.email
        bs['amount_paid'] = amount_paid[user.id]
        bs['amount_owed'] = amount_owed[user.id]
        bs['balance'] = amount_paid[user.id] - amount_owed[user.id]
        bs['description'] = 'Should pay ' + str(abs(bs['balance'])) if bs['balance'] < 0 else 'Can get back ₹' + str(abs(bs['balance']))
        balance_sheet.append(bs)

    content = {
        'balance_sheet': balance_sheet,
    }
    
    return render(request, 'expenses/balance_sheet.html', content)

def download_balance_sheet(request):
    if not 'user_id' in request.session:
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])
    myparticipations = Participant.objects.filter(user=user)

    users = set()
    expenses = set()
    amount_paid = {}
    amount_owed = {}

    for participation in myparticipations:
        expenses.add(participation.expense)
    for expense in expenses:
        participations = Participant.objects.filter(expense=expense)
        for participation in participations:
            users.add(participation.user)
            if participation.user.id not in amount_paid:
                amount_paid[participation.user.id] = 0
            if participation.user.id not in amount_owed:
                amount_owed[participation.user.id] = 0
            amount_owed[participation.user.id] += participation.amount_owed
        amount_paid[expense.created_by.id] += expense.total_amount

    user_list = list(users)

    balance_sheet = []
    for user in user_list:
        bs = {}
        bs['name'] = user.name
        bs['email'] = user.email
        bs['amount_paid'] = amount_paid[user.id]
        bs['amount_owed'] = amount_owed[user.id]
        bs['balance'] = amount_paid[user.id] - amount_owed[user.id]
        balance_sheet.append(bs)

    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    
    writer.writerow(['Name', 'Email', 'Amount Paid', 'Amount Owed', 'Balance', 'Description'])

    
    for entry in balance_sheet:
        description = 'Should pay ' + str(abs(entry['balance'])) if entry['balance'] < 0 else 'Can get back ₹' + str(abs(entry['balance']))
        writer.writerow([entry['name'], entry['email'], entry['amount_paid'], entry['amount_owed'], entry['balance'], description])

    return response
