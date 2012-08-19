from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from auth.models import Account
from cloudfish import CLOUD_AWS, CLOUD_RACKSPACE
from cloudfish.models import Cloud


def index(request):
    if request.user.is_authenticated():
        return render(request, 'index_loggedin.html')
    return render(request, 'index.html')


@login_required
def account(request):
    c = {}
    c.update({'active_account': 'active'})
    c['errors'] = []
    c['msgs'] = []
    if request.POST:

        current_passwd = request.POST['cpasswd']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            c['errors'].append("New password don't match")
        if not request.user.check_password(current_passwd):
            c['errors'].append("Current password don't match")

        if not c['errors']:
            request.user.set_password(password)
            request.user.save()
            # We need to re-encrypt all connected Clouds auth data
            account = Account.objects.filter(id=request.user.id)
            connected_clouds = Cloud.objects.filter(account=account)
            for cloud in connected_clouds:
                old_data = cloud.decode_auth_data(salt=current_passwd)
                cloud.add_auth_data(salt=password, **old_data)
                cloud.save()
            c['msgs'].append("Account saved")

        return render(request, 'account.html', c)

    return render(request, 'account.html', c)


@login_required
def servers(request):
    user = request.user
    account = Account.objects.get(id=user.id)
    clouds = Cloud.objects.filter(account=account)
    servers = []
    for cloud in clouds:
        servers += cloud.get_servers(**request.session["clouds"][cloud.type])

    return render(request, 'servers.html', {'active_servers': 'active', "servers": servers})


@csrf_protect
def register(request):
    c = {}
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        email = request.POST['email']
        if Account.objects.filter(email=email):
            c["errors"] = "This email is already in use."
            return render(request, "register.html", c)

        new_user = Account.objects.create_user(username, email, password)
        new_user.save()

        user = authenticate(username=username, password=password)
        login(request, user)

        request.session['passwd'] = password
        return HttpResponseRedirect(reverse("connect-view"))

    return render(request, 'register.html', c)


@login_required
def connect(request):
    if request.POST:
        c = {}
        c['errors'] = []
        if not request.session.get('clouds', None):
            request.session['clouds'] = {}

        passwd = request.POST['password']
        user = request.user
        account = Account.objects.get(id=user.id)

        if not account.check_password(passwd):
            c['errors'].append("Wrong password, please check")
            return render(request, 'connect.html', c)

        if "aws_key_id" in request.POST and request.POST["aws_key_id"]:
            aws_key_id = request.POST["aws_key_id"]
            aws_secret_key = request.POST["aws_secret_key"]
            cloud = Cloud(type=CLOUD_AWS, account=account)
            cloud.add_auth_data(salt=passwd, cloud_login=aws_key_id, cloud_password=aws_secret_key)
            if not cloud.is_valid(cloud_login=aws_key_id, cloud_password=aws_secret_key):
                c['errors'].append("Invalid credentials for Amazon AWS, please check")
            else:
                cloud.save()
                request.session['clouds'][CLOUD_AWS] = cloud.decode_auth_data(salt=passwd)

        if "rackspace_username" in request.POST and request.POST["rackspace_username"]:
            rackspace_username = request.POST["rackspace_username"]
            rackspace_api_key = request.POST["rackspace_api_key"]
            cloud = Cloud(type=CLOUD_RACKSPACE, account=account)
            cloud.add_auth_data(salt=passwd, cloud_login=rackspace_username, cloud_password=rackspace_api_key)
            if not cloud.is_valid(cloud_login=rackspace_username, cloud_password=rackspace_api_key):
                c['errors'].append("Invalid credentials for Rackspace Open Cloud, please check.")
            else:
                cloud.save()
                request.session['clouds'][CLOUD_RACKSPACE] = cloud.decode_auth_data(salt=passwd)

        request.session.modified = True
        if c['errors']:
            return render(request, 'connect.html', c)

        return HttpResponseRedirect(reverse("myservers-view"))

    return render(request, 'connect.html')
