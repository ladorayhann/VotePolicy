document.addEventListener( 'DOMContentLoaded', function () {
	new Splide( '#card-slider', {
		perPage    : 3,
		perMove : 1,
		width: '70em',
		padding: {
			left : '1.5em',
			right: '1.5em',
		},
		gap:'1em',
		classes: {
			arrows: 'splide__arrows',
			arrow : '.carousel-button',
			prev  : 'splide__arrow--prev carousel-button left',
			next  : 'splide__arrow--next carousel-button right',
		},
		pagination: false,
		breakpoints: {
			850: {
				perPage: 1,
				width : '35em'
			}
		}
	} ).mount();

} );

function recaptchaCallback()  {
	const buttons = document.querySelectorAll('.vote-buttons button')
	buttons.forEach((button) => {
		button.disabled = false;
		button.title = ""
	})
}