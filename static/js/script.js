// Pomodoro Timer with Break + Sound + Pause

let studyTime = 1500;   // 25 minutes
let breakTime = 300;    // 5 minutes

let time = studyTime;
let timerRunning = false;
let isStudySession = true;
let countdown;


// Sound Alert
let alarmSound = new Audio("https://www.soundjay.com/buttons/sounds/beep-07.mp3");


// Update Display
function updateDisplay() {

    let minutes = Math.floor(time / 60);
    let seconds = time % 60;

    seconds = seconds < 10 ? "0" + seconds : seconds;

    document.getElementById("time-display").innerText =
        minutes + ":" + seconds;

    document.getElementById("session-type").innerText =
        isStudySession ? "Study Time" : "Break Time";
}


// Start Timer
function startTimer() {

    if (timerRunning) return;

    timerRunning = true;

    countdown = setInterval(function () {

        time--;
        updateDisplay();

        if (time <= 0) {

            alarmSound.play();

            // Switch Study → Break
            if (isStudySession) {
                alert("Study session finished! Take a break.");
                time = breakTime;
                isStudySession = false;
            }

            // Switch Break → Study
            else {
                alert("Break finished! Back to study.");
                time = studyTime;
                isStudySession = true;
            }

            updateDisplay();
        }

    }, 1000);
}


// Pause Timer
function pauseTimer() {
    clearInterval(countdown);
    timerRunning = false;
}


// Reset Timer
function resetTimer() {
    clearInterval(countdown);
    timerRunning = false;
    isStudySession = true;
    time = studyTime;
    updateDisplay();
}
/* ===== Sidebar Toggle Function ===== */

function toggleMenu() {

    let sidebar = document.querySelector(".sidebar");
    let content = document.querySelector(".content");

    sidebar.classList.toggle("closed");
    content.classList.toggle("full");

}


// Default Load
updateDisplay();
