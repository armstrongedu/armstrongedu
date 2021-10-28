from armstrong.celery import app


@app.task
def update_daily():
    from django.db.models import Sum

    from dashboard.models import UpdatedDaily
    from payment.models import Invoice, Membership, MembershipType


    UpdatedDaily.objects.create(
        total_gross_sales=Invoice.objects.aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_number_of_customers=Membership.objects.count(),
        total_sales_egypt=Invoice.objects.filter(country=MembershipType.EGYPT).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_qatar=Invoice.objects.filter(country=MembershipType.QATAR).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_bahrain=Invoice.objects.filter(country=MembershipType.BAHRAIN).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_saudi_arabia=Invoice.objects.filter(country=MembershipType.SAUDI_ARABIA).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_united_arab_emirates=Invoice.objects.filter(country=MembershipType.UNITED_ARAB_EMIRATES).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_jordan=Invoice.objects.filter(country=MembershipType.JORDAN).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_kuwait=Invoice.objects.filter(country=MembershipType.KUWAIT).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_oman=Invoice.objects.filter(country=MembershipType.OMAN).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_sales_international=Invoice.objects.filter(country=MembershipType.INTERNATIONAL).aggregate(Sum('billed'))['billed__sum'] or 0.0,
    )

@app.task
def update_monthly():
    from datetime import timedelta

    from django.db.models import Sum
    from django.utils.timezone import now
    from django.contrib.auth import get_user_model

    from dashboard.models import UpdatedMonthly
    from payment.models import Invoice, Membership, MembershipType

    last_month = (now().replace(day=1)-timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0)

    UpdatedMonthly.objects.create(
        date=last_month.date().strftime('%B'),
        total_gross_sales=Invoice.objects.filter(created_at__gte=last_month).aggregate(Sum('billed'))['billed__sum'] or 0.0,
        total_number_of_customers=Membership.objects.filter(activated_on__gte=last_month).count(),
        total_number_of_registers=get_user_model().objects.filter(date_joined__gte=last_month).count(),
    )

@app.task
def update_daily_promocode():
    from datetime import timedelta

    from django.db.models import Sum
    from django.utils.timezone import now
    from django.contrib.auth import get_user_model

    from dashboard.models import UpdatedDailyPromocode
    from payment.models import Invoice, Membership, MembershipType, Promocode

    for promocode in Promocode.objects.all():
        dashboard_promocode, _ = UpdatedDailyPromocode.objects.get_or_create(
            promocode_name=promocode.promocode,
            defaults={'total_sales':0.0},
        )
        dashboard_promocode.total_sales = Invoice.objects.filter(promocode_name=promocode.promocode).aggregate(Sum('billed'))['billed__sum'] or 0.0
        dashboard_promocode.save()


@app.task
def update_daily_membershiptype():
    from datetime import timedelta

    from django.db.models import Sum
    from django.utils.timezone import now
    from django.contrib.auth import get_user_model

    from dashboard.models import UpdatedDailyMembershipType
    from payment.models import Invoice, Membership, MembershipType, Promocode, MembershipType

    for membership_type in MembershipType.objects.all():
        dashboard_membership_type, _ = UpdatedDailyMembershipType.objects.get_or_create(
            name=membership_type.name,
            defaults={'total_sales':0.0},
        )
        dashboard_membership_type.total_sales = Invoice.objects.filter(item_name=membership_type.name).aggregate(Sum('billed'))['billed__sum'] or 0.0
        dashboard_membership_type.save()
