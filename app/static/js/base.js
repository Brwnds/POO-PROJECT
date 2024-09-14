document.addEventListener('DOMContentLoaded', function () {
    const userIcon = document.getElementById('user-icon');
    const userPopup = document.getElementById('user-popup');
    const editProfileLink = document.getElementById('edit-profile-link');

    // Função para abrir/fechar o popup ao clicar no ícone de usuário
    userIcon.addEventListener('click', function (event) {
        userPopup.style.display = userPopup.style.display === 'block' ? 'none' : 'block';
    });

    // Fechar o popup se o usuário clicar fora dele
    document.addEventListener('click', function (event) {
        if (!userPopup.contains(event.target) && !userIcon.contains(event.target)) {
            userPopup.style.display = "none";
        }
    });

    // Redirecionamento ao clicar em "Editar Perfil"
    if (editProfileLink) {
        const isSuperuser = userPopup.getAttribute('data-is-superuser') === 'True';  // Verifica se é superusuário

        editProfileLink.addEventListener('click', function (event) {
            event.preventDefault();  // Previne o comportamento padrão do link
            if (isSuperuser) {
                window.location.href = "/admin";  // Redireciona para a página de admin se for superusuário
            } else {
                window.location.href = "/adm";    // Redireciona para a página de perfil comum se for usuário comum
            }
        });
    }
});
