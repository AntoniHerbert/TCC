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

    // Enviar a imagem para o servidor WebSocket
    socket.send(imageData);
}