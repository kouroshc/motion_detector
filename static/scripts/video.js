$(document).ready(function () {
    const videoElement = document.getElementById('videoContainer');
    let stream;
    // Get available video devices
    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            devices.forEach(device => {
                if (device.kind === 'videoinput') {
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label || 'Camera ' + ($('#cameraSelect').options.length + 1);
                    $('#cameraSelect').appendChild(option);
                }
            });
        });

    // Start recording when the Record button is clicked
    $('#recordButton').click(async function () {
        const deviceId = $('#cameraSelect').value;
        try {
            stream = await navigator.mediaDevices.getUserMedia({video: {deviceId}});
            videoElement.srcObject = stream;
            videoElement.play();
            console.log(stream, videoElement)

        } catch (error) {
            console.error('Error accessing camera:', error);
        }
    });


    // Stop recording when needed (e.g., another button)
    $('#stopButton').click(function () {
        console.log("helll");
        window.mediaStream.getTracks().forEach((track) => {
            track.stop();
        });
    });

    let pc = new RTCPeerConnection();

// Function to send an offer request to the server
    async function createOffer() {
        console.log("Sending offer request");

        // Fetch the offer from the server
        const offerResponse = await fetch("/offer", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                sdp: "",
                type: "offer",
            }),
        });

        // Parse the offer response
        const offer = await offerResponse.json();
        console.log("Received offer response:", offer);

        // Set the remote description based on the received offer
        await pc.setRemoteDescription(new RTCSessionDescription(offer));

        // Create an answer and set it as the local description
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
    }

// Trigger the process by creating and sending an offer
    createOffer();

});
