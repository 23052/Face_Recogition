

document.getElementById('startButton').addEventListener('click', function() {
  const video = document.getElementById('video');
//   const socket = new WebSocket('ws://localhost:8000/ws/stream');

  if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
          .then(function(stream) {
              video.srcObject = stream;
          })
          .catch(function(error) {
              console.log("Erreur lors de l'accès à la caméra: ", error);
          });    
    
  }
});
