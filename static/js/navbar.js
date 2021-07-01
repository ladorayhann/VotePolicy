// Onclick handler for toggling navbar buttons
document.getElementById("dropdown-burger").addEventListener('click', () => {
    document.getElementById("nav-group").classList.toggle("show")
})

const dropdownClick = (e) => {
    e.currentTarget.nextElementSibling.classList.toggle("show")
}

const dropwdownFocusOut = (e) => {
    if(e.relatedTarget !== null && e.relatedTarget.className === 'dropdown-item'){
        e.preventDefault();
    } else {
        e.currentTarget.nextElementSibling.classList.remove("show")
    }
}

const dropdowns = document.getElementsByClassName("nav-dropdown")
Array.from(dropdowns).forEach(element => {
    element.addEventListener('click', (e) => dropdownClick(e))
    element.addEventListener('focusout', (e) => dropwdownFocusOut(e))
});