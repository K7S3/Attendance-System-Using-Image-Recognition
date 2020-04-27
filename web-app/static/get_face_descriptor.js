$(document).ready(async function () {

    const MODEL_URL = '/static/models'
    const video = document.getElementById('video');
    const socket = io('http://localhost:8000');
    socket.on('message', (msg)=>{
        alert(msg);
    })
    Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
        faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
        faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
    ]).then()
    $("form").submit(function (e) {
        e.preventDefault();
        form_data = $('form').serializeArray().reduce(function (obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        startVideo()
    });


    function startVideo() {

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            // Not adding `{ audio: true }` since we only want video now
            navigator.mediaDevices.getUserMedia({
                video: true
            }).then(function (stream) {
                //video.src = window.URL.createObjectURL(stream);
                video.srcObject = stream;
                video.play();
            });
        }

    }
    video.addEventListener('play', () => {
        // const canvas = faceapi.createCanvasFromMedia(video)
        // document.body.append(canvas)

        const displaySize = {
            width: video.width,
            height: video.height
        }
        // canvas.width = input.width
        // canvas.height = input.height
        // faceapi.matchDimensions(canvas, displaySize)

        setInterval(async () => {
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptors()
            const resizedDetections = faceapi.resizeResults(detections, displaySize)
            // canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
            const canvas = document.getElementById('overlay')
            canvas.width = video.width
            canvas.height = video.height
            faceapi.draw.drawDetections(canvas, resizedDetections)
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
            form_data['face_vec'] = resizedDetections[0]
            socket.emit('join lecture', form_data);
        }, 100)
    })
});