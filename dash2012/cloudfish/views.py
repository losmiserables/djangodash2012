from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from auth.models import Account
from cloudfish import CLOUD_AWS, CLOUD_RACKSPACE
from cloudfish.models import Cloud


def index(request):
    if request.user.is_authenticated():
        return render(request, 'index_loggedin.html', {'greetings': 'Hi!'})
    return render(request, 'index.html')


@login_required
def account(request):
    return render(request, 'account.html', {'active_account': 'active'})


@login_required
@cache_page(60 * 5)
def servers(request):
    user = request.user
    account = Account.objects.get(id=user.id)
    clouds = Cloud.objects.filter(account=account)
    servers = []
    for cloud in clouds:
        servers += cloud.get_servers()

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
        request.session['clouds'] = {}
        # FIXME!!
        passwd = request.session['passwd']
        user = request.user
        account = Account.objects.get(id=user.id)
        if "aws_key_id" in request.POST:
            aws_key_id = request.POST["aws_key_id"]
            aws_secret_key = request.POST["aws_secret_key"]
            cloud = Cloud(type=CLOUD_AWS, account=account)
            cloud.add_auth_data(salt=passwd, cloud_login=aws_key_id, cloud_password=aws_secret_key)
            cloud.save()
            request.session['clouds'][CLOUD_AWS] = cloud.decode_auth_data(salt=passwd)

        if "rackspace_username" in request.POST:
            rackspace_username = request.POST["rackspace_username"]
            rackspace_api_key = request.POST["rackspace_api_key"]
            cloud = Cloud(type=CLOUD_RACKSPACE, account=account)
            cloud.add_auth_data(salt=passwd, cloud_login=rackspace_username, cloud_password=rackspace_api_key)
            cloud.save()

        request.session.modified = True
        return HttpResponseRedirect(reverse("myservers-view"))

    return render(request, 'connect.html')
