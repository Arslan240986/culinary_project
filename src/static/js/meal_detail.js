$(document).ready(function () {
    // <!--Comments show and hide js-->
    let display = false
    $('.cmt_btn').click(function () {
        if (display === false) {
            $(this).next('.comment-box').show('slow');
            $('.comment-box').scrollTop($('.comment-box').prop('scrollHeight'))
            display = true
        } else {
            $(this).next('.comment-box').hide('slow');
            display = false
        }
    });
    //        Like button
    if ($(window).width() < 768) {
        $('.ui.heart').popup({
            on    : 'click'
        });
    } else {
        $('.ui.heart').popup()
    }
    $('#meal_like_button').on('click', function (event) {
        event.preventDefault();
        var pk = $(this).attr('datatype')
        const url = $('#like_form').attr('action')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: 'POST',
            url: url,
            data: { 'dish_id': pk, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function (response) {
                if(response['user_not_login']){

                } else {
                    h = $('.meal_total_likes').html(response['form'])
                    console.log(h);
                    console.log(response['is_liked']);
                    if (response['is_liked'] == 'Like') {
                        $('#meal_like_button').removeClass('outline')
                        $('#meal_like_button').attr('data-content', 'Передумал')
                    } else if (response['is_liked'] == 'Unlike') {
                        $('#meal_like_button').addClass('outline')
                        $('#meal_like_button').attr('data-content', 'Нравится')
                    }
                }
            },
            error: function (rs, e) {
                console.log('error in like', rs.responseText);
            },
        });
    });
    
    //        Add recipe to the culinary_book
    $(document).on('click', '.add_dishes', function (event) {
        event.preventDefault()
        var pk = $('.meal_id').val()
        const url = $('.need_change').attr('action')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: 'POST',
            url: url,
            data: { 'id': pk, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function (response) {
                var add = response['dish_added']
                if (add) {
                    $('.subscribe_div_add').removeClass('active')
                    $('.dish_book_count').html(response['count'])
                    $('.add_dishes').val('в мою кулинарную книгу')
                } else {
                    $('.subscribe_div_add').addClass('active')
                    $('.dish_book_count').html(response['count'])
                    $('.add_dishes').val('в кулинарной книге')
                }
            },
            error: function (rs, e) {
                console.log('drugoy', rs.responseText);
            },
        });
    });

    // adding comment
    $('.comment_button').click(function(e){
        e.preventDefault();
        const url = $('.formReview').attr('action');
        let csrf = $('input[name=csrfmiddlewaretoken]').val();
        let text = $('textarea[id=id_text]').val();
        $.ajax({
            type: 'POST',
            url: url,
            data: {text, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function(response){
                if (document.contains(document.querySelector('.ui.positive.message'))){
                    document.querySelector('.ui.positive.message').remove()
                }
                if (response.status){
                    $('.formReview').before(`<div class="ui positive message">
                        <i class="close icon"></i>
                        <div class="header">
                            Спасибо за участие
                        </div>
                        <p>Ваш комментарий принят после прохождения модерации будет добавлен на сайт</p>
                    </div>`)
                    // <!--message close-->
                    $('.message .close').on('click', function() {
                        $(this).closest('.message').transition('fade');
                    });
                }
                    // <!-- this is clear textarea after saving comment-->
                $('textarea[id=id_text]').val('');
            },
            error: function(rs, e){
                console.log(rs.responseText);
            },
        });
    });
});
// adding sub_comment
function addComment(id) {
    var btn = document.getElementById(id)
    var url_for_comments = document.querySelector('.formReview').getAttribute('action')
    let csrf_for_comments = $('input[name=csrfmiddlewaretoken]').val()
    if (document.contains(document.getElementById('replay_form'))) {
        document.getElementById('replay_form').remove()
    }
    btn.insertAdjacentHTML('afterEnd', `<form id="replay_form" action="${url_for_comments}" method="post" class="ui form input_background mt-10 ml-40">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_for_comments}">
            <textarea name="text" cols="40" rows="2" maxlength="5000" required="" id="id_text"></textarea>
            <input type="hidden" name="parent" value="${id}">
            <div class="ui two buttons">\<button onclick="removeCommentForm()" class="ui inverted red button mt-10">Закрыть</button>
            <button type="submit" class="ui inverted green button mt-10 child_comment_buttons">ДОБАВИТЬ КОММЕНТАРИЙ</button></div></form>`);
    $('.child_comment_buttons').click(function (e) {
        e.preventDefault();
        let text = $('textarea[id=id_text]').val()
        let parent = $('input[name=parent]').val()
        $.ajax({
            type: 'POST',
            url: url_for_comments,
            data: { parent, text, 'csrfmiddlewaretoken': csrf_for_comments },
            dataType: 'json',
            success: function (response) {
                if (document.contains(document.querySelector('.ui.positive.message'))) {
                    document.querySelector('.ui.positive.message').remove()
                }
                if (response.status) {
                    $('#replay_form').before(`<div class="ui positive message">
                            <i class="close icon"></i>
                            <div class="header">
                                Спасибо за участие
                            </div>
                            <p>Ваш комментарий принят после прохождения модерации будет добавлен на сайт</p>
                        </div>`)
                    // <!--message close-->
                    $('.message .close').on('click', function () {
                        $(this).closest('.message').transition('fade');
                    });
                }
                $('textarea[id=id_text]').val('');
            },
            error: function (rs, e) {
                console.log(rs.responseText);
            },
        });
    });
}
function removeCommentForm(){
    document.getElementById('replay_form').remove()
}

