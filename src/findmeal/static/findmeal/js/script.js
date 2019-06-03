$(document).ready(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Rounds numbers to nearest 0.5
    function roundHalf(num) {
        return Math.round(parseFloat(num) * 2) / 2;
    }

    var pan = [];

    var options = {
        max_value: 5,
        step_size: 1,
        cursor: 'pointer',
        ajax_method: 'POST',
        url: $(".rate").attr('action'),
        initial_value: roundHalf($("#current-rating").val()),
    }

    $(".rate").rate(options);

    $(".rate").on("updateSuccess", function(ev, data) {
        $(".rate").rate("setValue", roundHalf(data), 1);
    });

    $(".rate").on("updateError", function(ev, jxhr, msg, err) {
        alert("Bir hata oluştu; lütfen daha sonra tekrar deneyin!");
    });

    if (document.getElementById("search-ingredient-input") != null) {
        autocomplete(document.getElementById("search-ingredient-input"));
    }

    $.extend({
        el: function(el, props) {
            var $el = $(document.createElement(el));
            $el.attr(props);
            return $el;
        }
    });

    function generateItem(ingredientId, ingredientName) {
        if (pan.includes(ingredientName) == false) {
            pan.push(ingredientName);

            $("#content").append(
                $.el('div', {
                    'class': 'card bg-light ingredient-item'
                }).append(
                    $.el('div', {
                        'class': 'card-body position-relative'
                    }).append(
                        $.el('button', {
                            'class': 'close close-ingredient',
                            'aria-label': 'Close'
                        }).append(
                            $.el('span', {
                                'aria-hidden': 'true'
                            }).html('&times;')
                        )
                    )
                    .append(
                        $.el('p', {
                            'class': 'card-text'
                        }).text(ingredientName)
                    )
                    .append(
                        $.el('input', {
                            'type': 'hidden',
                            'name': 'i',
                            'class': 'ingredient',
                            'value': ingredientId
                        })
                    )
                )
            );
        }
    }

    $(document).on("click", "div.autocomplete-item", function() {
        var ingredientId = $(this).children().eq(1).val();
        var ingredientName = $(this).children().eq(2).val();
        generateItem(ingredientId, ingredientName);
        $("#search-button").prop("disabled", false);
    });

    $("#content").on("click", ".close-ingredient", function(e) {
        e.preventDefault();
        $(this).parent().parent().fadeOut(300, function() {
            $(this).remove();
        });
        var index = pan.indexOf($(this).next().text());
        if (index > -1) {
            pan.splice(index, 1);
        }
        if (!pan.length) {
            $("#search-button").prop("disabled", true);
        }

    });

    $(".list-group > a").hover(function() {
        $(this).toggleClass("active");
    });

});
