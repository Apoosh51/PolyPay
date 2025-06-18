from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from decimal import Decimal

from users.models import Curator, Student
from .models import Transfer, Ticket
from .forms import CreditForm, TransferForm, ConversionForm

@login_required
def admin_curator(request):
    # ваш существующий код без изменений
    user = request.user
    if not hasattr(user, 'curator'):
        return redirect('login')
    curator = user.curator

    groups = curator.students.values_list('group', flat=True).distinct()
    sel = request.GET.get('group')
    credit_form = None
    if sel:
        credit_form = CreditForm(request.POST or None)
        credit_form.fields['student'].queryset = curator.students.filter(group=sel)
        if request.method == 'POST' and credit_form.is_valid():
            st, amt = credit_form.cleaned_data['student'], credit_form.cleaned_data['amount']
            Transfer.objects.create(from_user=user, to_student=st, amount=amt, currency='PC')
            st.polycoin_balance += amt
            st.save()
            return redirect(f"{request.path}?group={sel}")

    transfers = Transfer.objects.filter(from_user=user, currency='PC').order_by('-created_at')
    return render(request, 'bank/AdminCurator.html', {
        'curator': curator,
        'groups': groups,
        'selected_group': sel,
        'credit_form': credit_form,
        'transfers': transfers,
    })

@login_required
def cancel_transfer(request, pk):
    # ваш существующий код без изменений
    user = request.user
    if not hasattr(user, 'curator'):
        return redirect('login')
    tr = get_object_or_404(Transfer, pk=pk, from_user=user, currency='PC', canceled=False)
    if timezone.now() - tr.created_at <= timedelta(minutes=15):
        st = tr.to_student
        st.polycoin_balance -= tr.amount
        st.save()
        tr.canceled = True
        tr.canceled_at = timezone.now()
        tr.save()
    return redirect('admin_curator')

@login_required
def student_bank(request):
    # проверка роли студента и логика переводов/конвертации
    user = request.user
    if not hasattr(user, 'student'):
        return redirect('login')
    student = user.student

    transfer_form   = TransferForm(request.POST or None)
    conversion_form = ConversionForm(request.POST or None)
    action = request.POST.get('action')

    if request.method == 'POST':
        if action == 'convert' and conversion_form.is_valid():
            amt  = conversion_form.cleaned_data['amount']
            dirn = conversion_form.cleaned_data['direction']
            if dirn == 'pc_to_kzt':
                if student.polycoin_balance >= amt:
                    student.polycoin_balance -= amt
                    student.kzt_balance      += amt * Decimal('10')
                else:
                    conversion_form.add_error('amount', 'Недостаточно PolyCoin')
            else:
                if student.kzt_balance >= amt:
                    student.kzt_balance      -= amt
                    student.polycoin_balance += amt / Decimal('10')
                else:
                    conversion_form.add_error('amount', 'Недостаточно KZT')
            if not conversion_form.errors:
                student.save()
                return redirect('student_bank')

        if action == 'transfer' and transfer_form.is_valid():
            phone, amt, curr = (
                transfer_form.cleaned_data['phone'],
                transfer_form.cleaned_data['amount'],
                transfer_form.cleaned_data['currency'],
            )
            try:
                rec = Student.objects.get(phone_number=phone)
            except Student.DoesNotExist:
                transfer_form.add_error('phone', 'Студент не найден')
            else:
                if curr == 'KZT':
                    if student.kzt_balance < amt:
                        transfer_form.add_error('amount', 'Недостаточно KZT')
                    else:
                        student.kzt_balance -= amt
                        rec.kzt_balance     += amt
                else:
                    if student.polycoin_balance < amt:
                        transfer_form.add_error('amount', 'Недостаточно PolyCoin')
                    else:
                        student.polycoin_balance -= amt
                        rec.polycoin_balance     += amt
                if not transfer_form.errors:
                    student.save()
                    rec.save()
                    Transfer.objects.create(
                        from_user=user,
                        to_student=rec,
                        amount=amt,
                        currency='KZT' if curr=='KZT' else 'PC'
                    )
                    return redirect('student_bank')

    # контекст для талонов
    today = timezone.localdate()
    tickets = Ticket.objects.filter(student=student).order_by('-created_at')
    today_ticket = tickets.filter(created_at__date=today).first()
    show_ticket_id = request.GET.get('show_ticket')

    return render(request, 'bank/StudentsBank.html', {
        'student':         student,
        'transfer_form':   transfer_form,
        'conversion_form': conversion_form,
        'today_ticket':    today_ticket,
        'show_ticket_id':  show_ticket_id,
    })

