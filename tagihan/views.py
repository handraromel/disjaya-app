from wkhtmltopdf.views import PDFTemplateView

from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.db.models import Q, Sum, Value as V
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Anggaran, Pembayaran, User
from .forms import AnggaranForm, PembayaranForm, ProblemForm, UserForm

@login_required(login_url="/tagihan/login_user/")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'tagihan/login.html')
    else:
        anggaran = Anggaran.objects.filter(user=request.user)
        pembayaran_results = Pembayaran.objects.all()
    return render(request, 'tagihan/index.html', {'anggaran':anggaran})

@login_required(login_url="/tagihan/login_user/")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_anggaran(request):
    if not request.user.is_authenticated():
        return render(request, 'tagihan/login.html')
    else:
        form = AnggaranForm(request.POST or None, request.FILES or None)
        user = User.objects.all()
        if form.is_valid():
            anggaran = form.save(commit=False)
            anggaran.save()
            anggaran.user = user
            anggaran.save()
            form.save_m2m()
            return HttpResponsePermanentRedirect(reverse('tagihan:detail', args=(anggaran.id,)))
        context = {
            'form': form,
        }
        return render(request, 'tagihan/create_anggaran.html', context)

@login_required(login_url="/tagihan/login_user/")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_pembayaran(request, anggaran_id):
    form = PembayaranForm(request.POST or None, request.FILES or None)
    anggaran = get_object_or_404(Anggaran, pk=anggaran_id)
    if form.is_valid():
        pembayaran =  form.save(commit=False)
        pembayaran.anggaran = anggaran
        pembayaran.save()
        return HttpResponsePermanentRedirect(reverse('tagihan:detail', args=(anggaran.id,)))
    context = {
        'anggaran':anggaran,
        'form':form,
    }
    return render(request, 'tagihan/create_pembayaran.html', context)

@login_required(login_url="/tagihan/login_user/")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detail(request, anggaran_id):
    if not request.user.is_authenticated():
        return render(request, 'tagihan/login.html')
    else:
        anggaran = get_object_or_404(Anggaran, pk=anggaran_id)
        pembayaran_result = anggaran.pembayaran_set.all().order_by('id')

        query = request.GET.get('q')
        if query :
            pembayaran_result = pembayaran_result.filter(
                Q(provider_name__icontains=query) |
                Q(vendor_number__icontains=query) |
                Q(bill_number__icontains=query) |
                Q(receipt_number__icontains=query) |
                Q(payment_date__icontains=query) |
                Q(verification_date__icontains=query)
            ).distinct()

        paginator = Paginator(pembayaran_result, 10)
        page = request.GET.get('page')
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        total_emp_payment = anggaran.pembayaran_set.filter(is_verified=True).aggregate(total_emp=Coalesce(Sum('employee_payment'), V(0)))
        total_pension_payment = anggaran.pembayaran_set.filter(is_verified=True).aggregate(total_pension=Coalesce(Sum('pension_payment'), V(0)))
        total_all = total_emp_payment['total_emp'] + total_pension_payment['total_pension']
        rest_anggaran = anggaran.money_amount - total_all
        user = request.user

        context = {
            'pembayaran' : pages,
            'anggaran': anggaran,
            'user': user,
            'total_emp_payment':total_emp_payment,
            'total_pension_payment':total_pension_payment,
            'total_all':total_all,
            'rest_anggaran':rest_anggaran,
        }
        return render(request, 'tagihan/detail.html', context)

@login_required(login_url="/tagihan/login_user/")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_pembayaran(request, anggaran_id, pembayaran_id):
    anggaran = Anggaran.objects.get(pk = anggaran_id)
    pembayaran = get_object_or_404(Pembayaran, pk = pembayaran_id)
    if request.method == "POST":
        form = PembayaranForm(request.POST, instance=pembayaran)
        if form.is_valid():
            pembayaran = form.save(commit=False)
            pembayaran.user = request.user
            pembayaran.save()
            return HttpResponsePermanentRedirect(reverse('tagihan:detail', args=(anggaran.id,)))
    else:
        form = PembayaranForm(instance=pembayaran)
    context = {
        'anggaran' : anggaran,
        'form' : form,
    }
    return render(request, 'tagihan/edit_pembayaran.html', context)

@login_required(login_url="/tagihan/login_user/")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_problem(request, anggaran_id, pembayaran_id):
    anggaran = Anggaran.objects.get(pk = anggaran_id)
    pembayaran = get_object_or_404(Pembayaran, pk = pembayaran_id)
    if request.method == "POST":
        form = ProblemForm(request.POST, instance=pembayaran)
        if form.is_valid():
            pembayaran = form.save(commit=False)
            pembayaran.user = request.user
            pembayaran.save()
            return HttpResponsePermanentRedirect(reverse('tagihan:detail', args=(anggaran.id,)))
    else:
        form = ProblemForm(instance=pembayaran)
    context = {
        'anggaran' : anggaran,
        'form' : form,
    }
    return render(request, 'tagihan/edit_problem.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                anggaran = Anggaran.objects.filter(user=request.user)
                return HttpResponsePermanentRedirect(reverse('tagihan:index'))
            else:
                return render(request, 'tagihan/login.html', {'error_message':'akun anda sudah tidak aktif'})
        else:
            return render(request, 'tagihan/login.html', {'error_message':'silahkan cek kembali username dan password anda'})
    return render(request, 'tagihan/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'tagihan/login.html')

@login_required(login_url="/tagihan/login_user/")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verified(request, pembayaran_id):
    pembayaran = get_object_or_404(Pembayaran, pk=pembayaran_id)
    try:
        if pembayaran.is_verified:
            pembayaran.is_verified = False
        else:
            pembayaran.is_verified = True
        pembayaran.save()
    except (KeyError, Pembayaran.DoesNotExist):
        return JsonResponse({'success' : False})
    else:
        return JsonResponse({'success' : True})

class print_pdf(PDFTemplateView):
    filename = 'output.pdf'
    template_name = 'tagihan/print.html'
    context_object_name = "anggaran"
    cmd_options = {
        'margin-top': 3,
        'encoding': 'utf8',
        'quiet': True,
        'page-size': 'A4',
        'orientation': 'Landscape',
    }
    def get_context_data(self,**kwargs):
        anggaran = get_object_or_404(Anggaran, id=self.kwargs['anggaran_id'])
        total_emp_payment = anggaran.pembayaran_set.filter(is_verified=True).aggregate(total_emp=Coalesce(Sum('employee_payment'), V(0)))
        total_pension_payment = anggaran.pembayaran_set.filter(is_verified=True).aggregate(total_pension=Coalesce(Sum('pension_payment'), V(0)))
        total_all = total_emp_payment['total_emp'] + total_pension_payment['total_pension']
        rest_anggaran = anggaran.money_amount - total_all
        context = {
            'anggaran': anggaran,
            'total_emp_payment':total_emp_payment,
            'total_pension_payment':total_pension_payment,
            'total_all':total_all,
            'rest_anggaran':rest_anggaran
        }
        return context
