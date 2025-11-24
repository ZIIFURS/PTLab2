from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from .models import Product, Purchase


def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['person', 'address']
    template_name = 'shop/purchase_form.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.product = get_object_or_404(Product, id=kwargs['product_id'])

    def dispatch(self, request, *args, **kwargs):
        if not self.product.can_be_purchased():
            return render(request, 'shop/out_of_stock.html', {
                'product': self.product
            }, status=400)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        purchase = form.save(commit=False)
        purchase.product = self.product
        purchase.save()

        # Уменьшаем количество товара
        self.product.decrease_quantity()

        return render(self.request, 'shop/purchase_success.html', {
            'person': purchase.person,
            'product': self.product
        })