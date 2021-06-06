showSubCategory()
function showSubCategory(){
    //        <!--Dependence dropdown-->
    $('#id_category').change(function (e) {
        e.preventDefault();
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
}
showListOfIngredient()
function showListOfIngredient(){
    // shows list of ingredients when user focus on input
    $('.form-control.dish_ingredient_name').on('focus', (e) => {
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
                if (input.val()){
                    var val = input.val().trim().toLowerCase();
                    keyUp(val)
                }
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
                    keyUp(val)
                })
                function keyUp(val){
                        if (val) {
                            var words = ingredients.filter(function (item) {
                                return item.toLowerCase().indexOf(val) === 0;
                            });
                            console.log(val)
                            list.html(getComliteHtml(words));
                            list.removeClass('d_none');
                            if(val && words.length == 0){
                                list.addClass('d_none');
                            }
                            // positionList();
                        } else {
                            list.html(getComliteHtml(response));
                            list.removeClass('d_none');

                        }
                    
                }
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
}
$(document).ready(function () {
    //<!--        Semantic ui checkbox and dropdown -->
    $('.max.example ui.normal.dropdown').dropdown({ maxSelections: 3 });
    $('.my_dropdown').dropdown();
    $('.ui.toggle.checkbox').checkbox();

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
        $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'block', })
    })
    $('.instruction_image_div').mouseout((e) => {
        $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'none', })
    })
    
    // Show on temporary window image which was selected
    $('.instruction_image_div').click((e)=>{
        var next_elemn_div = $(e.target).next()
        var hiden_inputload_image_instractuin = next_elemn_div.children('input[type=file]')
        hiden_inputload_image_instractuin.click()

        hiden_inputload_image_instractuin.change((e)=>{
            if ($(e.target).prop('files') && $(e.target).prop('files')[0]) {
                previousImage = next_elemn_div.prev()
                var reader = new FileReader()
                reader.onload = function (e) {
                    var image = e.target.result
                    previousImage.attr({'src': image})
                }
                reader.readAsDataURL($(e.target).prop('files')[0])
            }
        })
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

