$(document).ready(function(){
// <!--Comments show and hide js-->
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
                        if (response['is_liked']=='Like'){
                            $('#like').removeClass('down')
                            $('#like').addClass('up')
                        } else if (response['is_liked']=='Unlike'){
                            $('#like').removeClass('up')
                            $('#like').addClass('down')
                        }
                    },
                    error: function(rs, e){
                        console.log('second', rs.responseText);
                    },
                });
        });
//        Add recipe to the culinary_book
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
  });

  function addComment(id){
        var btn = document.getElementById(id)
        var url_for_comments = document.querySelector('.formReview').getAttribute('action')
        let csrf_for_comments = $('input[name=csrfmiddlewaretoken]').val()
        console.log(url_for_comments)
        if (document.contains(document.getElementById('replay_form'))){
            document.getElementById('replay_form').remove()
        }
        btn.insertAdjacentHTML('afterEnd', `<form id="replay_form" action="${url_for_comments}" method="post" class="ui form input_background mt-10 ml-40">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_for_comments}">
            <textarea name="text" cols="40" rows="2" maxlength="5000" required="" id="id_text"></textarea>
            <input type="hidden" name="parent" value="${id}">
            <div class="ui two buttons">\<button onclick="removeCommentForm()" class="ui basic secondary button mt-10">Закрыть</button>
            <button type="submit" class="ui basic positive button mt-10 child_comment_buttons">ДОБАВИТЬ КОММЕНТАРИЙ</button></div></form>`);
        $('.child_comment_buttons').click(function(e){
            e.preventDefault();
            let text = $('textarea[id=id_text]').val()
            let parent = $('input[name=parent]').val()
            $.ajax({
                type: 'POST',
                url: url_for_comments,
                data: {parent, text, 'csrfmiddlewaretoken': csrf_for_comments },
                dataType: 'json',
                success: function(response){
                    if (document.contains(document.querySelector('.ui.positive.message'))){
                        document.querySelector('.ui.positive.message').remove()
                    }
                    if (response.status){
                        $('#replay_form').before(`<div class="ui positive message">
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
                    $('textarea[id=id_text]').val('');
                },
                error: function(rs, e){
                    console.log(rs.responseText);
                },
            });
        });
    }

