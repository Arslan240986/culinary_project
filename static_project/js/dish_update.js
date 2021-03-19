
$(document).ready(function(){
        $('.parent_category').change(function(e){
            $('.sub_category').addClass('active');
            $('.category').addClass('active');
            $('.category').empty()
            event.preventDefault();
                var pk = $('.parent_category').val()
                const url = $('.parent_category').attr('data-href-template')
                let csrf = $('input[name=csrfmiddlewaretoken]').val()
                $.ajax({
                    type: 'GET',
                    url: url,
                    data: {'id': pk, 'csrfmiddlewaretoken': csrf },
                    dataType: 'json',
                    success: function(response){
                        if(response.length>0){
                        $('.sub_category').removeClass('active');
                            html_data = '<option value="" selected="True">---------</option>'
                            response.forEach(function(subcats){
                                html_data += `<option value="${subcats.id}">${subcats.name}</option>`
                                })
                            $('.sub_category').html(html_data)
                        }
                    },
                    error: function(rs, e){
                        console.log('second', rs.responseText);
                    },
                });
        })
        $('.sub_category').change(function(e){
                event.preventDefault();
                var pk = $('.sub_category').val()
                const url = $('.parent_category').attr('data-href-template')
                let csrf = $('input[name=csrfmiddlewaretoken]').val()
                $.ajax({
                    type: 'GET',
                    url: url,
                    data: {'id': pk, 'csrfmiddlewaretoken': csrf },
                    dataType: 'json',
                    success: function(response){
                        if(response.length>0){
                            $('.category').removeClass('active');
                            html_data = '<option value="" selected="True">---------</option>'
                            response.forEach(function(subcats){
                                html_data += `<option value="${subcats.id}">${subcats.name}</option>`
                                })
                            $('.category').html(html_data)
                        }
                    },
                    error: function(rs, e){
                        console.log('second', rs.responseText);
                    },
                });
        })
})