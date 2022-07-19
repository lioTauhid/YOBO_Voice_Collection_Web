
const recordAudio = () =>
    new Promise(async resolve => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];

        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });

        const start = () => {
            audioChunks = [];
            mediaRecorder.start();
        };

        const stop = () =>
            new Promise(resolve => {
                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    const play = () => audio.play();
                    resolve({ audioChunks, audioBlob, audioUrl, play });
                });

                mediaRecorder.stop();
            });

        resolve({ start, stop });
    });

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

const recordButton = document.querySelector('#record');
const stopButton = document.querySelector('#stop');
const playButton = document.querySelector('#play');
const saveButton = document.querySelector('#save');
const messageText = document.querySelector('#saved-audio-messages');
const audioWav = document.querySelector('#wav');
//const savedAudioMessagesContainer = document.querySelector('#saved-audio-messages');
const modal = document.querySelector("#myModal");

let recorder;
let audio;

recordButton.addEventListener('click', async () => {
    messageText.hidden = false;
    messageText.innerHTML = "Recording will start in 2 second";
    await sleep(1000);
    messageText.innerHTML = "Recording will start in 1 second";
    await sleep(1000);
    messageText.innerHTML = "Recording will start in 0 second";
    await sleep(1000);
    messageText.innerHTML = "Recording in progress...";
    audioWav.hidden = false;
    await sleep(100);

    recordButton.setAttribute('disabled', true);
    stopButton.removeAttribute('disabled');
    playButton.setAttribute('disabled', true);
    saveButton.setAttribute('disabled', true);
    if (!recorder) {
        recorder = await recordAudio();
    }
    recorder.start();
    await sleep(2000);
    stopButton.click();
});

stopButton.addEventListener('click', async () => {
    recordButton.removeAttribute('disabled');
    stopButton.setAttribute('disabled', true);
    playButton.removeAttribute('disabled');
    saveButton.removeAttribute('disabled');
    messageText.hidden = true;
    audioWav.hidden = true;
    audio = await recorder.stop();
    audio.play();
});

playButton.addEventListener('click', () => {
    audio.play();
});

saveButton.addEventListener('click', () => {
    const reader = new FileReader();
    reader.readAsDataURL(audio.audioBlob);
    reader.onload = () => {
        const base64AudioMessage = reader.result.split(',')[1];

        fetch('/audio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audioFile: base64AudioMessage })
        }).then(res => {
            if (res.status === 200) {
                messageText.innerHTML = "Saved to Server Successfully";
                messageText.hidden = false;
                modal.style.display = "block";
                //return populateAudioMessages();
            }
            console.log('Invalid status saving audio message: ' + res.status);
        });
    };
})

//recordButton.addEventListener('mousedown', () => {
//document.getElementById("saved-audio-messages").hidden=false;
//console.log('long press');
//document.getElementById("saved-audio-messages").style.color = 'red';
//document.getElementById("saved-audio-messages").innerHTML = "Date : " + Date();});
//recordButton.addEventListener('mouseup', () => {
//console.log('long press release');});

const populateAudioMessages = () => {
    return fetch('/audio').then(res => {
        if (res.status === 200) {
            console.log(res);
            return res.json().then(json => {
                json.messageFilenames.forEach(filename => {
                    let audioElement = document.querySelector(`[data-audio-filename="${filename}"]`);
                    if (!audioElement) {
                        audioElement = document.createElement('audio');
                        audioElement.src = `/play/${filename}`;
                        audioElement.setAttribute('data-audio-filename', filename);
                        audioElement.setAttribute('controls', true);
                        savedAudioMessagesContainer.appendChild(audioElement);
                    }
                });
            });
        }
        console.log('Invalid status getting messages 2: ' + res.status);
    });
};

audioWav.hidden = true;
messageText.hidden = true;
//populateAudioMessages();


nameF = document.querySelector('#nameF');
emailF = document.querySelector('#emailF');
phoneF = document.querySelector('#phoneF');
addressF = document.querySelector('#addressF');
submit = document.querySelector('#submit');
span = document.getElementsByClassName("close")[0];

submit.addEventListener('click', () => {
    fetch('/saveUser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "userName": nameF.value,
            "email": emailF.value,
            "phone": phoneF.value,
            "address": addressF.value
        })
    }).then(res => {
        if (res.status === 200) {
            console.log('Succesed: ' + res);
            modal.style.display = "none";
        } else {
            console.log('Invalid status, check all fields: ' + res.status);
        }
    });
});

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}