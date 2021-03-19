
var knopka = document.querySelectorAll('.category_btn')
for(let i=0; i<knopka.length; i++){
   knopka[i].addEventListener('click', () => {
      knopka[i].classList.toggle('active')
   })
}

function addReview(name, id){
    document.querySelector('#contactparent').value = id
    document.querySelector('#exampleFormControlTextarea1').innerText = `${name}, `
    document.querySelector('#exampleFormControlTextarea1').focus()
}

