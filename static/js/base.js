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

            toggleBtn.classList.add('collapsed');

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

            toggleBtn.classList.remove('collapsed');
            
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
        if (dropdown && userBtn) {
            if (!dropdown?.contains(e.target) && !userBtn?.contains(e.target)) {
                dropdown.classList.add('hidden');
            }
        }
    });  

    window.showNotif = function(message) {
        const modal = document.getElementById('notifModal');
        const modalMessage = document.getElementById('notifModalMessage');
        modalMessage.textContent = message;
        modal.classList.remove('hidden');

        function closeModal() { modal.classList.add('hidden');}

        const okBtn = document.getElementById('okNotifModal');

        okBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', e => { if (e.target === modal) closeModal();});
    };

    window.showError = function(message) {
        const modal = document.getElementById('errorModal');
        const modalMessage = document.getElementById('errorModalMessage');
        modalMessage.textContent = message;
        modal.classList.remove('hidden');

        function closeModal() { modal.classList.add('hidden');}

        const okBtn = document.getElementById('okErrorModal');

        okBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', e => { if (e.target === modal) closeModal();});
    };

    window.showConfirm = function(message, onConfirm) {
        const modal = document.getElementById('confirmationModal');
        const modalMessage = document.getElementById('confirmationModalMessage');
        const okBtn = document.getElementById('okConfirmationBtn');
        const cancelBtn = document.getElementById('cancelConfirmationBtn');

        modalMessage.textContent = message || 'Apakah Anda yakin?';
        modal.classList.remove('hidden');

        function closeModal() {
            modal.classList.add('hidden');
            okBtn.removeEventListener('click', confirmHandler);
            cancelBtn.removeEventListener('click', closeModal);
            modal.removeEventListener('click', overlayHandler);
        }

        function confirmHandler() {
            closeModal();
            if (typeof onConfirm === 'function') onConfirm();
        }

        function overlayHandler(e) {
            if (e.target === modal) closeModal();
        }

        okBtn.addEventListener('click', confirmHandler);
        cancelBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', overlayHandler);
    };


});