@login_required
def buy_ticket(request):
    user = request.user
    if not hasattr(user, 'student'):
        return redirect('login')
    student = user.student

    today = timezone.localdate()
    if Ticket.objects.filter(student=student, created_at__date=today).exists():
        return redirect('student_bank')

    if request.method == 'POST':
        curr = request.POST.get('currency')
        if curr == 'PC':
            amt = Decimal('100')  # 100 PolyCoin = 100*10 KZT = 1000 KZT
            if student.polycoin_balance < amt:
                return redirect('student_bank')
            student.polycoin_balance -= amt
        else:
            amt = Decimal('1000') # 1000 KZT
            if student.kzt_balance < amt:
                return redirect('student_bank')
            student.kzt_balance -= amt
        student.save()

        ticket = Ticket.objects.create(student=student, currency=curr, amount=amt)
        return redirect(f"{reverse('student_bank')}?show_ticket={ticket.id}")

    return redirect('student_bank')

@login_required
def use_ticket(request, ticket_id):
    user = request.user
    if not hasattr(user, 'student'):
        return redirect('login')
    ticket = get_object_or_404(Ticket, id=ticket_id, student=user.student)
    if not ticket.used:
        ticket.used    = True
        ticket.used_at = timezone.now()
        ticket.save()
    return redirect('student_bank')

"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from users.models import Curator, Student
from .models import Transfer
from .forms import CreditForm, TransferForm, ConversionForm

@login_required
def admin_curator(request):
    user = request.user
    if not hasattr(user, 'curator'):
        return redirect('login')
    curator = user.curator

    groups = curator.students.values_list('group', flat=True).distinct()
    sel = request.GET.get('group')
    credit_form = None
    if sel:
        credit_form = CreditForm(request.POST or None)
        credit_form.fields['student'].queryset = curator.students.filter(group=sel)
        if request.method=='POST' and credit_form.is_valid():
            st, amt = credit_form.cleaned_data['student'], credit_form.cleaned_data['amount']
            Transfer.objects.create(from_user=user, to_student=st, amount=amt, currency='PC')
            st.polycoin_balance += amt
            st.save()
            return redirect(f"{request.path}?group={sel}")

    transfers = Transfer.objects.filter(from_user=user, currency='PC').order_by('-created_at')
    return render(request, 'bank/AdminCurator.html', {
        'curator': curator,
        'groups': groups,
        'selected_group': sel,
        'credit_form': credit_form,
        'transfers': transfers,
    })

@login_required
def cancel_transfer(request, pk):
    user = request.user
    if not hasattr(user, 'curator'):
        return redirect('login')
    tr = get_object_or_404(Transfer, pk=pk, from_user=user, currency='PC', canceled=False)
    if timezone.now() - tr.created_at <= timedelta(minutes=15):
        st = tr.to_student
        st.polycoin_balance -= tr.amount
        st.save()
        tr.canceled, tr.canceled_at = True, timezone.now()
        tr.save()
    return redirect('admin_curator')

@login_required
def student_bank(request):
    user = request.user
    if not hasattr(user, 'student'):
        return redirect('login')
    student = user.student

    transfer_form   = TransferForm(request.POST or None)
    conversion_form = ConversionForm(request.POST or None)
    action = request.POST.get('action')  # 'convert' или 'transfer'

    if request.method == 'POST':
        # Конвертация
        if action == 'convert' and conversion_form.is_valid():
            amt  = conversion_form.cleaned_data['amount']
            dirn = conversion_form.cleaned_data['direction']
            if dirn == 'pc_to_kzt':
                if student.polycoin_balance >= amt:
                    student.polycoin_balance -= amt
                    student.kzt_balance      += amt * Decimal('10')
                else:
                    conversion_form.add_error('amount', 'Недостаточно PolyCoin')
            else:
                if student.kzt_balance >= amt:
                    student.kzt_balance      -= amt
                    student.polycoin_balance += amt / Decimal('10')
                else:
                    conversion_form.add_error('amount', 'Недостаточно KZT')

            if not conversion_form.errors:
                student.save()
                return redirect('student_bank')

        # Перевод
        if action == 'transfer' and transfer_form.is_valid():
            phone, amt, curr = (
                transfer_form.cleaned_data['phone'],
                transfer_form.cleaned_data['amount'],
                transfer_form.cleaned_data['currency']
            )
            try:
                rec = Student.objects.get(phone_number=phone)
            except Student.DoesNotExist:
                transfer_form.add_error('phone', 'Студент не найден')
            else:
                if curr == 'KZT':
                    if student.kzt_balance < amt:
                        transfer_form.add_error('amount', 'Недостаточно KZT')
                    else:
                        student.kzt_balance   -= amt
                        rec.kzt_balance       += amt
                else:
                    if student.polycoin_balance < amt:
                        transfer_form.add_error('amount', 'Недостаточно PolyCoin')
                    else:
                        student.polycoin_balance   -= amt
                        rec.polycoin_balance       += amt

                if not transfer_form.errors:
                    student.save()
                    rec.save()
                    Transfer.objects.create(
                        from_user=user,
                        to_student=rec,
                        amount=amt,
                        currency='KZT' if curr=='KZT' else 'PC'
                    )
                    return redirect('student_bank')

    return render(request, 'bank/StudentsBank.html', {
        'student':         student,
        'transfer_form':   transfer_form,
        'conversion_form': conversion_form,
    })
"""