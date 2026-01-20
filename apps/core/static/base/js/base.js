document.addEventListener('DOMContentLoaded', () => {

    // Submenu sidebar
    document.querySelectorAll('.menu-item.has-submenu > a')
        .forEach(link => {
            link.addEventListener('click', event => {
                event.preventDefault();
                link.parentElement.classList.toggle('active');
            });
        });

    // Dropdown do usuário
    const trigger = document.querySelector('.user-trigger');
    const menu = document.querySelector('.user-menu');

    if (trigger) {
        trigger.addEventListener('click', e => {
            e.stopPropagation();
            menu.classList.toggle('open');
        });

        document.addEventListener('click', () => {
            menu.classList.remove('open');
        });
    }
});
