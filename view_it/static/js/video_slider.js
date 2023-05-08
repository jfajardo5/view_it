import KeenSlider from 'keen-slider';

/* Project specific Javascript goes here. */
document.addEventListener('DOMContentLoaded', function () {
  const sliderElements = document.querySelectorAll('.video-slider');

  sliderElements.forEach((sliderElement, index) => {
    // Add a unique ID to each slider element
    sliderElement.id = `video-slider-${index}`;

    try {
      const slider = new KeenSlider(
        `#video-slider-${index}`,
        {
          slides: {
            perView: 2,
            spacing: 15,
          },
          breakpoints: {
            '(min-width: 400px)': {
              slides: { perView: 1 },
            },
            '(min-width: 600px)': {
              slides: { perView: 2, spacing: 1 },
            },
            '(min-width: 1000px)': {
              slides: { perView: 5, spacing: 1 },
            },
          },
        },
        [navigation],
      );

      // lazyLoad(sliderElement);
    } catch (error) {
      console.error('Error initializing slider:', error);
    }
  });
});

// function lazyLoad(sliderElement) {
//   const observer = new IntersectionObserver(
//     (entries, observer) => {
//       entries.forEach((entry) => {
//         if (entry.isIntersecting) {
//           const video = entry.target.querySelector('video');
//           const source = video.querySelector('source');

//           if (source.dataset.src) {
//             source.src = source.dataset.src;
//             source.removeAttribute('data-src');
//             video.load();

//             observer.unobserve(entry.target);
//           }
//         }
//       });
//     },
//     { rootMargin: '200px' },
//   );

//   const slides = sliderElement.querySelectorAll('.keen-slider__slide');
//   slides.forEach((slide) => observer.observe(slide));
// }

function navigation(slider) {
  let wrapper, arrowLeft, arrowRight;

  function markup(remove) {
    wrapperMarkup(remove);
    arrowMarkup(remove);
  }

  function removeElement(elment) {
    elment.parentNode.removeChild(elment);
  }
  function createDiv(className) {
    var div = document.createElement('div');
    var classNames = className.split(' ');
    classNames.forEach((name) => div.classList.add(name));
    return div;
  }

  function arrowMarkup(remove) {
    if (remove) {
      removeElement(arrowLeft);
      removeElement(arrowRight);
      return;
    }
    arrowLeft = createDiv('arrow arrow--left');
    arrowLeft.addEventListener('click', () => slider.prev());
    arrowRight = createDiv('arrow arrow--right');
    arrowRight.addEventListener('click', () => slider.next());

    wrapper.appendChild(arrowLeft);
    wrapper.appendChild(arrowRight);
  }

  function wrapperMarkup(remove) {
    if (remove) {
      var parent = wrapper.parentNode;
      while (wrapper.firstChild)
        parent.insertBefore(wrapper.firstChild, wrapper);
      removeElement(wrapper);
      return;
    }
    wrapper = createDiv('navigation-wrapper');
    slider.container.parentNode.appendChild(wrapper);
    wrapper.appendChild(slider.container);
  }

  function updateClasses() {
    var slide = slider.track.details.rel;
    slide === 0
      ? arrowLeft.classList.add('arrow--disabled')
      : arrowLeft.classList.remove('arrow--disabled');
    slide === slider.track.details.slides.length - 1
      ? arrowRight.classList.add('arrow--disabled')
      : arrowRight.classList.remove('arrow--disabled');
  }

  slider.on('created', () => {
    markup();
    updateClasses();
  });
  slider.on('optionsChanged', () => {
    console.log(2);
    markup(true);
    markup();
    updateClasses();
  });
  slider.on('slideChanged', () => {
    updateClasses();
  });
  slider.on('destroyed', () => {
    markup(true);
  });
}
