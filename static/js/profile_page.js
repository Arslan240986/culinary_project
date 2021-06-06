$(document).ready(function () {
    $('#modal-btn').click(function () {
        $('.ui.modal.mymodal').modal('show')
        $('.ui.radio.checkbox').checkbox();
        $('.ui.toggle.checkbox').checkbox();
        $('#avatar_image_id').click(() => {
            $('#id_avatar').click()
            $('#id_avatar').change((e) => {
            })
        })

    })
    $.datetimepicker.setLocale('ru');
    $('.date_input').datetimepicker({
        timepicker:false,
        format:'d.m.Y'
    });

})

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader()
        reader.onload = function (e) {
            var image = e.target.result
            var imageField = document.getElementById('avatar_image_id')
            imageField.src = image
        }
        reader.readAsDataURL(input.files[0])
    }
}