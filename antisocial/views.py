import secrets

from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import EmailToken, LinkedEmailAccount, User


def main(request):
    return render(request, 'main.html')


def login(request):
    auth_type = request.POST['auth_type']
    if auth_type == 'email':
        return login_email(request)


def logout(request):
    was_user = request.user.display_name
    auth.logout(request)
    return render(request, 'logout_confirm.html', {
        'previous_user': was_user,
    })


def login_email(request):
    address = request.POST['email']
    account, _ = LinkedEmailAccount.objects.get_or_create(email=address)
    token = secrets.token_urlsafe()

    EmailToken.objects.create(account=account, token=token)
    send_mail(
        # TODO: Get the name of the site from settings
        'Your temporary password for Antisocial',
        f'Use {token} to log in.',
        # TODO: configure a noreply account in settings
        'noreply@bob.bob',
        [address],
    )

    return render(request, 'email_token_sent.html', {
        'address': address,
        'return_url': request.POST['return_url'],
    })


def email_token_submit(request):
    submitted_token = request.GET['token']
    try:
        token = EmailToken.objects.get(token=submitted_token)
    except EmailToken.DoesNotExist:
        return render(request, 'sorry.html', {
            'message':
                f'{submitted_token} is not an active temporary password.',
        }, status_code=422)

    account = token.account

    if account.user is None:
        account.user = User.objects.create(
            display_name=account.email,
        )
        account.save()

    auth.login(request, account.user)

    token.delete()

    next_path = request.GET.get('next', '/')
    if next_path == '/logout':
        next_path = '/'
    return HttpResponseRedirect(next_path)


