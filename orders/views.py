from django.shortcuts import render
from django.http import JsonResponse
from .models import ProductInBasket, ProductInOrder, Order
from .forms import CheckoutContactForm
from django.contrib.auth.models import User


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    is_delete = data.get('is_delete')

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(
            session_key=session_key,
            is_active=True,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        if not created:
            new_product.quantity += int(quantity)
            new_product.save(force_update=True)

    # common code for two cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_quantity = products_in_basket.count()
    return_dict['products_total_quantity'] = products_total_quantity

    return_dict['products'] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict['id'] = item.id
        product_dict['item'] = item.product.name
        product_dict['price_per_item'] = item.price_per_item
        product_dict['quantity'] = item.quantity
        return_dict['products'].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key

    products_in_basket = ProductInBasket.objects.filter(
        session_key=session_key,
        is_active=True,
        order__isnull=True
    )

    form = CheckoutContactForm(request.POST or None)

    if request.POST:
        print(request.POST)
        if form.is_valid():
            print('That ok!')
            data = request.POST
            name = data.get("name", )
            phone = data['phone']
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(
                user=user,
                customer_name=name,
                customer_phone=phone,
                status_id=1
            )

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    product_in_basket.quantity = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(
                        product=product_in_basket.product,
                        quantity=product_in_basket.quantity,
                        price_per_item=product_in_basket.price_per_item,
                        total_price=product_in_basket.total_price,
                        order=order
                    )

        else:
            print('Fuck')
    return render(request, 'orders/checkout.html', locals())
