console.log(document.querySelector('title').innerText)

let input = document.querySelector('#id_url')

input.addEventListener('focus',(e)=>{
    console.log(input)
    input.value = ''
})