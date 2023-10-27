import PhotoSwipeLightbox from './photoswipe/dist/photoswipe-lightbox.esm.js';

fetch("/graphql", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
    },
    body: JSON.stringify({ query: "{ getBoats { id, link, timestamp } }" }),
    // body: JSON.stringify({ query: "query getAllBoats" }),
})
    .then(r => r.json())
    .then(data => console.log("data returned:", data))

const lightbox = new PhotoSwipeLightbox({
    gallery: '#my-gallery',
    children: 'a',
    pswpModule: () => import('photoswipe/dist/photoswipe.esm.js')
});

lightbox.init();