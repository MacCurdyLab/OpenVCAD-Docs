/**
 * Click-to-enlarge lightbox for images in the main Sphinx article body (#main-content).
 * Set data-no-lightbox on an <img> to disable.
 */
(function () {
    'use strict';

    var OVERLAY_ID = 'openvcad-lightbox-root';

    function closeLightbox() {
        var el = document.getElementById(OVERLAY_ID);
        if (el) {
            el.remove();
        }
        document.removeEventListener('keydown', onKey);
        document.body.style.overflow = '';
    }

    function onKey(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    }

    function openLightbox(src, alt) {
        closeLightbox();

        var overlay = document.createElement('div');
        overlay.id = OVERLAY_ID;
        overlay.className = 'openvcad-lightbox-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-label', 'Enlarged image');

        var closeBtn = document.createElement('button');
        closeBtn.type = 'button';
        closeBtn.className = 'openvcad-lightbox-close';
        closeBtn.setAttribute('aria-label', 'Close');
        closeBtn.appendChild(document.createTextNode('\u00d7'));

        var inner = document.createElement('div');
        inner.className = 'openvcad-lightbox-inner';

        var big = document.createElement('img');
        big.src = src;
        big.alt = alt || '';
        big.className = 'openvcad-lightbox-image';
        big.decoding = 'async';

        inner.appendChild(big);
        overlay.appendChild(closeBtn);
        overlay.appendChild(inner);

        overlay.addEventListener('click', function (e) {
            if (e.target === overlay || e.target === closeBtn) {
                closeLightbox();
            }
        });

        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';
        closeBtn.focus();
        document.addEventListener('keydown', onKey);
    }

    function onMainContentClick(e) {
        if (e.target.tagName !== 'IMG') {
            return;
        }
        var img = e.target;
        if (img.getAttribute('data-no-lightbox') !== null) {
            return;
        }
        var root = document.getElementById('main-content');
        if (!root || !root.contains(img)) {
            return;
        }
        e.preventDefault();
        e.stopPropagation();
        var src = img.currentSrc || img.src;
        openLightbox(src, img.alt);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        var root = document.getElementById('main-content');
        if (!root) {
            return;
        }
        root.addEventListener('click', onMainContentClick, true);
    }
})();
