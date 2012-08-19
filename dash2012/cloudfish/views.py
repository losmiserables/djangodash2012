from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
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
@cache_page(60 * 2)
@vary_on_cookie
def servers(request):
    user = request.user
    account = Account.objects.get(id=user.id)
    clouds = Cloud.objects.filter(account=account)
    servers = {}
    images = {}
    sizes = {}
    locations = {}
    for cloud in clouds:
        servers[cloud.type] = cloud.get_servers(**request.session["clouds"][cloud.type])
        images[cloud.type] = cloud.get_images(**request.session["clouds"][cloud.type])
        sizes[cloud.type] = cloud.get_sizes(**request.session["clouds"][cloud.type])
        locations[cloud.type] = cloud.get_locations(**request.session["clouds"][cloud.type])

    return render(request, 'servers.html', {'active_servers': 'active',
                                            "servers": servers,
                                            "images": images,
                                            "sizes": sizes,
                                            "regions": locations
                                            })


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
    c = {'active_connect': 'active'}
    if request.POST:
        c['errors'] = []
        c['msgs'] = []
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
            cloud, _ = Cloud.objects.get_or_create(type=CLOUD_AWS, account=account)
            cloud.add_auth_data(salt=passwd, cloud_login=aws_key_id, cloud_password=aws_secret_key)
            if not cloud.is_valid(cloud_login=aws_key_id, cloud_password=aws_secret_key):
                c['errors'].append("Invalid credentials for Amazon AWS, please check")
            else:
                cloud.save()
                request.session['clouds'][CLOUD_AWS] = cloud.decode_auth_data(salt=passwd)
                c['msgs'].append("Amazon AWS credentials saved")

        if "rackspace_username" in request.POST and request.POST["rackspace_username"]:
            rackspace_username = request.POST["rackspace_username"]
            rackspace_api_key = request.POST["rackspace_api_key"]
            cloud, _ = Cloud.objects.get_or_create(type=CLOUD_RACKSPACE, account=account)
            cloud.add_auth_data(salt=passwd, cloud_login=rackspace_username, cloud_password=rackspace_api_key)
            if not cloud.is_valid(cloud_login=rackspace_username, cloud_password=rackspace_api_key):
                c['errors'].append("Invalid credentials for Rackspace Open Cloud, please check.")
            else:
                cloud.save()
                request.session['clouds'][CLOUD_RACKSPACE] = cloud.decode_auth_data(salt=passwd)
                c['msgs'].append("Rackspace Open Cloud credentials saved")

        request.session.modified = True
        if c['errors']:
            return render(request, 'connect.html', c)

        return render(request, 'connect.html', c)
    else:
        # GET
        print "GET"
        c['connected'] = {}
        account = Account.objects.get(id=request.user.id)
        connected_clouds = Cloud.objects.filter(account=account)
        for cloud in connected_clouds:
            c['connected'][cloud.type] = True

    return render(request, 'connect.html', c)


@login_required
def disconnect(request):
    account = Account.objects.get(id=request.user.id)
    cloud = request.GET['cloud']
    print cloud
    if Cloud.objects.filter(type=cloud, account=account).exists():
        Cloud.objects.filter(type=cloud, account=account).delete()
    return HttpResponseRedirect(reverse('connect-view'))


def notfound(request):
    return render(request, '404.html')


@login_required
@csrf_protect
def create(request):
    c = {}
    if request.POST:
        account = Account.objects.get(id=request.user.id)
        provider = request.POST["provider"]
        name = request.POST["node-name"]
        image_id = request.POST["image"]
        size_id = request.POST["size"]
        location_id = request.POST["location"]

        cloud = Cloud.objects.filter(account=account, type=provider)[0]
        cloud.create_server(name=name, image=image_id, size=size_id, location=location_id, **request.session["clouds"][cloud.type])

        return render(request, "servers.html", c)


@login_required
def stop(request, provider, node_id):
    credentials = request.session["clouds"][provider]
    account = Account.objects.get(id=request.user.id)
    cloud = Cloud.objects.filter(account=account, type=provider)[0]
    cloud.stop_server(node_id, **credentials)

    return render(request, "servers.html")


@login_required
def start(request, provider, node_id):
    credentials = request.session["clouds"][provider]
    account = Account.objects.get(id=request.user.id)
    cloud = Cloud.objects.filter(account=account, type=provider)[0]
    cloud.start_server(node_id, **credentials)

    return render(request, "servers.html")
