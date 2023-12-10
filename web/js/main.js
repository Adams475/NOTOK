document.getElementById("button-name").addEventListener("click", ()=>{}, false);
$("#dropdown").attr('disabled',true);
$("#dropdown").selectpicker("refresh")
$("#dropdown-running").attr('disabled',true);
$("#dropdown-running").selectpicker("refresh")

var threads = 0;
var assets = 0;

$('#start-button').on('click', async function (e) {
    eel.communicate("start")
})

$('#pause-button').on('click', async function (e) {
    eel.communicate("pause")
})

$('#exit-button').on('click', async function (e) {
    eel.communicate("exit")
})

eel.expose(browser_exit);
function browser_exit() {
    window.close();
}

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}
