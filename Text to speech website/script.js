let speech = new SpeechSynthesisUtterance();
let voices = [];

let voiceSelect = document.querySelector("select");

window.speechSynthesis.onvoiceschanged = () => {
    voices = window.speechSynthesis.getVoices();
    speech.voice = voices[0];

    voices.forEach((voice, i) => (voiceSelect.options[i]) = new Option(voice.name, i));
}

voiceSelect.addEventListener("change", () => {
    speech.voice = voices[voiceSelect.value];
})

document.querySelector(".play").addEventListener("click", () => {
    speech.text = document.querySelector("textarea").value;
    window.speechSynthesis.speak(speech);
})

document.querySelector(".pause").addEventListener("click", () => {
    speech.text = document.querySelector("textarea").value;
    window.speechSynthesis.pause(speech);
})

document.querySelector(".resume").addEventListener("click", () => {
    speech.text = document.querySelector("textarea").value;
    window.speechSynthesis.resume(speech);
})
document.querySelector(".stop").addEventListener("click", () => {
    speech.text = document.querySelector("textarea").value;
    window.speechSynthesis.cancel(speech);
})

document.querySelector(".download").addEventListener("click", async () => {
    let text = document.querySelector("textarea").value;
    let synthesis = window.speechSynthesis;

    let audio = new Audio();
    let utterance = new SpeechSynthesisUtterance(text);
    let audioChunks = [];

    utterance.onerror = function(event) {
        console.error("Speech synthesis error:", event.error);
    };

    utterance.onend = function() {
        audio.srcObject = null; // Clear the audio source
        let audioStream = audio.captureStream(); // Capture the audio output
        let mediaRecorder = new MediaRecorder(audioStream);

        mediaRecorder.ondataavailable = function(event) {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = function() {
            let audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
            let url = URL.createObjectURL(audioBlob);

            // Create a link element and simulate a click to trigger download
            let link = document.createElement("a");
            link.href = url;
            link.download = "speech.mp3";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        };

        mediaRecorder.start();
        audio.play(); // Play the synthesized speech
        setTimeout(() => {
            mediaRecorder.stop(); // Stop recording after speech ends
        }, utterance.duration * 1000);
    };

    synthesis.cancel(); // Cancel any previous speech synthesis
    synthesis.speak(utterance);
});

