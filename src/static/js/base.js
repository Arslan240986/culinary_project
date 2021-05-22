var prevScrollpos = window.pageYOffset;
var navbar = document.querySelector("#navbar")
document.querySelector('.bread').style.marginTop = navbar.offsetHeight + 3 + 'px'
function navbarHide() {
    window.onscroll = function () {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            navbar.classList.remove("top_show");
        } else if (currentScrollPos == 0) {
            navbar.classList.remove("top_show");
        } else if (prevScrollpos + 5 < currentScrollPos) {
            $('.ui.dropdown').dropdown('hide');
            navbar.classList.add("top_show");
        }
        prevScrollpos = currentScrollPos;
    }
}
navbarHide()
$(document).ready(function () {
    $('.add_post_box_custom').attr('style', `top: ${50}px !important;`)
    $('.ui.dropdown.user_post').dropdown();
    $('.ui.dropdown').dropdown();
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
                if (response.status) {
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
    // hovering on friends and messages icon on sidebar
    $('.custom_chat_icon').hover((e) => {
        $(e.target).removeClass('grey')
        $(e.target).addClass('yellow')
    }, (e) => {
        $(e.target).removeClass('yellow')
        $(e.target).addClass('grey')
    })
    // this is add dropdown button adapgtive Jquery function 
    if ($(window).width() <= 768) {
        // document.querySelector('.bread').style.marginTop = navbar + navbar+'px'
        // navbarHide(document.querySelector("#sub_navbar"))
        $('.add_dropdown_box_button_ushefa').removeClass('labeled')
        $('.add_more_text_ushefa').remove()
        $('.add_dropdown_icon_ushefa').addClass('big')
    }
    $(window).resize(() => {
        if ($(window).width() <= 768) {
            // navbarHide(document.querySelector("#sub_navbar"))
            $('.add_dropdown_box_button_ushefa').removeClass('labeled')
            $('.add_more_text_ushefa').remove()
            $('.add_dropdown_icon_ushefa').addClass('big')
        } else if ($(window).width() > 768 && document.contains(document.querySelector('.add_more_text_ushefa')) == false) {
            // navbarHide(document.querySelector("#navbar"))
            $('.add_dropdown_box_button_ushefa').addClass('labeled')
            $('.add_dropdown_icon_ushefa').removeClass('big')
            $('.add_dropdown_box_button_ushefa').append('<span class="text add_more_text_ushefa">Добавить</span>')
        }
    })
    // this shows search input while on mobile style
    $('.search_form_ushefa_icon').click(() => {
        $('.search_form_ushefa_icon').removeClass('display')
        $('.search_form_ushefa').removeClass('display')
        $('.first_nav_block').children().each(element => {
            $($('.first_nav_block').children()[element]).addClass('d_none')
        });
        var search_form = `<div class="item search_item_form width_100">
        <form action="/dishes/by_search/" class="mr-10 search_form_ushefa width_100" method="get" >
            <div class="ui fluid action input">
                <input class=" font-oswald" type="search" placeholder="Введите слово" aria-label="Search" name="q">
                <button class="ui basic yellow button" type="submit">
                    <i class="search link icon"></i>
                </button>
            </div>
        </form><i class="close big white icon " onclick="closeSearch(this)"></i></div>`
        $('.first_nav_block').append(search_form)
    })
    // sidebar open close semantic ui
    $('.big.white.bars.icon').click(() => {
        $('.ui.basic.modal.ushefa_modal').modal('show');
    })
    // links to children achours on personal dropdown lists
    $('.centered_custom').click((e)=>{
        $(e.target).children('.dropdown').click()
    })
    $('.personal_drop_list').on('click', (e)=>{
        e.stopPropagation();
        e.target.querySelector('a').click()
    })

})
function closeSearch(e) {
    $(e).parent().remove()
    $('.first_nav_block').children().each(element => {
        $($('.first_nav_block').children()[element]).removeClass('d_none')
    });
    $('.search_form_ushefa_icon').addClass('display')
    $('.search_form_ushefa').addClass('display')
}

// lazy load js 
const lazy_images = document.querySelectorAll('img[data-src]')
const windowHieght = document.documentElement.clientHeight
let = lazyImagesPosition = []
if(lazy_images.length>0){
    lazy_images.forEach(img => {
        if(img.dataset.src){
            lazyImagesPosition.push(img.getBoundingClientRect().top + pageYOffset)
            lazyScrollCheck()
        }
    })
}

window.addEventListener('scroll', lazyScroll)

function lazyScroll(){
    if(document.querySelectorAll('img[data-src]').length>0){
        lazyScrollCheck()
    }
}
function lazyScrollCheck(){
    let imgIndex = lazyImagesPosition.findIndex(
        item => pageYOffset > item - windowHieght
    );
    if (imgIndex >= 0){
        if(lazy_images[imgIndex].dataset.src){
            lazy_images[imgIndex].src = lazy_images[imgIndex].dataset.src
            lazy_images[imgIndex].classList.add('width')
            lazy_images[imgIndex].parentElement.classList.remove('loading_gif')
            lazy_images[imgIndex].removeAttribute('data-src')
            lazy_images[imgIndex].classList.remove('d_none')
        }
        delete lazyImagesPosition[imgIndex]
    }
}