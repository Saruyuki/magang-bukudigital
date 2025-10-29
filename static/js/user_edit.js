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
