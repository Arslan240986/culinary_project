showSubCategory()
function showSubCategory() {
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
    $('.instruction_image_div').click((e) => {
        var next_elemn_div = $(e.target).next()
        var hiden_inputload_image_instractuin = next_elemn_div.children('input[type=file]')
        hiden_inputload_image_instractuin.click()
        hiden_inputload_image_instractuin.change((e) => {
            if ($(e.target).prop('files') && $(e.target).prop('files')[0]) {
                previousImage = next_elemn_div.prev()
                var reader = new FileReader()
                reader.onload = function (e) {
                    var image = e.target.result
                    previousImage.attr({ 'src': image })
                }
                reader.readAsDataURL($(e.target).prop('files')[0])
            }
        })
    })

})

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


var outerFormset = $("fieldset.ingredient_form_set").not('.ui.negative.message')
    .djangoFormset({
        on: {
            formInitialized: function (event, form) {
                /* Init inner formset */
                var innerFormsetElem = form.elem.children('div.ingredient_block');

                var innerFormset = innerFormsetElem.children('div').djangoFormset({
                    deleteButtonText: '<i class="ui big times circle red icon cursor"></i>',
                });

                innerFormsetElem.on('click', '[data-action=add-inner-ingredient-form]', function (event) {
                    innerFormset.addForm();
 
                });

            },
        },
        deleteButtonText: '<i class="ui big times circle red icon cursor"></i>',
    });

/* Add new outer form on add button click */
$('form').on('click', '[data-action=add-outer-ingredient-form]', function (event) {
    outerFormset.addForm();
});
$(function () {
    var formset = $('div.inline.instruction_visible').djangoFormset({
        deleteButtonText: '<i class="ui big times circle red icon cursor"></i>',
    });

    $('form').on('click', '[data-action=add-form-to-instruction]', function (event) {
        formset.addForm();
        // Show on temporary window image which was selected
        $('.instruction_image_div').click((e) => {
            var next_elemn_div = $(e.target).next()
            var hiden_inputload_image_instractuin = next_elemn_div.children('input[type=file]')
            hiden_inputload_image_instractuin.click()

            hiden_inputload_image_instractuin.change((e) => {
                if ($(e.target).prop('files') && $(e.target).prop('files')[0]) {
                    previousImage = next_elemn_div.prev()
                    var reader = new FileReader()
                    reader.onload = function (e) {
                        var image = e.target.result
                        previousImage.attr({ 'src': image })
                    }
                    reader.readAsDataURL($(e.target).prop('files')[0])
                }
            })
        })
        // <!--  Hovering on instruction image          -->
        $('.instruction_image_div').mouseover((e) => {
            $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'block', })
        })
        $('.instruction_image_div').mouseout((e) => {
            $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'none', })
        })
    });
});