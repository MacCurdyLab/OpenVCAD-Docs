/**
 * Image carousels: a [data-openvcad-carousel] element holding several <img>
 * slides shows one at a time, with previous/next buttons and a counter.
 * The slide marked .is-active (or the first one) shows without JavaScript.
 */
(function () {
    'use strict';

    function makeButton(className, label, text) {
        var button = document.createElement('button');
        button.type = 'button';
        button.className = className;
        button.setAttribute('aria-label', label);
        button.appendChild(document.createTextNode(text));
        return button;
    }

    function initCarousel(carousel) {
        if (carousel.getAttribute('data-openvcad-carousel-bound') !== null) {
            return;
        }
        var slides = Array.prototype.slice.call(carousel.querySelectorAll(':scope > img'));
        if (slides.length < 2) {
            return;
        }
        carousel.setAttribute('data-openvcad-carousel-bound', '');

        var index = slides.findIndex(function (slide) {
            return slide.classList.contains('is-active');
        });
        if (index < 0) {
            index = 0;
        }

        var prev = makeButton('openvcad-carousel-prev', 'Previous image', '‹');
        var next = makeButton('openvcad-carousel-next', 'Next image', '›');
        var counter = document.createElement('span');
        counter.className = 'openvcad-carousel-counter';
        counter.setAttribute('aria-live', 'polite');

        function show(i) {
            index = (i + slides.length) % slides.length;
            slides.forEach(function (slide, j) {
                slide.classList.toggle('is-active', j === index);
            });
            counter.textContent = (index + 1) + ' / ' + slides.length;
        }

        prev.addEventListener('click', function () {
            show(index - 1);
        });
        next.addEventListener('click', function () {
            show(index + 1);
        });

        carousel.appendChild(prev);
        carousel.appendChild(next);
        carousel.appendChild(counter);
        show(index);
    }

    function init() {
        document.querySelectorAll('[data-openvcad-carousel]').forEach(initCarousel);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
