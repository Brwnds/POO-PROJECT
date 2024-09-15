document.addEventListener('DOMContentLoaded', function () {
    // Função para atualizar o preço dinâmico
    document.querySelectorAll('.tamanho-select').forEach(function (selectElement) {
        selectElement.addEventListener('change', function () {
            const selectedOption = this.options[this.selectedIndex];
            const precoAtualizado = selectedOption.getAttribute('data-preco');
            const precoElemento = this.closest('.card').querySelector('.preco-dinamico');
            
            // Atualiza o preço exibido
            precoElemento.textContent = precoAtualizado;
        });
    });

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

    // Código para adicionar bolo ao carrinho
    document.querySelectorAll('.botao-comprar').forEach(function (button) {
        button.addEventListener('click', function () {
            const boloId = this.getAttribute('data-product-id');
            const selectElement = this.previousElementSibling;
            const tamanhoSelecionado = selectElement.value.toUpperCase();
            const sabor = this.getAttribute('data-product');
            const preco = selectElement.options[selectElement.selectedIndex].getAttribute('data-preco');

            const data = {
                bolo_id: boloId,
                tamanho: tamanhoSelecionado,
                bolo_nome: sabor,
                preco: preco
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

    // Finalizar compra
    const finalizarCompraBtn = document.getElementById('finalizar-compra');
    finalizarCompraBtn.addEventListener('click', function () {
        const totalElem = document.getElementById('total');
        const carrinhoItens = document.getElementById('carrinho-itens');

        if (parseFloat(totalElem.textContent.replace('R$ ', '')) > 0) {
            alert('Compra finalizada!');
            fetch('/finalizar_compra/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            }).then(() => {
                // Limpa o conteúdo do carrinho na interface
                carrinhoItens.innerHTML = '';
                totalElem.textContent = 'R$ 0,00';
            }).catch(error => {
                console.error('Erro ao limpar o carrinho:', error);
            });
        } else {
            alert('O carrinho está vazio!');
        }
    });
});