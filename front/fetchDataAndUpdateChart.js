function fetchDataAndUpdateChart(counter) {

numero  = counter;

    url =`http://localhost:5000/random-number?index=${numero}`
    fetch(url)
        .then(response => response.text())
        .then(responseData => {
            // Parse da resposta para obter o número aleatório
            const randomNumber = parseFloat(responseData);

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
        })
        .catch(error => {
            console.error('Erro ao buscar dados do servidor:', error);
        });
}