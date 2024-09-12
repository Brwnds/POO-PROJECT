document.addEventListener('DOMContentLoaded', function () {
    const botaoComprar = document.querySelectorAll('.botao-comprar');
    const carrinhoItens = document.getElementById('carrinho-itens');
    const totalElem = document.getElementById('total');
    const finalizarCompraBtn = document.getElementById('finalizar-compra');
    let total = 0;

    botaoComprar.forEach(button => {
        button.addEventListener('click', function () {
            const productName = this.getAttribute('data-product');
            const tamanhoSelect = this.previousElementSibling;
            const tamanhoSelecionado = tamanhoSelect.options[tamanhoSelect.selectedIndex].value;

            // Faz a requisição POST para adicionar o bolo ao carrinho
            fetch('/adicionar-ao-carrinho/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Pega o CSRF token
                },
                body: JSON.stringify({
                    'bolo_nome': productName,
                    'tamanho': tamanhoSelecionado
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Bolo adicionado ao carrinho com sucesso!');
                    // Você pode também atualizar o carrinho na página, se necessário
                } else {
                    alert('Erro ao adicionar bolo ao carrinho.');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao adicionar bolo ao carrinho.');
            });
        });
    });

    // Função para obter o CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    finalizarCompraBtn.addEventListener('click', function () {
        if (total > 0) {
            alert(`Compra finalizada! Total: R$ ${total.toFixed(2)}`);
            carrinhoItens.innerHTML = '';
            total = 0;
            totalElem.textContent = 'R$ 0,00';
        } else {
            alert('O carrinho está vazio!');
        }
    });
});
