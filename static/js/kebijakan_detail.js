function toggleActive(e) {
    e.currentTarget.classList.toggle('active')
    console.log("clicked")
    const sectionContent = e.currentTarget.nextElementSibling
    sectionContent.classList.toggle('active')
}

const accordions = document.getElementsByClassName("section-accordion")
Array.from(accordions).forEach(element => {
    element.addEventListener('click', (e) => toggleActive(e))
});


