from django.conf.urls import url
from wkhtmltopdf.views import PDFTemplateView
from . import views

app_name = 'tagihan'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<anggaran_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pembayaran_id>[0-9]+)/verified/$', views.verified, name='verified'),
    url(r'^create_anggaran/$', views.create_anggaran, name='create_anggaran'),
    url(r'^(?P<anggaran_id>[0-9]+)/create_pembayaran/$', views.create_pembayaran, name='create_pembayaran'),
    url(r'^(?P<anggaran_id>[0-9]+)/edit_pembayaran/(?P<pembayaran_id>[0-9]+)/$', views.edit_pembayaran, name='edit_pembayaran'),
    url(r'^(?P<anggaran_id>[0-9]+)/add_problem/(?P<pembayaran_id>[0-9]+)/$', views.edit_problem, name='edit_problem'),
    url(r'^(?P<anggaran_id>[0-9]+)/print/$', views.print_pdf.as_view(template_name='tagihan/print.html', filename='output.pdf'), name='print_pdf'),
]
