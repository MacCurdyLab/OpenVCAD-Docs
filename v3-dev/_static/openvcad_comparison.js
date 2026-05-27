/**
 * Draggable before/after image comparison controls.
 */
(function () {
    'use strict';

    function clamp(value) {
        return Math.max(0, Math.min(100, value));
    }

    function updateComparison(comparison, input) {
        var value = clamp(Number(input.value));
        comparison.style.setProperty('--openvcad-comparison-position', value + '%');
    }

    function initComparison(comparison) {
        var input = comparison.querySelector('.openvcad-comparison-control');
        if (!input) {
            return;
        }
        if (input.getAttribute('value') !== null) {
            input.value = input.getAttribute('value');
        }
        updateComparison(comparison, input);
        input.addEventListener('input', function () {
            updateComparison(comparison, input);
        });
    }

    function init() {
        var comparisons = document.querySelectorAll('[data-openvcad-comparison]');
        comparisons.forEach(initComparison);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
