$(document).ready(async function () {
    const MODEL_URL = '/static/models'
    // await faceapi.loadTinyFaceDetectorModel(MODEL_URL)

    // await faceapi.loadFaceLandmarkTinyModel(MODEL_URL)
    // await faceapi.loadFaceRecognitionModel(MODEL_URL)
    const video = document.getElementById('video');
    
    Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
        faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
        faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
    ]).then(startVideo)

    function startVideo() {
        navigator.getUserMedia({
                video: {}
            },
            stream => video.srcObject = stream,
            err => console.error(err)
        )
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
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks()
            const resizedDetections = faceapi.resizeResults(detections, displaySize)
            // canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
            const  canvas = document.getElementById('overlay')
            canvas.width = video.width
            canvas.height = video.height
            console.log('afafda')
            faceapi.draw.drawDetections(canvas, resizedDetections)
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)

        }, 100)
    })
});