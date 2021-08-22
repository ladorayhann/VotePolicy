
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
    const jenisKampanye = url.searchParams.get("jenis_kampanye") || 'ekonomi'
    const selectedOption = document.querySelector(`.input-radio[value=${jenisKampanye}]`)
    selectedOption.checked = true
    toggleClass()
}

updateButton()

function setPage(pageNum, keyword, jenisKampanye) {
    var searchParams = new URLSearchParams(window.location.search)
    searchParams.set('page', pageNum)
    if (keyword != undefined && jenisKampanye != undefined){
      searchParams.set('keyword', keyword)
      searchParams.set('jenis_kampanye', jenisKampanye)
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
