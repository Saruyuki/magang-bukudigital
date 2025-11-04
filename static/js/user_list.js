document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('editUserModal');
  const closeBtn = document.getElementById('closeEditUserModal');
  const cancelBtn = document.getElementById('cancelEditBtn');
  const form = document.getElementById('editUserForm');

  function openModal() { modal.classList.remove('hidden'); }
  function closeModal() { modal.classList.add('hidden'); }

  closeBtn.addEventListener('click', closeModal);
  cancelBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });

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
      alert('Gagal memuat data pengguna.');
      console.error(err);
    }
  };

  window.deleteUser = async function (userId) {
    if (!confirm("Apakah Anda yakin ingin menghapus akun ini?")) return;

    try {
      const res = await fetch(`/user/${userId}/delete/`, {
        method: 'POST',
        headers: { 
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      });

      const data = await res.json();

      if (data.success) {
        alert('Pengguna berhasil dihapus.');
        location.reload();
      } else {
        alert(data.error || 'Gagal menghapus pengguna.')
      }
    } catch (err) {
      console.error(err);
      alert('Terjadi kesalahan jaringan.');
    }
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
        alert('User berhasil diperbarui.');
        closeModal();
        location.reload();
      } else {
        alert(data.error || 'Gagal menyimpan data.');
      }
    } catch (err) {
      alert('Terjadi kesalahan jaringan.');
      console.error(err);
    }
  });
});
