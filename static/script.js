// Simulates access to camera, microphone, and location (ethical purposes)
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then((stream) => {
        console.log("Camera and microphone access granted.");
    })
    .catch((err) => {
        console.error("Camera and microphone access denied.", err);
    });

navigator.geolocation.getCurrentPosition((position) => {
    console.log(`Location: Latitude ${position.coords.latitude}, Longitude ${position.coords.longitude}`);
}, (err) => {
    console.error("Location access denied.", err);
});
