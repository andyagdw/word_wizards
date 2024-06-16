// SEE https://getbootstrap.com/docs/5.3/customize/color-modes/

(() => {
  'use strict';

  const getStoredTheme = () => localStorage.getItem('theme');
  const setStoredTheme = theme => localStorage.setItem('theme', theme);

  // Get elements
  const themeToggleBtn = document.getElementById('theme-toggler');
  const html = document.documentElement;
  const header = document.getElementById('header');
  const navbar = document.getElementById('navbar');
  const logo = document.getElementById("logo");
  const footer = document.getElementById("footer")
  const word_of_the_day_data_container = document.getElementById("word-of-the-day-data-container");
  const starter_container = document.getElementById("div-starter-container");
  const plus_container = document.getElementById("div-plus-container");
  const pro_container = document.getElementById("div-pro-container");

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  const setTheme = theme => {
    if (theme === 'auto') {
      theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-theme', theme);

    //  Change element classnames or attribute depending on theme
    if (theme === 'dark') {
        // See templates/partials/_navbar.html
        themeToggleBtn.innerHTML = `<img src=${navbar.dataset.lightModeImg} alt='sun' class='theme-img' />`;
        themeToggleBtn.className = 'btn bg-light text-dark';
        html.setAttribute("data-bs-theme", "dark");

        if (header.classList.contains("header-starter-container")) {
            header.classList.remove("bg-light");
            header.classList.add("border-bottom");
        }
        else if (header.classList.contains("header-plus-container")) {
            header.classList.remove("bg-light");
            header.classList.add("border-bottom");
        }
        else if (header.classList.contains("header-pro-container")) {
            header.classList.remove("bg-light");
            header.classList.add("border-bottom");
        }
        else {
            header.className = "mb-5 header-container border-bottom";
        }
        
        // See templates/partials/_navbar.html
        logo.setAttribute("src", navbar.dataset.imgLogoDark);
        footer.classList.remove("bg-light");
        
        if (word_of_the_day_data_container) {
          word_of_the_day_data_container.classList.remove("bg-light");
          word_of_the_day_data_container.classList.add("border");
        }

        if (starter_container) {
          starter_container.classList.replace("starter-container-light", "starter-container-dark");
        }
        
        if (plus_container) {
          plus_container.classList.replace("plus-container-light", "plus-container-dark");
        }
        
        if (pro_container) {
          pro_container.classList.replace("pro-container-light", "pro-container-dark");
        }

    } else {
        // See templates/partials/_navbar.html
        themeToggleBtn.innerHTML =`<img src=${navbar.dataset.darkModeImg} alt='moon' class='theme-img' />`;
        themeToggleBtn.className = 'btn bg-dark text-light';
        html.setAttribute("data-bs-theme", "auto")

        if (header.classList.contains("header-starter-container")) {
            header.classList.add("bg-light");
            header.classList.remove("border-bottom");
        }
        else if (header.classList.contains("header-plus-container")) {
            header.classList.add("bg-light");
            header.classList.remove("border-bottom");
        }
        else if (header.classList.contains("header-pro-container")) {
          header.classList.add("bg-light");
          header.classList.remove("border-bottom");
        }
        else {
            header.className = "bg-light mb-5 header-container";
        }
        // See templates/partials/_navbar.html
        logo.setAttribute("src", navbar.dataset.imgLogoLight);
        footer.classList.add("bg-light");

        if (word_of_the_day_data_container) {
          word_of_the_day_data_container.classList.add("bg-light");
          word_of_the_day_data_container.classList.remove("border");
        }

        if (starter_container) {
          starter_container.classList.replace("starter-container-dark", "starter-container-light");
        }
        
        if (plus_container) {
          plus_container.classList.replace("plus-container-dark", "plus-container-light");
        }
        
        if (pro_container) {
          pro_container.classList.replace("pro-container-dark", "pro-container-light");
        }
    }
  };

  setTheme(getPreferredTheme());

  // Theme toggler
  themeToggleBtn.addEventListener('click', () => {
    const currentTheme = getPreferredTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setStoredTheme(newTheme);
    setTheme(newTheme);

  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme();
    if (!storedTheme) {
      setTheme(getPreferredTheme());
    }
  });
})();