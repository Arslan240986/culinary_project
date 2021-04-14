$(document).ready(function(){
<!--Comments show and hide js-->
        let display = false
        $('.cmt_btn').click(function(){
            if(display===false){
                $(this).next('.comment-box').show('slow');
                $('.comment-box').scrollTop($('.comment-box').prop('scrollHeight'))
                display = true
            } else {
                $(this).next('.comment-box').hide('slow');
                display = false
            }
        });
//        Like button
        $(document).on('click', '#like', function(event){
            event.preventDefault();
                var pk = $(this).attr('value')
                const url = $('#like_form').attr('action')
                let csrf = $('input[name=csrfmiddlewaretoken]').val()
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {'dish_id': pk, 'csrfmiddlewaretoken': csrf },
                    dataType: 'json',
                    success: function(response){
                        h = $('.result_book').html(response['form'])
                        console.log(response['is_liked'])
                        if (response['is_liked']=='Like'){
                            $('#like').removeClass('up')
                            $('#like').addClass('down')
                        } else if (response['is_liked']=='Unlike'){
                            $('#like').removeClass('down')
                            $('#like').addClass('up')
                        }
                    },
                    error: function(rs, e){
                        console.log('second', rs.responseText);
                    },
                });
        });
        $(document).on('click', '.add_dishes', function(event){
        event.preventDefault()
        var pk = $('.meal_id').val()
        const url = $('.need_change').attr('action')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
                type: 'POST',
                url: url,
                data: {'id': pk, 'csrfmiddlewaretoken': csrf },
                dataType: 'json',
                success: function(response){
                    var add = response['dish_added']
                    if (add) {
                        $('.subscribe_div_add').removeClass('active')
                        $('.dish_book_count').html(response['count'])
                        $('.add_dishes').val('в мою кулинарную книгу')
                    } else {
                        $('.subscribe_div_add').addClass('active')
                        $('.dish_book_count').html(response['count'] )
                        $('.add_dishes').val('в кулинарной книге')
                        }
                },
                error: function(rs, e){
                    console.log('drugoy', rs.responseText);
                },
        });
    });