// Showing more comment from data when user clicks open more 
var global_val_for_visibility_msg = $('.custom_comment').length
$(document).ready( () => {
    $('.get_another_number').click( (e) => {
        const url = $(e.target).attr('data-href-template')
        global_val_for_visibility_msg += 5
        $.ajax({
            type: 'GET',
            url: `${url}/${global_val_for_visibility_msg}/`,
            success: function (some) {
                const new_data = some.new_data
                $('.get_another_number').addClass('d_none')
                $('.ui.active.centered.inline.black.loader').removeClass(`d_none`)
                setTimeout(function () {
                    var tempo_div_level_2 = Object()
                    var tempo_div_level_1 = Object()
                    $('.ui.active.centered.inline.black.loader').addClass(`d_none`)
                    new_data.map(post => {
                        var avatar_a_element = `<a class="avatar" href="#"><img src="${post.user_avatar}"></a>`
                        var content_div_element = `<div class="content">
                                                        <a class="author" href="${post.user_personal_page}">${post.user_name}</a>
                                                        <div class="metadata">
                                                            <span class="date">${post.created}</span>
                                                        </div>
                                                        <div class="text">
                                                        ${post.text}
                                                        </div>
                                                        <div id="${post.id}" class="actions">
                                                            <a class="ui inverted green mini button" onclick="addComment(${post.id})">Ответить</a>
                                                        </div>
                                                    </div> `
                                                                            
                        if (post.level == 2){
                            var content_div_element_last = `<div class="content">
                                                        <a class="author">${post.user_name}</a>
                                                        <div class="metadata">
                                                            <span class="date">${post.created}</span>
                                                        </div>
                                                        <div class="text">
                                                        ${post.text}
                                                        </div>
                                                    </div> `
                            var custom_comment_div = document.createElement('div')
                            custom_comment_div.setAttribute('class', 'comment custom_comment')
                            custom_comment_div.innerHTML = avatar_a_element
                            custom_comment_div.innerHTML += content_div_element_last
                            tempo_div_level_2[post.id] = custom_comment_div
                        }else if(post.level == 1){
                            var custom_comment_div = document.createElement('div')
                            custom_comment_div.setAttribute('class', 'comment custom_comment')
                            custom_comment_div.innerHTML = avatar_a_element
                            custom_comment_div.innerHTML += content_div_element
                            if (tempo_div_level_2){
                                var comments_div = document.createElement('div')
                                comments_div.setAttribute('class', 'comments')
                                for (var elem in tempo_div_level_2){
                                    comments_div.append(tempo_div_level_2[elem])
                                }
                                custom_comment_div.append(comments_div)
                            }
                            tempo_div_level_1[post.id] = custom_comment_div
                            tempo_div_level_2 = {}
                        }else if(post.level == 0){
                            var custom_comment_div = document.createElement('div')
                            custom_comment_div.setAttribute('class', 'comment custom_comment')
                            custom_comment_div.innerHTML = avatar_a_element
                            custom_comment_div.innerHTML += content_div_element
                            if (tempo_div_level_1){
                                var comments_div = document.createElement('div')
                                comments_div.setAttribute('class', 'comments')
                                for (var elem in tempo_div_level_1){
                                    comments_div.append(tempo_div_level_1[elem])
                                }
                                custom_comment_div.append(comments_div)
                                tempo_div_level_1 = {}
                            }
                            $('.comment-box').scrollTop($('.custom_comment').first().prop('scrollHeight'))
                            $('.comment.custom_comment').first().before(custom_comment_div)
                        }
                        
                    });
                    
                    
                    
                    if (some.load_more['load_more']) {
                        $('.get_another_number').removeClass('d_none')
                    }

                }, 1000);
            },
            error: function (error) {
                console.log('error', error)
            }
        })
    })
})

