
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

const radioInputs = document.getElementsByClassName("radio-item")
Array.from(radioInputs).forEach(element => {
    element.addEventListener('change',toggleClass)
});