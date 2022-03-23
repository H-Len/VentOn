// audio
const icon = document.querySelector('i.fa fa-microphone')
let paragraph = document.createElement('p');
let container = document.querySelector('.text-box');
container.appendChild(paragraph);
const sound = document.querySelector('.sound');

window.SpeechRecognition = webkitSpeechRecognition || window.SpeechRecognition;
const synth = window.speechSynthesis;
recognition = new SpeechRecognition();
recognition.interinResult = true;

icon.addEventListener('click', () => {
    sound.play();
    dictate();
});

const dictate = () => {
    recognition.start();
    recognition.onresult = (event) => {
        const speechToText = Array.from(event.results)
        .map(result => result[0])
        .map(result => transcript)
        .join(' ');
        console.log(speechToText)
        paragraph.textContent = speechToText;
    }
}

if (event.results[0].isFinal) {
    paragraph = document.createElement('p');
    container.appendChild(paragraph);
    
    // if (speechToText.includes('what is the time')) {
    //     speak(getTime);
    // };

    if (speechToText.includes('what is the date')) {
        speak(getDate);
    };
}

const speak = () => {
    const utterThis = new SpeechSynthesisUtterance(action());
    synth.speak(utterThis);
}

// const getTime = () => {
//     const time = new Date(Date.now())
//     return 'the time is ${time.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}'
// }

const getDate = () => {
    const time = new Date(Date.now())
    return 'today is ${time.toLocaleDateString()}';
}

// const getTheWeather = () => {
//     fetch('http://api.openweathermap.org/data/2.5/weather?q=${speech.split(' ')[5]}&appid=6aa90859f3e957ff6c77ec9b1bc86296&units=metric')
// }
// .then(function(response) {
//     return response.json();
// }).then(function(weather){
//     if (weather.cod === '404') {
//         utterThis = new SpeechSynthesisUtterance('I cannot find the weather for ${speech.split(' ')[5]}');
//         synth.speak(utterThis);
//         return;
//     }
//     utterThis = new SpeechSynthesisUtterance('this weather condition in ${weather.name} is mostly full of ${weather.weather[0].condition} at a temperature of ${weather.main.temp} degrees Celcius');
//     synth.speak(utterThis);
// })