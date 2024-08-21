function fetchDataAndUpdateChart(randomNumber) {
    const newData = { x: xValue, y: randomNumber };
    data.push(newData);

    xValue++; // Incrementa o valor de x

    // Atualiza o gráfico com os novos dados
    grafico1.update();
}