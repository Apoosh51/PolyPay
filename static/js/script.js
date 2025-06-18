// header.html
// dark mode
const toggleBtn = document.getElementById('theme-toggle');
const icon = toggleBtn.querySelector('i');
const logo = document.getElementById('site-logo');

const lightLogoSrc = logo.dataset.lightLogo;
const darkLogoSrc  = logo.dataset.darkLogo;

const saved = localStorage.getItem('theme') || 'dark';

document.documentElement.setAttribute('data-theme', saved);
icon.className = saved === 'light' ? 'bx bx-moon' : 'bx bx-sun';
logo.src = saved === 'light' ? lightLogoSrc : darkLogoSrc;

toggleBtn.addEventListener('click', () => {
  const next = document.documentElement.getAttribute('data-theme') === 'light'
    ? 'dark'
    : 'light';

  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);

  icon.className = next === 'light' ? 'bx bx-moon' : 'bx bx-sun';

  logo.src = next === 'light' ? lightLogoSrc : darkLogoSrc;
});


// lang-switcher
const langToggle = document.getElementById('lang-toggle');
const switcher = document.querySelector('.lang-switcher');

langToggle.addEventListener('click', e => {
    e.stopPropagation();
    const isOpen = langToggle.getAttribute('aria-expanded') === 'true';
    langToggle.setAttribute('aria-expanded', String(!isOpen));
    switcher.classList.toggle('open');
});

// Закрытие при клике вне
document.addEventListener('click', () => {
    switcher.classList.remove('open');
    langToggle.setAttribute('aria-expanded', 'false');
});


//index.html
//banner
(function () {
    const slides = document.querySelectorAll('.banner-slide');
    const radios = document.querySelectorAll('input[name="banner-radio"]');
    let current = 0, total = slides.length;

    function showSlide(idx) {
        slides[current].classList.remove('active');
        slides[idx].classList.add('active');
        radios[idx].checked = true;
        current = idx;
    }

    radios.forEach((r, i) => r.addEventListener('change', () => showSlide(i)));

    setInterval(() => {
        showSlide((current + 1) % total);
    }, 5000);
})();