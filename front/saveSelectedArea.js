function saveSelectedArea() {
    const selectedAreaX = parseInt(selectedArea.style.left);
    const selectedAreaY = parseInt(selectedArea.style.top);
    const selectedAreaWidth = parseInt(selectedArea.style.width);
    const selectedAreaHeight = parseInt(selectedArea.style.height);

    let video = document.getElementById('video');
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');

    canvas.width = selectedAreaWidth;
    canvas.height = selectedAreaHeight;

    ctx.drawImage(video,selectedAreaX, selectedAreaY, selectedAreaWidth, selectedAreaHeight, 0 , 0, canvas.width, canvas.height);

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

