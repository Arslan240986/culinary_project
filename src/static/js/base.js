"use strict"

var prevScrollpos = window.pageYOffset;
var navbar = document.querySelector("#navbar")
document.querySelector('.bread').style.marginTop = navbar.offsetHeight + 3 + 'px'
async function navbarHide() {
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
$(document).ready(async function () {
    $('.add_post_box_custom').attr('style', `top: ${50}px !important;`)
    $('.ui.dropdown.user_post').dropdown();
    $('.ui.dropdown').dropdown();
    $('.ui.accordion').accordion();
    $('.popup_category').popup();
    // <!--   Add email for subcribe ajax response true or false     -->
    $('.subscribe_button').click(async function (e) {
        e.preventDefault();
        try{
            var email = $('.form__input').val()
            const url = $('#subscribe_form').attr('action')
            let csrf = $('input[name=csrfmiddlewaretoken]').val()
            await $.ajax({
                type: 'POST',
                url: url,
                data: { 'email': email, 'csrfmiddlewaretoken': csrf },
                dataType: 'json',
                success: function (response) {
                    if (response.status) {
                        if (document.contains(document.querySelector('.ui.positive.message'))) {
                            document.querySelector('.ui.positive.message').remove();
                        }
                        $('.footer-subsrcibe').before(`
                            <div class="ui positive message">
                            <i class="close icon"></i>
                            <div class="header">
                            Вы успешно добавили свой имаил на рассылку
                            </div>
                            <p>Спасибо за подписку</p>
                            </div>`
                        );
                        $('.message .close').on('click', function () {
                            $(this).closest('.message').transition('fade');
                        });
                    } else {
                        if (document.contains(document.querySelector('.ui.warning.message'))) {
                            document.querySelector('.ui.warning.message').remove();
                        }
                        $('.footer-subsrcibe').before(`
                            <div class="ui warning message">
                            <i class="close icon"></i>
                            <div class="header">
                            Данный имаил уже находится в списке рассылок
                            </div>
                            <p>Спасибо за подписку.</p>
                            </div>`
                        );
                        $('.message .close').on('click', function () {
                            $(this).closest('.message').transition('fade');
                        });
                    };
                },
                error: function (rs, e) {
                    console.log('error_log', rs.responseText);
                },
            });
        }
        catch(error){
            console.error(error);
        }
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
        <form action="/dishes/by_search_title/" class="mr-10 search_form_ushefa width_100" method="get" >
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
    // links to children anchours on personal dropdown lists
    $('.centered_custom').click((e)=>{
        $(e.target).children('.dropdown').click()
    })    
    // $('.side_bar_search_content').sidebar('setting', 'transition', 'overlay').sidebar('toggle')
})
function closeSearch(e) {
    $(e).parent().remove()
    $('.first_nav_block').children().each(element => {
        $($('.first_nav_block').children()[element]).removeClass('d_none')
    });
    $('.search_form_ushefa_icon').addClass('display')
    $('.search_form_ushefa').addClass('display')
}
// masonry grid layout
function masonryGrid(){
    $('.grid_ushefa').masonry({
        fitWidth: true,
        gutter: 10,
        itemSelector: '.grid-item_ushefa',
    });
}
// lazy load js 
function imageLazyLoad(){
    const lazy_images = document.querySelectorAll('img[data-src]')
    const windowHieght = document.documentElement.clientHeight
    let lazyImagesPosition = []

    if(lazy_images.length>0){
        lazy_images.forEach(img => {
            if(img.dataset.src){
                lazyImagesPosition.push(img.getBoundingClientRect().top + pageYOffset)
                lazyScrollCheck()
                masonryGrid()
            }
        })
    }

    window.addEventListener('scroll', lazyScroll)

    function lazyScroll(){
        if(document.querySelectorAll('img[data-src]').length>0){
            lazyScrollCheck()
            masonryGrid()
        }
    }

    function lazyScrollCheck(){
        let imgIndex = lazyImagesPosition.findIndex(
            item => pageYOffset > item - windowHieght
        );
        if (imgIndex >= 0){
            if(lazy_images[imgIndex].dataset.src && lazy_images[imgIndex].complete){
                lazy_images[imgIndex].src = lazy_images[imgIndex].dataset.src;
                lazy_images[imgIndex].parentElement.classList.remove('padding');
                lazy_images[imgIndex].classList.add('width');
                lazy_images[imgIndex].removeAttribute('data-src');
                lazy_images[imgIndex].classList.remove('d_none');
                lazy_images[imgIndex].parentElement.classList.remove('loading_gif');
            }
            delete lazyImagesPosition[imgIndex]
            
        }
    }
}

imageLazyLoad()

// ajax filterin dishes by categories
if (document.contains(document.querySelector('form[name=dish_filter_ajax]'))){
    async function sendAjaxToFilterDishe(url, params){
        await fetch(`${url}?${params}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/x-www-form-urlcoded',
            }
        })
        .then(response => response.json())
        .then(json => renderFilterResult(json))
        .catch(error => console.error(error))
        
    }
    async function sendAjaxToPagination(url, page_num, params){
        await fetch(`${url}${page_num}?${params}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/x-www-form-urlcoded',
            }
        })
        .then(response => response.json())
        .then(json => renderFilterResult(json))
        .catch(error => console.error(error))
        
    }

    const forms_filetr_send_ajax = document.querySelector('form[name=dish_filter_ajax]')
    // const forms_title_search_ajax = document.querySelector('form[name=dish_title_search_ajax]')
    $('.all_filter_click').on('click', function(e){
        let url = forms_filetr_send_ajax.action;
        let params = new URLSearchParams(new FormData(forms_filetr_send_ajax)).toString();
        let loader = `<div class="ui active inverted dimmer custom_dimmer_loader">
                        <div class="ui large text loader">Loading</div>
                    </div>`
        $('.content_side_yummy').append(loader)
        sendAjaxToFilterDishe(url, params)
    })
    $('.all_filter_click').next().on('click', function(e){
        if($(e.target).prev().attr('checked') == 'checked'){
            $(e.target).prev().attr({'checked': false})
            $(e.target).removeClass('checked')
        } else{
            $(e.target).prev().attr({'checked': true})
            $(e.target).addClass('checked')
        }
        
        let url = forms_filetr_send_ajax.action;
        let params = new URLSearchParams(new FormData(forms_filetr_send_ajax)).toString();
        let loader = `<div class="ui active inverted dimmer custom_dimmer_loader">
                        <div class="ui large text loader">Loading</div>
                    </div>`
        $('.content_side_yummy').append(loader)
        sendAjaxToFilterDishe(url, params)
    })
    
    $('.search_title_ajax').on('click', function(e){
        e.preventDefault()
        let url = forms_filetr_send_ajax.action;
        let params = new URLSearchParams(new FormData(forms_filetr_send_ajax)).toString();
        sendAjaxToFilterDishe(url, params)
    });

    function renderFilterResult(data){
        // let template = Hogan.compile(html)
        // let output = template.render(data)
        let div_output = $('.grid_ushefa')
        div_output.html('')
        for(var i=0; i<data['meals'].length; i++){
            let meal = data['meals'][i]
            div_output.append(`
                <div class="grid-item_ushefa">
                    <a href="/detail/${meal['slug']}/${meal['id']}" class="ui fluid card">
                        <div class="page_image loading_gif">
                            <img class="filtered_dishes_img" src="/static/image/2.png" data-src="/media/${meal['poster']}" alt="${meal['title']}">
                        </div>
                        <div class="content">
                            <div class="header grey">
                            ${meal['title']}
                            </div>
                        </div>
                        <div class="extra content">
                            <span class="left floated">
                                <i class="comment icon"></i>
                                ${meal['total_comments']}
                                <i class="eye icon"></i>
                                ${meal['total_hits']}
                                <i class="ui thumbs up icon"></i>
                                ${meal['likes']}
                            </span>
                        </div>
                    </a>
                </div>`)
        }
        div_output.masonry('reloadItems')
        imageLazyLoad()
        setTimeout(()=>{
            $('.custom_dimmer_loader').remove();
        },1000)

        // Ajax pagination 
        let pagin = $('.pagination_try')
        pagin.html('')

        if(data['page_num']>1){
            pagin.append(`<a href="${data['page_num']-1}" class="icon item pagination_item chevron"><i class="left chevron icon"></i></a>`)
        }
        if (data['page_num']-3>=1){
            $('.pagination_item.chevron').after(
                `<a href="${data['page_num']-3}" class="item pagination_item">...</a>`
            )
        }
        if(data['page_range'].length > 1){
            for(var i=0; i<data['page_range'].length; i++){
                if (data['page_range'][i]==data['page_num']){
                    pagin.append(`<span class="active item">${data['page_range'][i]}</span>`)
                }else if (data['page_num']+3 == data['page_range'][i]) {
                    pagin.append(`<a href="${data['page_range'][i]}" class="item pagination_item">...</a>`)
                } else if (data['page_range'][i]<data['page_num']+3 && data['page_range'][i]>data['page_num']-3 ){
                    pagin.append(`<a href="${data['page_range'][i]}" class="item pagination_item">${data['page_range'][i]}</a>`)
                }  
            }
            if(data['page_num']<data['page_range'].length){
                pagin.append(`<a href="${data['page_range'][data['page_num']]}" class="icon item pagination_item"><i class="right chevron icon"></i></a>`)
             }
        };

        $('.ushefa_according_title').html(`Найдено рецептов по вашему запросу - ${data['meal_counts']}`);

        $('.pagination_item').click((e)=>{
            e.preventDefault();
            let params = new URLSearchParams(new FormData(forms_filetr_send_ajax)).toString();
            let page_num= $(e.target).attr('href');
            sendAjaxToPagination(forms_filetr_send_ajax.action, page_num, params)
        })

    }
}


// This is shows more category when click on button show more
$(document).ready(()=>{
    function showHideAllFilterElements(elem){
        let element = elem
        for(let i = 0; i < $(`.${element}`).length; i++){
            if($(`.${element}`)[i].classList.contains('d_none')){
                $(`.${element}`)[i].classList.remove('d_none')
                $(`.${element}`)[i].classList.add('visible')
            }else{
                $(`.${element}`)[i].classList.remove('visible')
                $(`.${element}`)[i].classList.add('d_none')
            }
        }
    }
    $('.show_more_button').on('click', (e)=>{
        showHideAllFilterElements($(e.target).attr('datatype'))
        if($(e.target).children('i').hasClass('plus')){
            $(e.target).children('i').removeClass('plus')
            $(e.target).children('i').addClass('minus')
        } else{
            $(e.target).children('i').removeClass('minus')
            $(e.target).children('i').addClass('plus')
        }
        
    })
    if ($(window).width() < 770){
        $('.show_search_button').addClass('show')
        $('.side_bar_search_content').removeClass('four').removeClass('wide')
        .removeClass('column').addClass('sidebar');
        $('.filter_element_container').removeClass('stackable').removeClass('grid').removeClass('ui').addClass('pushable');
        $('.content_side_yummy').removeClass('twelve').removeClass('wide')
        .removeClass('fluid').removeClass('column').addClass('pusher');
        $('.side_bar_search_content')
        .sidebar({
            context: $('.filter_element_container')
        })
        .sidebar('attach events', '.show_search_button');
        
    };
})

