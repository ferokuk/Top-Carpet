$(document).ready(function () {
    let cur_size_id = $("#first_size").val();
    $('.zoom-image').on('mousemove', function (event) {
        const imageContainer = $(this).parent();
        const zoomImage = $(this);
        const containerOffset = imageContainer.offset();
        const imageOffset = zoomImage.offset();
        const containerWidth = imageContainer.width();
        const containerHeight = imageContainer.height();
        const x = ((event.pageX - containerOffset.left) / containerWidth) * 100;
        const y = ((event.pageY - containerOffset.top) / containerHeight) * 100;

        zoomImage.css('transform-origin', `${x}% ${y}%`);
    });

    $('.zoom-image').on('mouseleave', function () {
        $(this).css('transform-origin', 'center center');
    });
    $('[data-toggle="tooltip"]').tooltip();
    $(document).on("click", ".decrement", function () {
        let url = $(this).data("cart-change-url");
        let cartID = $(this).data("cart-id");
        let $input = $(this).closest('.btn-group').find('.number');
        let currentValue = parseInt($input.val());
        let phone = $("#phone").val();
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            updateCart(cartID, currentValue - 1, -1, url, phone);
        }
    });

    $(document).on("click", ".increment", function () {
        let url = $(this).data("cart-change-url");
        let cartID = $(this).data("cart-id");
        let phone = $("#phone").val();
        let input = $(this).closest('.btn-group').find('.number');
        let currentValue = parseInt(input.val());

        input.val(currentValue + 1);

        updateCart(cartID, currentValue + 1, 1, url, phone);
    });

    $(document).on("click", "#addToCart", function (e) {
        let size_id = cur_size_id;
        let add_to_cart_url = $(this).data("url");
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                carpet_size_id: size_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                show_success_toast(data)

            },

            error: function (data) {
                show_error_toast()
            },
        });
    })

    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        let cart_id = $(this).data("cart-id");
        let remove_from_cart_link = $(this).attr("href");
        let phone = $("#phone").val();
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: remove_from_cart_link,
            data: {
                cart_id: cart_id,
                phone: phone,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                show_success_toast(data)
                $("#cart_items_list").html(data.cart_items_html);

            },

            error: function (data) {
                show_error_toast()
            },
        });
    });


    $(document).on("click", ".size-btn", function (e) {
        let size_id = $(this).data("size-id");
        let url = $(this).data("url");
        $('.size-btn').removeClass('active-orange-bg').addClass('btn-secondary');
        $(this).removeClass('btn-secondary').addClass('active-orange-bg');
        cur_size_id = size_id;
        $.ajax({
            type: "POST",
            url: url,
            data: {
                size_id: size_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                $("#price").text(data.price)
                $("#quantity").text(data.quantity)
                $("#quantity_inner").toggleClass("text-danger", data.quantity <= 3);
                $("#waiting_days").toggleClass("d-none", data.quantity != 0);
                $("#addToCart").prop('disabled', data.quantity == 0)
            },

            error: function (data) {
                show_error_toast()
            },
        });

    });

    $(document).on("click", ".add-to-fav", function (e) {
        e.preventDefault();
        console.log("fdff")
        let carpet_id = $(this).data("carpet-id")
        let url = $(this).data("url")
        if ($(this).hasClass("btn-outline-danger")) {

            $(this).removeClass("btn-outline-danger").addClass("btn-danger");
        } else {

            $(this).removeClass("btn-danger").addClass("btn-outline-danger");
        }
        $.ajax({
            type: "POST",
            url: url,
            data: {
                carpet_id: carpet_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                show_success_toast(data)
            },

            error: function (data) {
                show_error_toast()
            },
        });
    });

    function show_success_toast(data) {
        let toastHTML =
            `<div class="toast bg-dark" role="alert" \
                aria-live="assertive" aria-atomic="true" data-delay="5000"> \
                        <div class="toast-header active-orange-bg"> \
                            <strong class="mr-auto">${data.type}</strong> \
                            <small>Только что</small> \
                            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close"> \
                                <span aria-hidden="true">&times;</span> \
                            </button> \
                        </div> \
                        <div class="toast-body"> \
                            ${data.message}. \
                        </div> \
            </div>
`;
        // Добавление toast на страницу
        $('.toast-container').append(toastHTML);
        // Инициализация отображения toast
        let toast = $('.toast');
        toast.toast('show');
        // Удаление toast из DOM после его исчезновения
        toast.on('hidden.bs.toast', function () {
            $(this).remove();
        });
    }

    function show_error_toast() {
        var toastHTML =
            '<div class="toast bg-dark" role="alert" \
            aria-live="assertive" aria-atomic="true" data-delay="5000"> \
                    <div class="toast-header"> \
                        <strong class="mr-auto">Ошибка</strong> \
                        <small>Только что</small> \
                        <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close"> \
                            <span aria-hidden="true">&times;</span> \
                        </button> \
                    </div> \
                    <div class="toast-body"> \
                        Произошла ошибка при выполнении действия. \
                    </div> \
                </div>';
        // Добавление toast на страницу
        $('.toast-container').append(toastHTML);
        // Инициализация отображения toast
        var toast = $('.toast');
        toast.toast('show');
        // Удаление toast из DOM после его исчезновения
        toast.on('hidden.bs.toast', function () {
            $(this).remove();
        });
    }

    function updateCart(cartID, quantity, change, url, phone) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                phone: phone,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {

                $("#cart_items_list").html(data.cart_items_html);

            },
            error: function (data) {
                show_error_toast()
            },
        });
    }
})