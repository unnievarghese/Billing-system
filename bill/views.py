from django.shortcuts import render,redirect
from bill.forms import ordercreateform,orderlinesform,productcreateform,purchasecreateform
from django.views.generic import TemplateView
from bill.models import order,ordelines,product,purchase
from django.db.models import Sum
from datetime import datetime,date
from django.db.models import Q

class ordercreate(TemplateView):
    model=order
    form_class=ordercreateform
    template_name = 'bill/ordercreate.html'
    context={}

    def get(self, request, *args, **kwargs):
        order=self.model.objects.last()
        if order:
            last_bill_number=order.bill_number
            lst=int(last_bill_number.split('-')[1])+1
            bill_number='klyn-'+str(lst)
        else:
            bill_number='klyn-1000'

        form=self.form_class(initial={'bill_number':bill_number})
        self.context['form']=form
        return render(request,self.template_name,self.context)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            bill_number=form.cleaned_data.get('bill_number')
            form.save()
            return redirect('orderlines',bill_number=bill_number)

class orderlines(TemplateView):
    model=ordelines
    form_class=orderlinesform
    template_name = 'bill/orderlines.html'
    context={}
    def get(self, request, *args, **kwargs):
        billnumber=kwargs.get('bill_number')
        form=self.form_class(initial={'bill_number':billnumber})
        self.context['form']=form
        self.context['items'] = self.model.objects.filter(bill_number__bill_number=billnumber)
        self.context['billnum']=billnumber
        total=ordelines.objects.filter(bill_number__bill_number=billnumber).aggregate(Sum('amount'))
        self.context['total']=total['amount__sum']
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            bill_number=form.cleaned_data.get('bill_number')
            p_qty=form.cleaned_data.get('product_quantity')
            product_name=form.cleaned_data.get('product_name')
            ordr=order.objects.get(bill_number=bill_number)
            produc=purchase.objects.get(product__product_name=product_name)
            prdct=product.objects.get(product_name=product_name)
            amount=p_qty *produc.selling_price
            orderlines=self.model(bill_number=ordr,product_name=prdct,product_qty=p_qty,amount=amount)
            orderlines.save()
            return redirect('orderlines',bill_number=ordr)
        else:
            self.context['form']=form
            return render(request,self.template_name,self.context)

class orderlines_delete(TemplateView):

    def get(self, request, *args, **kwargs):
        id=kwargs.get('id')
        bill_number=kwargs.get('bill_number')
        ordelines.objects.get(id=id).delete()
        ordr=order.objects.get(bill_number=bill_number)
        return redirect('orderlines',bill_number=ordr)

class billgenerate(TemplateView):
    model=order
    context={}
    template_name = 'bill/billdisplay.html'
    def get(self, request, *args, **kwargs):
        billnum=kwargs.get('bill_number')
        orderlines=ordelines.objects.filter(bill_number__bill_number=billnum)
        total = ordelines.objects.filter(bill_number__bill_number=billnum).aggregate(Sum('amount'))
        self.context['billnum']=billnum
        self.context['orderlines']=orderlines
        self.context['total']=total['amount__sum']
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        bill_number=kwargs.get('bill_number')
        ordr=self.model.objects.get(bill_number=bill_number)
        total = ordelines.objects.filter(bill_number__bill_number=bill_number).aggregate(Sum('amount'))
        total=total['amount__sum']
        ordr.bill_total=total
        ordr.save()
        return redirect('order')

class productcreate(TemplateView):
    model=product
    template_name = 'bill/productcreate.html'
    context={}
    def get(self, request, *args, **kwargs):
        form=productcreateform
        productlist=self.model.objects.all()
        self.context['productlist']=productlist
        self.context['form']=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=productcreateform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product')

class purchsecreate(TemplateView):
    model=purchase
    form_class = purchasecreateform
    context={}
    template_name = 'bill/purchasecreate.html'
    def get(self, request, *args, **kwargs):
        form=self.form_class
        purchaselist=self.model.objects.all()
        self.context['purchaselist']=purchaselist
        self.context['form']=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase')

