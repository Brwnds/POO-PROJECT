document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.botao-comprar').forEach(function (button) {
        button.addEventListener('click', function () {
            const boloId = this.getAttribute('data-product-id');
            const selectElement = this.previousElementSibling;
            const tamanhoSelecionado = selectElement.value.toUpperCase();  // Converte o tamanho para maiúsculas
            const sabor = this.getAttribute('data-product');

            const data = {
                bolo_id: boloId,
                tamanho: tamanhoSelecionado,
                bolo_nome: sabor
            };

            // Obtém o valor do CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch('/adicionar_ao_carrinho/', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Bolo adicionado ao carrinho com sucesso!');
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

    const finalizarCompraBtn = document.getElementById('finalizar-compra');
    const carrinhoItens = document.getElementById('carrinho-itens');
    const totalElem = document.getElementById('total');
    let total = 0;

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
