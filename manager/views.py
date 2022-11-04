
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

from . models import Vazhipadu, Data
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import StringIO ,BytesIO
import datetime, calendar


# Create your views here.
@login_required(login_url = 'login')
def index(request):
    return render(request, 'pages/index.html')


@login_required(login_url = 'login')
def booking(request):
    if request.method == 'POST':
        vazhipadus = Vazhipadu.objects.all()
        person_name = request.POST['name']
        nakshathram = request.POST['nakshathram']
        grand_total = 0
        summary = {
            "name" : person_name,
            "nakshathram" : nakshathram
        }
        for vazhipadu in vazhipadus:
            id_name = 'count'+str(vazhipadu.id)
            try:
                count = request.POST[id_name]
                if count.strip():
                    if int(count) > 0:
                    
                        total = int(count)*vazhipadu.price
                        grand_total += total
                        lst = [count,total]
                        summary.update({ vazhipadu.vazhipadu_name : lst })
            except:
                messages.error(request, 'ദെയവായി ശരിയായ എണ്ണം ENTER ചേയൂ')
                return redirect('booking')
   
        context = {
            'summary' : summary,
            'grand_total' : grand_total,
        }
        return render(request, 'pages/booking_summary.html', context)

    return render(request, 'pages/booking.html')


@login_required(login_url = 'login')
def get_data(request):

    if request.method == 'POST':
        try:
            month = int(request.POST['month'].strip())
            year = int(request.POST['year'].strip())
            num_days = calendar.monthrange(year, month)[1]
            days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
            month_year = days[0].strftime( "%B %Y" )
            vazhipadus = Vazhipadu.objects.all()
            data_all = []
            grand_total_sum_var = 0
            for day in days:
                date = day.strftime( "%d/%m/%Y" )
                totals = []
                total_sum_var = 0
                for vazhipadu in vazhipadus:
                    
                    total = 0
                    single_day_vazhipadu = Data.objects.filter(just_date = day , vazhipadu = vazhipadu)
                    # if single_day_vazhipadu.exists():
                    for number in single_day_vazhipadu:
                        total += number.count
                    totals.append(total)
                    total_sum_var += total*vazhipadu.price
                grand_total_sum_var += total_sum_var
                temp_list = [date]
                temp_list.extend(totals)
                temp_list.append(total_sum_var)
                data_all.append(temp_list)

        except:
            messages.error(request, 'ദെയവായി ശരിയായ മാസവും വർഷവും ENTER ചേയൂ')
            return redirect('get_data')

        context = {
            'data_all' : data_all,
            'grand_total_sum_var' : grand_total_sum_var,
            'month_year' : month_year,
            'month'  :  month,
            'year' : year,
        }
        return render(request, 'pages/view_data.html', context)
    return render(request, 'pages/get_data.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')

        else:
            messages.error(request, 'യൂസർ നെയിം അല്ലെങ്കിൽ പാസ്‌വേഡ് തെറ്റാണ്')
            return redirect('login')

    return render(request, 'pages/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'ലോഗ് ഔട്ട് ചെയ്തു')
    return redirect('login')




def print(request):
    
    template_path = 'pages/pdf_template.html'
    vazhipadus = Vazhipadu.objects.all()
    person_name = request.POST['name']
    nakshathram = request.POST['nakshathram']
    final_list = []
    for vazhipadu in vazhipadus:
        count_name = 'count_'+str(vazhipadu.id)
        if count_name in request.POST:
            count_no = request.POST[count_name]
            vazhipadu_names = vazhipadu.vazhipadu_name
            try:
                vazhipadu_add = Data(
                person_name = person_name,
                nakshathram = nakshathram,
                count = int(count_no.strip()),
                vazhipadu = vazhipadu,)
                vazhipadu_add.save()
            except:
                messages.error(request, 'Error : Please try again')
                return redirect('booking')

            temp = [vazhipadu_names, count_no]
            final_list.append(temp)
    context = { 'person_name' : person_name, 'nakshathram' : nakshathram, 'final_list' : final_list }
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    # result = BytesIO()
    # pdf_n = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # if not pdf_n.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return None
    result = BytesIO()
    pisa_status = pisa.pisaDocument(
        BytesIO(html.encode('UTF-8')), result)

    if not pisa_status.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    