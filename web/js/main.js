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
    eel.pause()
})

$('#exit-button').on('click', async function (e) {
    eel.communicate("start")
})

$('#add-item').on('click', async function (e) {
    input = $("#add-item-input").val();
    if (input == "") {
        alert("Error! - No input")
        return
    }
    var v_i = await eel.verify_input(input)();
    if (!v_i) {
        alert("Error! - Bad ID")
        return
    }
    $("#dropdown").attr('disabled',false);
    assets++;
    $("#dropdown").append('<option value="'+input+'">'+input+'</option>');
    $('#dropdown').selectpicker('val', input);
    $("#dropdown").selectpicker("refresh");
})

$('#remove-item').on('click', function (e) {
    if (assets == 0) {
        alert("Error! - No assets to remove.")
        return
    }
    assets--;
    var itemSelectorOption = $('#dropdown option:selected');
    itemSelectorOption.remove();
    if (assets == 0) {
        $("#dropdown").attr('disabled',true);
    }
    $("#dropdown").selectpicker("refresh");
})

$("#start-thread").on('click', async function (e) {
    var item = $('#dropdown option:selected');
    if (item.val() == "" || item.val() == null) {
        alert("Error! - No Item Selected.")
        return
    }
    var ver = await eel.dispatch_thread(item.val())()
    alert(ver);
    assets--;
    if (assets == 0) {
        $("#dropdown").attr('disabled',true);
    }
    threads++;
    document.getElementById('thread-count').innerText = "Threads Running: " + threads;
    item.remove();
    $("#dropdown").selectpicker("refresh");
    input = item.val();
    $("#dropdown-running").append('<option value="'+input+'">'+input+'</option>');
    $('#dropdown-running').selectpicker('val', input);
    $("#dropdown-running").attr('disabled',false);
    $("#dropdown-running").selectpicker("refresh");
})

$("#stop-thread").on('click', function (e) {
    if (threads == 0) {
        alert("Error! - No Threads Running.");
        return;
    }
    threads--;
    if (threads == 0) {
        $("#dropdown-running").attr('disabled',true);
    }
    document.getElementById('thread-count').innerText = "Threads Running: " + threads;
    var itemSelectorOption = $('#dropdown-running option:selected');
    itemSelectorOption.remove();
    $("#dropdown-running").selectpicker("refresh");
})

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}
