const openNav = document.querySelector('.close-nav')
const closeNav = document.querySelector('.open-nav')
const ToggleNav = document.querySelector('.close-nav-two')
const openLogOut = document.querySelector('.open-nav-two')
const topNav = document.querySelector('.top-nav')
const sideNav = document.querySelector('.nav-bar')
const mainBackground = document.querySelector('.main-background')

openNav.addEventListener('click', () => {
    sideNav.classList.add('active');
    mainBackground.classList.add('active');
});

closeNav.addEventListener('click', () => {
    sideNav.classList.remove('active');
    mainBackground.classList.remove('active');
});

ToggleNav.addEventListener('click', () => {
    sideNav.classList.toggle('active2');
    topNav.classList.toggle('active2');
    mainBackground.classList.toggle('active2');
});

openLogOut.addEventListener('click', () => {
    topNav.classList.toggle('active3');
});