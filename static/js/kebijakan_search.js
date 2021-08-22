
function toggleClass() {
    const radioItems = document.getElementsByClassName("radio-item")
    Array.from(radioItems).forEach(radioItem => {
        if (radioItem.firstElementChild.checked) {
            radioItem.classList.add("selected")
        } else {
            radioItem.classList.remove("selected")
        }
    })
}

function updateButton() {
    const url = new URL(window.location.href)
    const jenisKebijakan = url.searchParams.get("jenis_kebijakan") || 'ekonomi'
    const selectedOption = document.querySelector(`.input-radio[value=${jenisKebijakan}]`)
    selectedOption.checked = true
    toggleClass()
}

updateButton()


function setPage(pageNum, keyword, jenisKebijakan) {
    var searchParams = new URLSearchParams(window.location.search)
    searchParams.set('page', pageNum)
    if (keyword != undefined && jenisKebijakan != undefined){
        searchParams.set('keyword', keyword)
        searchParams.set('jenis_kebijakan', jenisKebijakan)
    }
    window.location.search = searchParams.toString()
}

const radioItems = document.getElementsByClassName("radio-item")
Array.from(radioItems).forEach(element => {
    element.addEventListener('change',toggleClass)
});

const radioInputs = document.getElementsByClassName('input-radio')
Array.from(radioInputs).forEach(element => {
    element.addEventListener('change',() => {element.form.submit()})
});
