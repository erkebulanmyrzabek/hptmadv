from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.utils import timezone
from admin_panel.models import AdminUser
from apps.users.models import Participant
from apps.events.models import Hackathon, HackathonPrizePlace
import csv
from io import StringIO
import datetime
from datetime import timedelta

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            admin_user = AdminUser.objects.get(username=username)
            if admin_user.check_password(password):
                request.session['admin_user_id'] = admin_user.id  # Сохраняем ID админа в сессии
                return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            pass
        return render(request, 'admin_panel/login.html', {'error': 'Неверные учетные данные'})
    return render(request, 'admin_panel/login.html')

def admin_dashboard(request):
    admin_user_id = request.session.get('admin_user_id')
    if not admin_user_id:
        return redirect('admin_login')
    
    # Аналитика
    total_users = Participant.objects.count()
    active_users = Participant.objects.filter(last_login__gte=timezone.now() - datetime.timedelta(days=30)).count()
    hackathons_count = Hackathon.objects.count()
    #submissions_count = Submission.objects.count() # TODO: Доделать

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'hackathons_count': hackathons_count,
        #'submissions_count': submissions_count,
    }
    return render(request, 'admin_panel/dashboard.html', context)

def manage_hackathons(request):
    admin_user_id = request.session.get('admin_user_id')
    if not admin_user_id:
        return redirect('admin_login')
    
    admin_user = AdminUser.objects.get(id=admin_user_id)
    hackathons = Hackathon.objects.all()
    if request.method == 'POST':
        if 'create' in request.POST:
            title = request.POST['title']
            status = request.POST['status']
            hackathon = Hackathon.objects.create(
                title=title,
                status=status,
                organization_id=1,
                registration_start_date=timezone.now(),
                registration_end_date=timezone.now() + timedelta(days=7),
                start_date=timezone.now() + timedelta(days=8),
                end_date=timezone.now() + timedelta(days=10),
            )

        elif 'archive' in request.POST:
            hackathon_id = request.POST['hackathon_id']
            Hackathon.objects.filter(id=hackathon_id).update(status='archived')

    return render(request, 'admin_panel/manage_hackathons.html', {'hackathons': hackathons})

def manage_users(request):
    admin_user_id = request.session.get('admin_user_id')
    if not admin_user_id:
        return redirect('admin_login')
    
    admin_user = AdminUser.objects.get(id=admin_user_id)
    users = Participant.objects.all()
    if request.method == 'POST':
        if 'ban' in request.POST:
            user_id = request.POST['user_id']
            Participant.objects.filter(id=user_id).update(is_banned=True)
        elif 'unban' in request.POST:
            user_id = request.POST['user_id']
            Participant.objects.filter(id=user_id).update(is_banned=False)

        elif 'role' in request.POST:
            user_id = request.POST['user_id']
            role_id = request.POST['role_id']
            Participant.objects.filter(id=user_id).update(role_id=role_id)

    return render(request, 'admin_panel/manage_users.html', {'users': users})

def analytics(request):
    admin_user_id = request.session.get('admin_user_id')
    if not admin_user_id:
        return redirect('admin_login')
    
    users_by_date = Participant.objects.extra({'date_created': "date(created_at)"}).values('date_created').annotate(count=Count('id'))
    hackathons_by_date = Hackathon.objects.extra({'date_created': "date(created_at)"}).values('date_created').annotate(count=Count('id'))

    if request.method == 'POST' and 'export' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="analytics.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date', 'New Users', 'New Hackathons'])
        for user_data, hackathon_data in zip(users_by_date, hackathons_by_date):
            writer.writerow([user_data['date_created'], user_data['count'], hackathon_data['count']])
        return response

    context = {
        'users_by_date': users_by_date,
        'hackathons_by_date': hackathons_by_date,
    }
    return render(request, 'admin_panel/analytics.html', context)

def admin_logout(request):
    request.session.pop('admin_user_id', None)
    return redirect('admin_login')