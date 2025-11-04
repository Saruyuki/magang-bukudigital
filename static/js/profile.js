document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('changePassModal');
  const openBtn = document.getElementById('changePassBtn');
  const closeBtn = document.getElementById('closePassModal');
  const cancelBtn = document.getElementById('cancelPassBtn');
  const form = document.getElementById('changePassForm');

  const openModal = () => modal.classList.remove('hidden');
  const closeModal = () => modal.classList.add('hidden');

  openBtn.addEventListener('click', openModal);
  closeBtn.addEventListener('click', closeModal);
  cancelBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const formData = new FormData(form);

    try {
      const res = await fetch("{% url 'change_password' %}", {
        method: "POST",
        headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
        body: formData
      });
      const data = await res.json();

      if (data.success) {
        alert("Password berhasil diubah.");
        closeModal();
        form.reset();
      } else {
        alert(data.error || "Gagal mengubah password.");
      }
    } catch (err) {
      console.error("Error:", err);
      alert("Terjadi kesalahan jaringan.");
    }
  });
});
