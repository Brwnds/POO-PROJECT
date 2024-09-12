document.addEventListener('DOMContentLoaded', function () {
    // Função para atualizar o carrinho
    function atualizarCarrinho() {
        fetch('/obter_carrinho/')
            .then(response => response.json())
            .then(data => {
                const carrinhoItens = document.getElementById('carrinho-itens');
                const totalElem = document.getElementById('total');
                const total = parseFloat(data.total);
                
                carrinhoItens.innerHTML = '';
                
                data.carrinho.forEach(item => {
                    const bolo = `<div>
                        <p>${item.bolo_nome} - ${item.tamanho} - R$ ${item.preco} x ${item.quantidade}</p>
                    </div>`;
                    carrinhoItens.innerHTML += bolo;
                });
                
                totalElem.textContent = `R$ ${total.toFixed(2)}`;
            })
            .catch(error => console.error('Erro ao carregar o carrinho:', error));
    }

    // Atualiza o carrinho quando a página é carregada
    atualizarCarrinho();

    // Código existente para adicionar bolo ao carrinho
    document.querySelectorAll('.botao-comprar').forEach(function (button) {
        button.addEventListener('click', function () {
            const boloId = this.getAttribute('data-product-id');
            const selectElement = this.previousElementSibling;
            const tamanhoSelecionado = selectElement.value.toUpperCase();
            const sabor = this.getAttribute('data-product');

            const data = {
                bolo_id: boloId,
                tamanho: tamanhoSelecionado,
                bolo_nome: sabor
            };

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
                    atualizarCarrinho();  // Atualiza o carrinho após adicionar um bolo
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

    const finalizarCompraBtn = document.getElementById('finalizar-compra');
    finalizarCompraBtn.addEventListener('click', function () {
        if (parseFloat(totalElem.textContent.replace('R$ ', '')) > 0) {
            alert('Compra finalizada!');
            fetch('/obter_carrinho/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            }).then(() => {
                carrinhoItens.innerHTML = '';
                totalElem.textContent = 'R$ 0,00';
            });
        } else {
            alert('O carrinho está vazio!');
        }
    });
});
