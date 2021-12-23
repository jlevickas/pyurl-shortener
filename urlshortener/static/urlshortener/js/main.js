let input = document.querySelector('#id_url')
let copybtn = document.querySelector('#success button')

input.addEventListener('focus',(e)=>{
    console.log(input)
    input.value = ''
})


function updateClipboard(){
    let url = document.querySelector('#shortURL').value
    navigator.clipboard.writeText(url)
    copybtn.innerHTML = 'Copied!'
    setTimeout(function(){
        copybtn.innerHTML = 'Copy'
    },3000)
}

copybtn.addEventListener('click',updateClipboard)