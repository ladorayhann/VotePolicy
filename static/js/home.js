document.addEventListener( 'DOMContentLoaded', function () {
	new Splide( '#card-slider', {
		perPage    : 2,
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