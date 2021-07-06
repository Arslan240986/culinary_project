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
})