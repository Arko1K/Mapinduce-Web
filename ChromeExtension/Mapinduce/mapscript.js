/**
 * Created by arko1k on 21/5/15.
 */


chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if(request.mapAhead) {
            var url = "http://192.168.14.250:8002?id=" + request.id + "&place=" + request.place + "&coords=" + request.coords;
            var mapFrame = $('#frame-polyedit');
            if (mapFrame.length)
                mapFrame.attr('src', url);
            else
                $("<iframe id='frame-polyedit' src='" + url + "'></iframe>").appendTo('body');
        }
    }
);