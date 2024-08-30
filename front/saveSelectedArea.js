function saveSelectedArea() {

    // Altura do vídeo na tela

    // Calcula a proporção entre o vídeo real e o vídeo exibido
    

    const selectedAreaX = cropArea.offsetLeft;
    const selectedAreaY = cropArea.offsetTop;
    const selectedAreaWidth = cropArea.offsetWidth;
    const selectedAreaHeight = cropArea.offsetHeight;

    

    let video = document.getElementById('video');
    let ctx = canvas.getContext('2d');

    const videoWidth = video.videoWidth;  // Largura real do vídeo
    const videoHeight = video.videoHeight; // Altura real do vídeo
    const displayWidth = video.offsetWidth; // Largura do vídeo na tela
    const displayHeight = video.offsetHeight; 
    
    const scaleX = videoWidth / displayWidth;
    const scaleY = videoHeight / displayHeight;

    const scaledX = selectedAreaX * scaleX;
    const scaledY = selectedAreaY * scaleY;
    const scaledWidth = selectedAreaWidth * scaleX;
    const scaledHeight = selectedAreaHeight * scaleY;

    canvas.width = selectedAreaWidth;
    canvas.height = selectedAreaHeight;

    ctx.drawImage(video,scaledX, scaledY, scaledWidth, scaledHeight, 0 , 0, canvas.width, canvas.height);

    let blob = canvas.toBlob((blob) => {
        let fd = new FormData();
        fd.append('image', blob, 'captura.png');
        let req = new Request(
            'http://127.0.0.1:5000/save-image',{
                method: 'POST',
                body: fd
            })
            fetch(req)
            .then(response=>response.json())
            .then(data=>{
                console.log('imagem upada');
                fetchDataAndUpdateChart(counter);
                counter ++;
            })
            .catch(err=>{
                console.log(err.message);
            });
        
    })
}    

    


    // croppedCanvas.toBlob(async (blob) => {
    //     // Cria um FormData para enviar o blob
    //     const formData = new FormData();
    //     formData.append('image', blob, 'captura.png');

    //     try {
    //         // Envia o blob para o servidor
    //         const response = await fetch('SEU_ENDPOINT_AQUI', {
    //             method: 'POST',
    //             body: formData
    //         });

    //         if (response.ok) {
    //             console.log('Imagem enviada com sucesso');
    //         } else {
    //             console.error('Erro ao enviar imagem:', response.statusText);
    //         }
    //     } catch (error) {
    //         console.error('Erro na requisição:', error);
    //     }
    // }, 'image/png');

