from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer


def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})


@login_required
def customer_list(request):
   customer = Customer.objects.filter(created_date__lte=timezone.now())
   return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
       # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock = form.save()
            # stock.customer = stock.id
            stock.updated_date = timezone.now()
            stock.save()
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
    else:
        # print("else")
        form = StockForm(instance=stock)
    return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
    return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def investment_list(request):
    investments = Investment.objects.filter(acquired_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})


@login_required
def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == "POST":
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            investment = form.save()
            # investment.customer = investment.id
            investment.updated_date = timezone.now()
            investment.save()
            investments = Investment.objects.filter(acquired_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html', {'investments': investments})
    else:
        # print("else")
        form = InvestmentForm(instance=investment)
    return render(request, 'portfolio/investment_edit.html', {'form': form})


@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    investments = Investment.objects.filter(acquired_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def portfolio(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutualfunds = MutualFund.objects.filter(customer=pk)
    sum_stock_initial_value = 0.0
    sum_stock_current_value = 0.0
    portfolio_initial_invest = 0.0
    portfolio_current_invest = 0.0
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(recent_val_total=Sum('recent_value'))[
        'recent_val_total']
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(acquired_val_total=Sum('acquired_value'))[
        'acquired_val_total']
    if sum_recent_value is None or sum_acquired_value is None:
        investment_result = 0.0
    else:
        investment_result = float(sum_recent_value) - float(sum_acquired_value)
    for stock in stocks:
        sum_stock_initial_value = sum_stock_initial_value + float(stock.initial_stock_value())
        sum_stock_current_value = sum_stock_current_value + float(stock.current_stock_value())
    if sum_stock_current_value is None or sum_stock_initial_value is None:
        stock_result = 0.0
    else:
        stock_result = float(sum_stock_current_value) - float(sum_stock_initial_value)
    sum_initial_mf_value = MutualFund.objects.filter(customer=pk).aggregate(initial_mf_total=Sum('invested_value'))[
        'initial_mf_total']
    sum_current_mf_value = MutualFund.objects.filter(customer=pk).aggregate(current_mf_total=Sum('current_value'))[
        'current_mf_total']
    if sum_current_mf_value is None or sum_initial_mf_value is None:
        mf_result = 0.0
    else:
        mf_result = float(sum_current_mf_value) - float(sum_initial_mf_value)
    if sum_acquired_value is not None:
        portfolio_initial_invest = float(portfolio_initial_invest) + float(sum_acquired_value)
    if sum_stock_initial_value is not None:
        portfolio_initial_invest = float(portfolio_initial_invest) + float(sum_stock_initial_value)
    if sum_initial_mf_value is not None:
        portfolio_initial_invest = float(portfolio_initial_invest) + float(sum_initial_mf_value)
    if sum_recent_value is not None:
        portfolio_current_invest = float(portfolio_current_invest) + float(sum_recent_value)
    if sum_stock_current_value is not None:
        portfolio_current_invest = float(portfolio_current_invest) + float(sum_stock_current_value)
    if sum_current_mf_value is not None:
        portfolio_current_invest = float(portfolio_current_invest) + float(sum_current_mf_value)
    grand_result = float(portfolio_current_invest) - float(portfolio_initial_invest)
    return render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                        'stocks': stocks, 'mutualfunds': mutualfunds,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_acquired_value': sum_acquired_value,
                                                        'investment_result': investment_result,
                                                        'sum_stock_current_value': sum_stock_current_value,
                                                        'sum_stock_initial_value': sum_stock_initial_value,
                                                        'stock_result': stock_result,
                                                        'sum_initial_mf_value': sum_initial_mf_value,
                                                        'sum_current_mf_value': sum_current_mf_value,
                                                        'mf_result': mf_result,
                                                        'portfolio_initial_invest': portfolio_initial_invest,
                                                        'portfolio_current_invest': portfolio_current_invest,
                                                        'grand_result': grand_result,
                                                        'customer': customer, })



# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)



@login_required
def mutualfund_list(request):
    mutualfunds = MutualFund.objects.filter(purchase_date__lte=timezone.now())
    return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})


@login_required
def mutualfund_new(request):
   if request.method == "POST":
       form = MutualFundForm(request.POST)
       if form.is_valid():
           mutualfund = form.save(commit=True)
           mutualfund.created_date = timezone.now()
           mutualfund.save()
           mutualfunds = MutualFund.objects.all()
           return render(request, 'portfolio/mutualfund_list.html',
                         {'mutualfunds': mutualfunds})
   else:
       form = MutualFundForm()
       # print("Else")
   return render(request, 'portfolio/mutualfund_new.html', {'form': form})


@login_required
def mutualfund_edit(request, pk):
    mutualfund = get_object_or_404(MutualFund, pk=pk)
    if request.method == "POST":
       form = MutualFundForm(request.POST, instance=mutualfund)
       if form.is_valid():
           mutualfund = form.save()
           # stock.customer = stock.id
           mutualfund.updated_date = timezone.now()
           mutualfund.save()
           mutualfunds = MutualFund.objects.all()
           return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})
    else:
       # print("else")
       form = MutualFundForm(instance=mutualfund)
    return render(request, 'portfolio/mutualfund_edit.html', {'form': form})


@login_required
def mutualfund_delete(request, pk):
    mutualfund = get_object_or_404(MutualFund, pk=pk)
    mutualfund.delete()
    mutualfunds = MutualFund.objects.all()
    return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})