$(document).ready(function () {
    var prevScrollpos = window.pageYOffset;
    document.querySelector('.bread').style.marginTop = document.querySelector("#navbar").offsetHeight + 5 + 'px'
    window.onmousewheel = function () {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            document.querySelector("#navbar").style.top = "0"
        } else if (currentScrollPos == 0) {
            document.querySelector("#navbar").style.top = "0"
        } else {
            document.querySelector("#navbar").style.top = '-' + document.querySelector("#navbar").offsetHeight + 'px';
        }
        prevScrollpos = currentScrollPos;
    }

    $('.ui.dropdown').dropdown();
    $('.ui.floating.labeled.icon.dropdown').dropdown();
    $('.ui.accordion').accordion();

    // <!--   Add email for subcribe ajax response true or false     -->
    $('.subscribe_button').click(function (e) {
        e.preventDefault();
        var email = $('.form__input').val()
        const url = $('#subscribe_form').attr('action')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: 'POST',
            url: url,
            data: { 'email': email, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function (response) {
                console.log(response.status)
                if (response.status) {
                    console.log('aasuccess')
                    if (document.contains(document.querySelector('.ui.positive.message'))) {
                        document.querySelector('.ui.positive.message').remove()
                    }
                    $('.footer-subsrcibe').before(`
                        <div class="ui positive message">
                        <i class="close icon"></i>
                        <div class="header">
                        Вы успешно добавили свой имаил на рассылку
                        </div>
                        <p>Спасибо за подписку</p>
                        </div>`
                    )
                    $('.message .close').on('click', function () {
                        $(this).closest('.message').transition('fade');
                    });
                } else {
                    if (document.contains(document.querySelector('.ui.warning.message'))) {
                        document.querySelector('.ui.warning.message').remove()
                    }
                    $('.footer-subsrcibe').before(`
                        <div class="ui warning message">
                        <i class="close icon"></i>
                        <div class="header">
                        Данный имаил уже находится в списке рассылок
                        </div>
                        <p>Спасибо за подписку.</p>
                        </div>`
                    )
                    $('.message .close').on('click', function () {
                        $(this).closest('.message').transition('fade');
                    });
                };
            },
            error: function (rs, e) {
                console.log('second', rs.responseText);
            },
        });
    })
})