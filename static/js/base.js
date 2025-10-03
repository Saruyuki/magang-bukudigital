document.addEventListener('DOMContentLoaded', function() {
    const topbar = document.getElementById('topbar')
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('main');
    const toggleBtn = document.getElementById('toggleSidebarBtn');

    const labels = document.querySelectorAll('.sidebar-label');
    const appName = document.querySelector('.app-name');
    const icons = document.querySelectorAll('.sidebar-icon');

    const userBtn = document.getElementById('userMenuBtn');
    const dropdown = document.getElementById('userDropdown');

    let expanded = true;

    toggleBtn?.addEventListener('click', () => {
        if (expanded) {
            sidebar.classList.add('sidebar-collapsed', 'disable-hover');
            sidebar.classList.remove('sidebar-expanded');
            main.classList.add('ml-16');
            main.classList.remove('ml-64');
            topbar.classList.add('left-16');
            topbar.classList.remove('left-64');

            labels.forEach(label => label.classList.add('hidden'));
            if (appName) appName.classList.add('hidden');

            icons.forEach(icon => icon.classList.remove('hidden'));

            setTimeout(() => {
                sidebar.classList.remove('disable-hover')
            }, 250);
        }
        else {
            sidebar.classList.remove('sidebar-collapsed', 'disable-hover');
            sidebar.classList.add('sidebar-expanded');
            main.classList.remove('ml-16');
            main.classList.add('ml-64');
            topbar.classList.remove('left-16');
            topbar.classList.add('left-64');
            
            labels.forEach(label => label.classList.remove('hidden'));
            if (appName) appName.classList.remove('hidden');

            icons.forEach(icon => icon.classList.add('hidden'));
        }
        expanded = !expanded;
    });

    userBtn?.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.classList.toggle('hidden');
    });

    window.addEventListener('click', function (e) {
        if (!dropdown.contains(e.target) && !userBtn.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
});