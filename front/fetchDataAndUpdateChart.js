function fetchDataAndUpdateChart(counter) {

numero  = counter;

    url =`http://localhost:5000/random-number?index=${numero}`
    fetch(url)
        .then(response => response.json())
        .then(responseData => {
            // Parse da resposta para obter o número aleatório
            const randomNumber = parseFloat(responseData.numero);

            // Adiciona o número aleatório aos dados do gráfico
            const newData = { x: xValue, y: randomNumber };
            data.push(newData);

            // Se o limite de dados for atingido, remova o ponto mais antigo
            if (data.length > dataLimit) {
                data.shift(); // Remove o ponto mais antigo
            }

            // Define o próximo ponto 50 pontos depois do recém-adicionado como 0
            if (data.length >= 50) {
                data[data.length - 50].y = 0;
            }

            xValue++; // Incrementa o valor de x

            // Atualiza o gráfico com os novos dados
            grafico1.update();

            const imageBase64 = responseData.image

            const img = new Image();
            img.onload = function() {
                const canvas = document.getElementById('image');
                const ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpa o canvas antes de desenhar
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height); // Desenha a imagem no canvas
            };
            img.src = imageBase64;

        })
        .catch(error => {
            console.error('Erro ao buscar dados do servidor:', error);
        });
}