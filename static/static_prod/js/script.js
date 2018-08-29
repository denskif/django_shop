$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

    function basketUpdating(product_id, quantity, is_deleted){
        var data = {};
            data.product_id = product_id;
            data.quantity = quantity;
            var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;

            if (is_deleted){
                data['is_delete'] = true;
            }

            var url = form.attr('action');

            console.log(data);

            $.ajax({
                url:url,
                type: 'POST',
                data: data,
                cache: true,
                success: function(data){
                    console.log('OK!');
                    console.log(data.products_total_quantity);
                    if (data.products_total_quantity || data.products_total_quantity == 0){
                        $('#basket_total_quantity').text("("+ data.products_total_quantity +")");
                        console.log(data.products);
                        $('.basket-items ul').html("");
                        $.each(data.products, function(k, v){
                            $('.basket-items ul').append('<li>'+ v.item +' ' + v.quantity + ' шт. по '+ v.price_per_item + ' UAH  ' +
                                '<a class="delete-item" href="" data-product_id="'+v.id+'">X</a>' +
                                '</li>');
                        });
                    }
                },
                error: function(){
                    console.log('error')
                }
            })
    }

    form.on('submit', function(e){
        e.preventDefault();
        console.log('123');
        var quantity = $('#number').val();
        console.log(quantity);
        var submit_btn = $('#submit_btn');
        var product_id = submit_btn.data('product_id');
        var product_name = submit_btn.data('name');
        var product_price = submit_btn.data('price');
        console.log(product_id);
        console.log(product_name);
        console.log(product_price);

        basketUpdating(product_id, quantity, is_deleted=false)

    });

    function ToggleBasket(){
       $('.basket-items').removeClass('hidden');
    }


    $('.basket-container').on('click', function(e){
        e.preventDefault();
        ToggleBasket();
    });

    $('.basket-container').mouseover(function(){
        ToggleBasket();
    });

    // $('.basket-container').mouseout(function(){
    //     ToggleBasket();
    // });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        quantity = 0;
        basketUpdating(product_id, quantity, is_deleted=true)
    })


    function calculatingBasketAmount() {
        var total_order_amount = 0.00;
        $('.total-product-in-basket-amount').each(function() {
            total_order_amount += parseFloat($(this).text());
        });
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-quantity", function () {
        var current_quantity = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        var total_amount = parseFloat(current_quantity * current_price).toFixed(2);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculatingBasketAmount();
    })

    calculatingBasketAmount();

});