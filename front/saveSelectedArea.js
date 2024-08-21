function saveSelectedArea(counter) {
    const minX = parseInt(selectedArea.style.left);
    const minY = parseInt(selectedArea.style.top);
    const width = parseInt(selectedArea.style.width);
    const height = parseInt(selectedArea.style.height);

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = width;
    canvas.height = height;

    ctx.drawImage(video, minX, minY, width, height, 0, 0, width, height);

    const imageData = canvas.toDataURL('image/png');

    fetch('http://localhost:5000/save-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => {
        if (response.ok) {
            console.log('Imagem enviada com sucesso.');
            fetchDataAndUpdateChart(counter);
            counter++;
        } else {
            console.error('Erro ao enviar imagem:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Erro ao enviar imagem:', error);
    });
}