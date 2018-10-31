// 発言の入力文字数・行数チェック
function inputCheck() {
    // 発言欄があるかチェック
    var inputArea = document.getElementById("voice_input_area");
    if(!inputArea) {
        return false;
    }

    var voiceLen = inputArea.value.length;
    document.getElementById("voice_input_number").innerText = voiceLen;

    var voiceLine = 0;
    var tval = document.getElementById("voice_input_area").value;
    num = tval.match(/\r\n/g); //IE 用
    num = tval.match(/\n/g);   //Firefox 用

    if (num != null) {
        voiceLine = num.length +1;
    } else {
        voiceLine = 1;
    }

    document.getElementById("voice_input_line").innerText = voiceLine;

    if ( voiceLen > 200 || voiceLine > 20) {
        document.voice.voice_submit.disabled = true;
    } else {
        document.voice.voice_submit.disabled = false;
    }
}