function getVideo(){
fetch('http://localhost:5000/get-video')
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao recuperar o vídeo do servidor');
        }
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('video')) {
            throw new Error('O servidor não retornou um vídeo válido');
        }
        return response.blob();
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        video.src = url;
    })
    .catch(error => {
        console.error('Erro ao recuperar o vídeo do servidor:', error);
        // Se falhar ao recuperar o vídeo do servidor ou se o servidor não retornar um vídeo válido, acessa a webcam
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                video.play();
            })
            .catch(err => {
                console.error('Erro ao acessar a webcam:', err);
            });
    });
}