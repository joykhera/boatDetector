import PhotoSwipeLightbox from './photoswipe/dist/photoswipe-lightbox.esm.js';

const response = await fetch("/graphql", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
    },
    body: JSON.stringify({ query: "{ getBoats { id, link, timestamp } }" }),
})
const boats = (await response.json()).data.getBoats
console.log(boats)
const gallery = document.getElementById('gallery');
const imgWidth = 1920
const imgHeight = 1080

for (const boat of boats) {
    const aTag = document.createElement('a');
    aTag.href = boat.link;
    aTag.setAttribute('data-pswp-width', imgWidth);
    aTag.setAttribute('data-pswp-height', imgHeight);
    aTag.setAttribute('target', '_blank');
    const imgTag = document.createElement('img');
    imgTag.src = boat.link;
    aTag.appendChild(imgTag);
    gallery.appendChild(aTag);
}

const lightbox = new PhotoSwipeLightbox({
    gallery: '#my-gallery',
    children: 'a',
    pswpModule: () => import('photoswipe/dist/photoswipe.esm.js')
});

lightbox.init();