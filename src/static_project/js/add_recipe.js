$(document).ready(function(){
//<!--        Semantic ui checkbox and dropdown -->
        $('.max.example ui.normal.dropdown').dropdown({maxSelections: 3});
        $('.my_dropdown').dropdown();
        $('.ui.toggle.checkbox').checkbox();
//        <!--Dependence dropdown-->
        $('#id_category').change(function(e){
            event.preventDefault();
            $('#id_sub_category').children().remove()
            $('#id_sub_category').siblings('div .text').html('---------')
                var pk = $('#id_category').val()
                const url = $('.recipe_box_category').attr('data-href-template')
                let csrf = $('input[name=csrfmiddlewaretoken]').val()
                $.ajax({
                    type: 'GET',
                    url: url,
                    data: {'category_id': pk, 'csrfmiddlewaretoken': csrf },
                    dataType: 'json',
                    success: function(response){
                    if(response.length > 0){
                        option = '<option value="" selected="True">---------</option>'
                        response.forEach(function(subcats){
                            option += `<option value="${subcats.id}">${subcats.name}</option>`
                            })
                        $('#id_sub_category').append(option)
                    } else {
                        $('#id_sub_category').children().remove()
                    }
                    },
                    error: function(rs, e){
                        console.log(rs.responseText);
                    },
                });
        });
//<!--on click poster image start image downloader-->
        $('#poster_image_id').click(()=>{
            $('#id_poster').click()
        })
        // Hover on image show icons
        $('#poster_image_id').mouseover(()=>{
            $('.form__add-img').css({'display':'block'})  
        })
        $('#poster_image_id').mouseout(()=>{
          $('.form__add-img').css({'display':'none'})  
        })
        $('.instruction_image_div').mouseover((e)=>{
            $(e.target).siblings('.form__add-img-instr').css({'display': 'block',})
        })
        $('.instruction_image_div').mouseout((e)=>{
            $(e.target).siblings('.form__add-img-instr').css({'display': 'none',})
        })
})
//<!--Show image on temporary window-->
function readURL(input){
    if(input.files && input.files[0]){
        var reader = new FileReader()
        reader.onload = function (e){
            var image = e.target.result
            var imageField = document.getElementById('poster_image_id')
            imageField.src = image
       }
       reader.readAsDataURL(input.files[0])
    }
}

//<!--open file selector instruction image-->
function clickImageFile(input){
    input.nextElementSibling.click()
}
//<!--Show instruction image on temporary window-->
function readURLInstrcution(input){
    if(input.files && input.files[0]){
        previousImage = input.previousElementSibling
        var reader = new FileReader()
        reader.onload = function (e){
            var image = e.target.result
            previousImage.src = image
       }
       reader.readAsDataURL(input.files[0])
    }
}

