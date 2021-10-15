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