class purchasedelete(TemplateView):

    def get(self, request, *args, **kwargs):
        id=kwargs.get('id')
        purchase.objects.get(id=id).delete()
        return redirect('purchase')

class purchaseedit(TemplateView):

    def get(self, request, *args, **kwargs):
        id=kwargs.get('id')
        purchase_obj=purchase.objects.get(id=id)
        form=purchasecreateform(instance=purchase_obj)
        context={}
        context['form']=form
        return render(request,'bill/purchasecreate.html',context)
    def post(self,request, *args, **kwargs):
        id=kwargs.get('id')
        purchase_obj=purchase.objects.get(id=id)
        form=purchasecreateform(request.POST,request.FILES,instance=purchase_obj)
        if form.is_valid():
            form.save()
            return redirect('purchase')

class adminpagecontent(TemplateView):
    template_name = 'bill/admin.html'

    def get(self, request, *args, **kwargs):
        context={}

        #   pie chart

        list, countlist, countvalues, datelist, datevalues= [], [], [], [], []
        areachart=['0','0','0','0','0','0','0','0','0','0','0','0']
        dict = {}
        for object in order.objects.all():
            if object.bill_date not in list:
                list.append(object.bill_date)
        for date in list:
            result = order.objects.filter(bill_date=date).count()
            dict[str(date)] = result
            countlist.append(result)
        dict = sorted(dict, key=dict.get, reverse=True)
        countlist = sorted(countlist, reverse=True)
        for i in range(3):
            countvalues.append(str(countlist[i]))
            datevalues.append(dict[i])
        context['countvalues'] = ','.join((countvalues))
        context['datevalues'] = ','.join((datevalues))
        context['date'] = datevalues

        #   display collection by month,week,day

        cunrent_month = datetime.now().month
        monthly_total = order.objects.filter(bill_date__month=cunrent_month).aggregate(Sum('bill_total'))
        context['month'] = monthly_total['bill_total__sum']
        cunrent_week = date.today().isocalendar()[1]
        weekly_total = order.objects.filter(bill_date__week=cunrent_week).aggregate(Sum('bill_total'))
        context['week'] = weekly_total['bill_total__sum']
        cunrent_day = date.today()
        daily_total = order.objects.filter(bill_date=cunrent_day).aggregate(Sum('bill_total'))
        context['daily'] = daily_total['bill_total__sum']

        #   progress bar

        listofproducts, listofcount = [], []
        product_dict = {}
        for item in product.objects.all():
            listofproducts.append(item.product_name)
        for item in listofproducts:
            solditemcount = 0
            obj = ordelines.objects.filter(Q(product_name__product_name=item) & Q(bill_number__bill_date=cunrent_day))
            for i in obj:
                solditemcount += i.product_qty
                product_dict[item] = solditemcount
        toplist = sorted(product_dict, key=product_dict.get, reverse=True)
        for item in toplist:
            if item in product_dict:
                listofcount.append(product_dict[item])
        if len(toplist) >= 5:
            context['toplist'] = toplist[:5]
        else:
            context['toplist'] = toplist
        context['count'] = listofcount

#      area chart

        areachart[cunrent_month-1]=str(monthly_total['bill_total__sum'])
        context['area']=','.join(areachart)
        print(areachart)
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):

        print('inside admin')
        context={}
        billnum=request.POST['search']
        orderlines = ordelines.objects.filter(bill_number__bill_number=billnum)
        total = ordelines.objects.filter(bill_number__bill_number=billnum).aggregate(Sum('amount'))
        context['billnum'] = billnum
        context['orderlines'] = orderlines
        context['total'] = total['amount__sum']
        return render(request,'bill/billdisplay.html' ,context)

class billlist(TemplateView):
    context={}
    template_name = 'bill/bill_list.html'
    def get(self, request, *args, **kwargs):
        orders=order.objects.all()
        self.context['orders']=orders
        return render(request,self.template_name,self.context)
