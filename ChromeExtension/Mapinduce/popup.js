/**
 * Created by arko1k on 25/5/15.
 */


$(document).ready(function () {
    $('.button').hover(function () {
        $(this).toggleClass('button-hover');
    });

    $('#button-done').click(function () {
        chrome.runtime.sendMessage({button: 'done'});
    });

    $('#button-correct').click(function () {
        chrome.runtime.sendMessage({button: 'correct'});
    });
});