$(document).ready(function () {
    console.log($(window))
    //<!--        Semantic ui checkbox and dropdown -->
    $('.max.example ui.normal.dropdown').dropdown({ maxSelections: 3 });
    $('.my_dropdown').dropdown();
    $('.ui.toggle.checkbox').checkbox();
    //        <!--Dependence dropdown-->
    $('#id_category').change(function (e) {
        event.preventDefault();
        $('#id_sub_category').children().remove()
        $('#id_sub_category').siblings('div .text').html('---------')
        var pk = $('#id_category').val()
        const url = $('.recipe_box_category').attr('data-href-template')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: 'GET',
            url: url,
            data: { 'category_id': pk, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function (response) {
                if (response.length > 0) {
                    option = '<option value="" selected="True">---------</option>'
                    response.forEach(function (subcats) {
                        option += `<option value="${subcats.id}">${subcats.name}</option>`
                    })
                    $('#id_sub_category').append(option)
                } else {
                    $('#id_sub_category').children().remove()
                }
            },
            error: function (rs, e) {
                console.log(rs.responseText);
            },
        });
    });
    //<!--on click poster image start image downloader-->
    $('#poster_image_id').click(() => {
        $('#id_poster').click()
    })
    // Hover on image show icons
    $('#poster_image_id').mouseover(() => {
        $('.form__add-img').css({ 'display': 'block' })
    })
    $('#poster_image_id').mouseout(() => {
        $('.form__add-img').css({ 'display': 'none' })
    })
    $('.instruction_image_div').mouseover((e) => {
        $(e.target).siblings('.form__add-img-instr').css({ 'display': 'block', })
    })
    $('.instruction_image_div').mouseout((e) => {
        $(e.target).siblings('.form__add-img-instr').css({ 'display': 'none', })
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
                        list.prev().val(targ.innerHTML);
                        list.addClass('d_none');
                    }else {
                        ClearAutoCompleteWindows()
                        $(document).off("click")
                    }
                });
                $(e.target).keyup(() => {
                    var val = input.val().trim().toLowerCase();
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
//<!--Show image on temporary window-->
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader()
        reader.onload = function (e) {
            var image = e.target.result
            var imageField = document.getElementById('poster_image_id')
            imageField.src = image
        }
        reader.readAsDataURL(input.files[0])
    }
}

//<!--open file selector instruction image-->
function clickImageFile(input) {
    input.nextElementSibling.click()
}
//<!--Show instruction image on temporary window-->
function readURLInstrcution(input) {
    if (input.files && input.files[0]) {
        previousImage = input.previousElementSibling
        var reader = new FileReader()
        reader.onload = function (e) {
            var image = e.target.result
            previousImage.src = image
        }
        reader.readAsDataURL(input.files[0])
    }
}

