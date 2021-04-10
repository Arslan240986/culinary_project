
$(document).ready(function () {
    $('.parent_category').change(function (e) {
        $('.sub_category').addClass('active');
        $('.category').addClass('active');
        $('.category').empty()
        event.preventDefault();
        var pk = $('.parent_category').val()
        const url = $('.parent_category').attr('data-href-template')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: 'GET',
            url: url,
            data: { 'id': pk, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function (response) {
                if (response.length > 0) {
                    $('.sub_category').removeClass('active');
                    html_data = '<option value="" selected="True">---------</option>'
                    response.forEach(function (subcats) {
                        html_data += `<option value="${subcats.id}">${subcats.name}</option>`
                    })
                    $('.sub_category').html(html_data)
                }
            },
            error: function (rs, e) {
                console.log('second', rs.responseText);
            },
        });
    })
    $('.sub_category').change(function (e) {
        event.preventDefault();
        var pk = $('.sub_category').val()
        const url = $('.parent_category').attr('data-href-template')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: 'GET',
            url: url,
            data: { 'id': pk, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function (response) {
                if (response.length > 0) {
                    $('.category').removeClass('active');
                    html_data = '<option value="" selected="True">---------</option>'
                    response.forEach(function (subcats) {
                        html_data += `<option value="${subcats.id}">${subcats.name}</option>`
                    })
                    $('.category').html(html_data)
                }
            },
            error: function (rs, e) {
                console.log('second', rs.responseText);
            },
        });
    })
    // shows list of ingredients when user focus on input 

    $('.form-control.dish_ingredient_name').on('focus', (e) => {
        var ch = document.getElementById('id_ingredient_set-0-name')
        const url = $(e.target).parent().attr('data-href')
        var input = $(e.target);
        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',

            success: function (response) {
                var ingredients = response
                var list = $(e.target).next('#autocomplete_list')
                list.html(getComliteHtml(response));
                list.removeClass('d_none');
                // positionList();
                $(document).on('click', (event) => {
                    var targ = event.target //Элемент, на котором произошло событие
                    if ($(event.target).parent().attr('id') === list.attr('id')) {
                        console.log(list.prev())
                        list.prev().val(targ.innerHTML);
                        list.addClass('d_none');
                    }else {
                        ClearAutoCompleteWindows()
                        $(document).off("click")
                    }
                });
                $(e.target).keyup(() => {
                    var val = input.val().trim().toLowerCase();
                    console.log(val)
                    if (val) {
                        var words = ingredients.filter(function (item) {
                            return item.toLowerCase().indexOf(val) === 0;
                        });
                        list.html(getComliteHtml(words));
                        list.removeClass('d_none');
                        // positionList();
                    } else {
                        list.html(getComliteHtml(response));
                        list.removeClass('d_none');

                    }
                })
                function getComliteHtml(words) {
                    var html = "";
                    for (var i = 0; i < words.length; i++) {
                        html += '<div>' + words[i] + '</div>'
                    }
                    return html;
                }
                console.log(response)
            },

            error: function (rs, e) {
                console.log(rs.responseText);
            },
        });
    })
})
// function that sets d_none class on autocomplete popups windows when blur input
function ClearAutoCompleteWindows() {
    var div_lists = document.querySelectorAll('#autocomplete_list')
    div_lists.forEach((e) => {
        if (e.getAttribute('class') == 'd_none') {
        } else {
            e.setAttribute('class', 'd_none')
        }

    })
}