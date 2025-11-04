document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('editUserModal');
  const cancelBtn = document.getElementById('cancelEditBtn');
  const form = document.getElementById('editUserForm');

  function openModal() { modal.classList.remove('hidden'); }
  function closeModal() { modal.classList.add('hidden'); }

  cancelBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });

  const registerModal = document.getElementById('registerModal');
  const openRegisterBtn = document.getElementById('openRegisterModal');

  const singleUserForm = document.getElementById('singleUserForm');
  const bulkUserForm = document.getElementById('bulkUserForm');

  const showSingleForm = document.getElementById('showSingleFormBtn');
  const showBulkForm = document.getElementById('showBulkFormBtn');

  function openRegisterModal() {
    registerModal.classList.remove('hidden');
  }

  function closeRegisterModal() {
    registerModal.classList.add('hidden');
  }

  openRegisterBtn.addEventListener('click', () => openRegisterModal());

  registerModal.addEventListener('click', e => { if (e.target === registerModal) closeRegisterModal(); });

  window.openEditUser = async function (userId) {
    try {
      const res = await fetch(`/user/${userId}/edit/`);
      const data = await res.json();

      document.getElementById('editUserId').value = data.id;
      document.getElementById('editNama').value = data.nama;
      document.getElementById('editJabatan').value = data.jabatan;
      document.getElementById('editRole').value = data.role;

      openModal();
    } catch (err) {
      showNotif('Gagal memuat data pengguna.');
      console.error(err);
    }
  };

  window.deleteUser = async function (userId) {
    showConfirm("Apakah Anda yakin ingin menghapus akun ini?", async () => {
      try {
        const res = await fetch(`/user/${userId}/delete/`, {
          method: 'POST',
          headers: { 
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          }
        });

        const data = await res.json();

        if (data.success) {
          showNotif('Pengguna berhasil dihapus.');
          location.reload();
        } else {
          showNotif(data.error || 'Gagal menghapus pengguna.')
        }
      } catch (err) {
        console.error(err);
        showNotif('Terjadi kesalahan jaringan.');
      }
    });
  };

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const userId = document.getElementById('editUserId').value;
    const formData = new FormData(form);
    const url = `${window.editUserUrlPattern}${userId}/`;
    console.log("Fetching:",)

    try {
      const res = await fetch(`${window.editUserUrlPattern}${userId}/`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();

      if (data.success) {
        showNotif('User berhasil diperbarui.');
        closeModal();
        location.reload();
      } else {
        showNotif(data.error || 'Gagal menyimpan data.');
      }
    } catch (err) {
      showNotif('Terjadi kesalahan jaringan.');
      console.error(err);
    }
  });

  showSingleForm?.addEventListener('click', () => {
    singleUserForm.classList.remove('hidden');
    bulkUserForm.classList.add('hidden');

    showSingleForm.classList.add('bg-blue-600', 'text-white');
    showSingleForm.classList.remove('bg-gray-300', 'text-gray-800');
    showBulkForm.classList.add('bg-gray-300', 'text-gray-800');
    showBulkForm.classList.remove('bg-blue-600', 'text-white');
  });

  showBulkForm?.addEventListener('click', () => {
    bulkUserForm.classList.remove('hidden');
    singleUserForm.classList.add('hidden');

    showBulkForm.classList.add('bg-blue-600', 'text-white');
    showBulkForm.classList.remove('bg-gray-300', 'text-gray-800');
    showSingleForm.classList.add('bg-gray-300', 'text-gray-800');
    showSingleForm.classList.remove('bg-blue-600', 'text-white');
  });
});
