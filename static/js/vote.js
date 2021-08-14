function checkVisible(elm) {
    var rect = elm.getBoundingClientRect();
    var viewHeight = Math.max(document.documentElement.clientHeight, window.innerHeight);
    return !(rect.bottom < 0 || rect.top - viewHeight >= 0);
}

const form = document.querySelector('.vote-form')
const jumpToVoteButton = document.querySelector('.button-fill.sticky')

function toggleShow() {
    if (checkVisible(form)) {
        jumpToVoteButton.classList.add('fade-out')
    } else {
        jumpToVoteButton.classList.remove('fade-out')
    }
}

window.onscroll = toggleShow

jumpToVoteButton.onclick = function() {
    form.scrollIntoView({behavior: "smooth"})
}