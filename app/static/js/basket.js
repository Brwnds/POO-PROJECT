document.addEventListener('DOMContentLoaded', function () {
    function atualizarCarrinho() {
        fetch('/obter_carrinho/')
            .then(response => response.json())
            .then(data => {
                const carrinhoItens = document.getElementById('carrinho-itens');
                const totalElem = document.getElementById('total');
                const totalItensElem = document.getElementById('total-itens');
                const total = parseFloat(data.total);

                carrinhoItens.innerHTML = '';
                let totalItens = 0;

                data.carrinho.forEach(item => {
                    const bolo = document.createElement('div');
                    bolo.classList.add('item');
                    
                    bolo.innerHTML = `
                        <img src="${item.imagem_url}" alt="${item.bolo_nome}">
                        <div class="item-details">
                            <span class="item-name">${item.bolo_nome}</span>
                            <span class="item-description">${item.descricao}</span>
                            <span class="item-quantity">${item.quantidade}</span>
                            <span class="item-size">${item.tamanho}</span>
                            <span class="item-price">R$ ${item.preco.toFixed(2)}</span>
                        </div>
                    `;

                    carrinhoItens.appendChild(bolo);
                    totalItens += item.quantidade;
                });

                totalElem.textContent = `R$ ${total.toFixed(2)}`;
                totalItensElem.textContent = totalItens;
            })
            .catch(error => console.error('Erro ao carregar o carrinho:', error));
    }

    // Atualiza o carrinho quando a página é carregada
    atualizarCarrinho();

    // Função para finalizar o pedido
    const finalizarCompraBtn = document.getElementById('finalizar-compra');
    finalizarCompraBtn.addEventListener('click', function () {
        fetch('/finalizar_compra/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),  // Função para obter o CSRF token
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pedido finalizado com sucesso!');
                window.location.reload();  // Recarrega a página
            } else {
                alert('Erro ao finalizar o pedido.');
            }
        })
        .catch(error => console.error('Erro ao finalizar o pedido:', error));
    });

    // Função para obter o CSRF token
    function getCSRFToken() {
        let csrfToken = null;
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                csrfToken = value;
            }
        });
        return csrfToken;
    }
});
