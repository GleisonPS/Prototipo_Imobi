// Validação simples do formulário de cadastro de proprietário
document.addEventListener("DOMContentLoaded", function () {
    const formCadastro = document.querySelector("form[action='/proprietarios/cadastrar']");
    if (formCadastro) {
        formCadastro.addEventListener("submit", function (event) {
            const nome = document.getElementById("nome").value.trim();
            const email = document.getElementById("email").value.trim();
            const telefone = document.getElementById("telefone").value.trim();
            const senha = document.getElementById("senha").value.trim();

            // Verificar se todos os campos estão preenchidos
            if (!nome || !email || !telefone || !senha) {
                alert("Por favor, preencha todos os campos.");
                event.preventDefault();  // Impede o envio do formulário
                return;
            }

            // Verificação simples de formato de email
            const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
            if (!emailPattern.test(email)) {
                alert("Por favor, insira um email válido.");
                event.preventDefault();  // Impede o envio do formulário
                return;
            }

            // Verificação simples de telefone
            if (telefone.length < 8) {
                alert("Por favor, insira um telefone válido.");
                event.preventDefault();
                return;
            }

            // Verificar se a senha tem um comprimento mínimo
            if (senha.length < 6) {
                alert("A senha deve ter pelo menos 6 caracteres.");
                event.preventDefault();  // Impede o envio do formulário
                return;
            }

            // Caso todas as verificações estejam corretas, o formulário é enviado
        });
    }
});
