var global_val_for_visibility_msg = 10

// < !--This is get messages from date base and popup window for privet message with form-- >
$(document).ready(function () {
    $('.mini.ui.positive.basic.button.w-big').click((event) => {
        $('.ui.tiny.modal.personal_message').modal({
            onHide: function () {
                global_val_for_visibility_msgval = 10
                window.location.reload()
            },
        }).modal('show');
        var slug = $(event.target).attr('datatype')
        getJson(slug)
    })
})

function getJson(slug) {
    document.querySelector('.bg-private_message').innerHTML = '';
    const pathname = `/private/chat/json/${slug}`
    $.ajax({
        type: 'GET',
        url: pathname,
        success: function (response) {
            const data = response.data
            $('.private_msg_form').attr('action', `${pathname}/`)
            if (response.load_more['load_more']) {
                document.querySelector('.bg-private_message').innerHTML = `<div class="comment">
                                                                                    <div class="ui fluid button get_another_number">Открыть сообшения</div>
                                                                                    </div>`;
            }
            data.map(post => {
                el = `<div class="comment private_message_custom ${post.sender}">
                                    <a class="avatar">
                                        <img class="ui avatar image" src="${post.user_avatar}">
                                    </a>
                                    <div class="content">
                                        <a class="author">${post.user_name}</a>
                                        <div class="metadata">
                                            <span class="date">${post.timestamp}</span>
                                        </div>
                                        <div class="text">
                                            ${post.message}
                                        </div>
                                    </div>
                                </div>`
                document.querySelector('.bg-private_message').innerHTML += el
            })
            $('.overflow-a').scrollTop($('.overflow-a').prop('scrollHeight'))
        },
        error: function (error) {
        }
    })
}
// < !--this Jq is POST's new message in db and put it private message windows-->
$('.private_msg_form').submit(function (e) {
    e.preventDefault()
    var message = $('.private_message_text').val()
    const url = $('.private_msg_form').attr('action')
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'message': message,
        },
        success: function (resp) {
            const last_data = resp.data
            last_data.map(post => {
                last_msg = `<div class="comment ${post.sender}">
                                <a class="avatar">
                                    <img class="ui avatar image" src="${post.user_avatar}">
                                </a>
                                <div class="content">
                                    <a class="author">${post.user_name}</a>
                                    <div class="metadata">
                                        <span class="date">${post.timestamp}</span>
                                    </div>
                                    <div class="text">
                                        ${post.message}
                                    </div>
                                </div>
                            </div>`
                document.querySelector('.bg-private_message').innerHTML += last_msg
            })
            $('.private_message_text').val('')
            $('.overflow-a').scrollTop($('.overflow-a').prop('scrollHeight'))
            $('.private_message_text').focus()
        },
        error: function (error) {
            console.log('error', error)
        }
    })
})
// < !--This is when scrolling top shows more chat from db history-- >
$('.overflow-a').click((e) => {
    if ($(e.target).hasClass('get_another_number')) {
        $('.get_another_number').remove()
        global_val_for_visibility_msg += 10
        const url = $('.private_msg_form').attr('action')
        $.ajax({
            type: 'GET',
            url: url + global_val_for_visibility_msg + '/',
            success: function (some) {
                const new_data = some.new_data
                $('.comment').first().before(`<div class="ui active centered inline black loader"></div>`)
                setTimeout(function () {
                    $('.ui.active.centered.inline.loader').remove()
                    new_data.map(post => {
                        load_msg = `<div class="comment ${post.sender}">
                                                <a class="avatar">
                                                    <img class="ui avatar image" src="${post.user_avatar}">
                                                </a>
                                                <div class="content">
                                                    <a class="author">${post.user_name}</a>
                                                    <div class="metadata">
                                                        <span class="date">${post.timestamp}</span>
                                                    </div>
                                                    <div class="text">
                                                        ${post.message}
                                                    </div>
                                                </div>
                                            </div>`
                        $('.comment').first().before(load_msg)
                    });

                    if (some.load_more['load_more']) {
                        $('.comment').first().before(`<div class="comment">
                                                                <div class="ui fluid button get_another_number">Открыть сообшения</div>
                                                            </div>`);
                    }

                }, 1000);
            },
            error: function (error) {
                console.log('error', error)
            }
        })
    }
})