//
//    function addComment(id){
//        var btn = document.getElementById(id)
//        if (document.contains(document.getElementById('replay_form'))){
//            document.getElementById('replay_form').remove()
//        }
//        btn.insertAdjacentHTML('afterEnd', `<form id="replay_form" action="{% url 'culinary_recipe:add_review' meal.id %}" method="post" class="ui form input_background mt-10 ml-40">
//            {% csrf_token%}
//            <textarea name="text" cols="40" rows="2" maxlength="5000" required="" id="id_text"></textarea>
//            <input type="hidden" name="parent" value="' + id + '">
//            <div class="ui two buttons">\<button onclick="removeCommentForm()" class="ui basic secondary button mt-10">Закрыть</button>
//            <button type="submit" class="ui basic positive button mt-10 child_comment_buttons">ДОБАВИТЬ КОММЕНТАРИЙ</button></div></form>`);
//        $('.child_comment_buttons').click(function(e){
//            e.preventDefault();
//            const url = $('#replay_form').attr('action')
//            let csrf = $('input[name=csrfmiddlewaretoken]').val()
//            let text = $('textarea[id=id_text]').val()
//            let parent = $('input[name=parent]').val()
//            $.ajax({
//                type: 'POST',
//                url: url,
//                data: {parent, text, 'csrfmiddlewaretoken': csrf },
//                dataType: 'json',
//                success: function(response){
//                    if (document.contains(document.querySelector('.ui.positive.message'))){
//                        document.querySelector('.ui.positive.message').remove()
//                    }
//                    if (response.status){
//                        $('#replay_form').before(`<div class="ui positive message">
//                            <i class="close icon"></i>
//                            <div class="header">
//                                Спасибо за участие
//                            </div>
//                            <p>Ваш комментарий принят после прохождения модерации будет добавлен на сайт</p>
//                        </div>`)
//                        <!--message close-->
//                        $('.message .close').on('click', function() {
//                            $(this).closest('.message').transition('fade');
//                        });
//                    }
//                    $('textarea[id=id_text]').val('');
//                },
//                error: function(rs, e){
//                    console.log(rs.responseText);
//                },
//            });
//        });
//    }
//
//    function removeCommentForm(){
//        document.getElementById('replay_form').remove()
//    }
//
//    $(document).ready(function(){
//        $('.formReview').submit(function(e){
//            e.preventDefault();
//            const url = $(this).attr('action');
//            let csrf = $('input[name=csrfmiddlewaretoken]').val();
//            let text = $('textarea[id=id_text]').val();
//            $.ajax({
//                type: 'POST',
//                url: url,
//                data: {text, 'csrfmiddlewaretoken': csrf },
//                dataType: 'json',
//                success: function(response){
//                    if (document.contains(document.querySelector('.ui.positive.message'))){
//                        document.querySelector('.ui.positive.message').remove()
//                    }
//                    if (response.status){
//                        $('.formReview').before(`<div class="ui positive message">
//                            <i class="close icon"></i>
//                            <div class="header">
//                                Спасибо за участие
//                            </div>
//                            <p>Ваш комментарий принят после прохождения модерации будет добавлен на сайт</p>
//                        </div>`)
//                        <!--message close-->
//                        $('.message .close').on('click', function() {
//                            $(this).closest('.message').transition('fade');
//                        });
//                    }
//                        <!-- this is clear textarea after saving comment-->
//                    $('textarea[id=id_text]').val('');
//                },
//                error: function(rs, e){
//                    console.log(rs.responseText);
//                },
//            });
//        });
//    });
//
//
//    <!--Load More Comments From DB-->
//    var global_val_for_visibility_comments = 5
//    $('.get_another_number').click((e) => {
//        $('.comment-box').scrollTop($('.custom_comment').first().prop('scrollHeight'))
//        const url = $('.get_another_number').attr('data-href-template')
//        $('.get_another_number').css('display', 'none')
//        global_val_for_visibility_comments += 5
//        $.ajax({
//            type: 'GET',
//            url:   url + global_val_for_visibility_comments + '/',
//            success: function(some){
//                const new_data = some.new_data
//                $('.comment-box').scrollTop($('.custom_comment').first().prop('scrollHeight'))
//                $('.comment-box').first().before(`<div class="ui active centered inline loader"></div>`)
//                setTimeout(function() {
//                    $('.ui.active.centered.inline.loader').remove();
//                    temporary_com_level_2 = {};
//                    new_data.map(post=>{
//                        var comment_div = $('<div class="comment custom_comment"></div>');
//                        var action_btn = $(`<div id="${post.id}" class="actions">
//                                                <a class="ui basic mini positive button" onclick="addComment(${ post.id })">Ответить</a>
//                                            </div>`);
//                        var content_comment =  $(`<div class="content">
//                                                    <a class="author">${post.author}</a>
//                                                    <div class="metadata">
//                                                        <span class="date">${post.created}</span>
//                                                    </div>
//                                                    <div class="text">
//                                                        ${post.text}
//                                                    </div>
//                                                </div>`)
//                        load_msg = $(`<a class="avatar">
//                                        <img src="{% if meal.author.profile.avatar %}{{ meal.author.profile.avatar.url }}{% else %}{% static '/image/avatar_man.png' %}{% endif %}">
//                                    </a>`)
//                        if (post.level == 2){
//                            comment_div = $('<div class="comment custom_comment pl-40 pt-20"></div>')
//                            comment_div.html(load_msg)
//                            comment_div.append(content_comment)
//                        } else if (post.level == 1){
//                            comment_div = $('<div class="comment custom_comment pl-20 pt-20"></div>')
//                            comment_div.html(load_msg)
//                            content_comment.append(action_btn)
//                            comment_div.append(content_comment)
//                        } else {
//                            comment_div.html(load_msg)
//                            content_comment.append(action_btn)
//                            comment_div.append(content_comment)
//                        }
//                        $('.custom_comment').first().before(comment_div)
//                    })
//
//                    if ( some.load_more['load_more'] ){
//                        $('.get_another_number').css('display', 'block')
//                    }
//                }, 500);
//            },
//            error: function(error){
//                console.log('error', error)
//            }
//        })
//    })
  });
