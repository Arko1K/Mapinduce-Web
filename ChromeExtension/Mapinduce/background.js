/**
 * Created by arko1k on 22/5/15.
 */


var currentPlaceId;


function getFullPlace(url) {
    var slice1 = url.slice(url.indexOf('place/') + 6);
    return slice1.slice(0, slice1.indexOf('/data') - 1);
}


chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (tab.url.includes('data') && changeInfo.status == 'complete' && tab.url.includes('place')) {
        var placeFull = getFullPlace(tab.url);
        var place = placeFull.split('/')[0];

        //if (fresh || place == currentPlace) { // Preventing manual navigation from browser.
        //    fresh = false;
        //    currentPlace = place;
        //    var coords = placeFull.slice(placeFull.indexOf('@') + 1);
        //    chrome.tabs.sendMessage(mapTab, {mapAhead: true, id: currentPlaceId, place: currentPlace, coords: coords});
        //}

        var coords = placeFull.slice(placeFull.indexOf('@') + 1);
        chrome.tabs.sendMessage(tabId, {mapAhead: true, id: currentPlaceId, place: place, coords: coords});
    }
});


chrome.browserAction.onClicked.addListener(function (tab) {
    $.ajax({
        type: "GET",
        url: "http://192.168.14.250:8002/next",
        success: function (res) {
            if(res) {
                var respObj = JSON.parse(res);
                currentPlaceId = respObj.id;
                var url = "https://www.google.co.in/maps/place/" + respObj.place;
                chrome.tabs.update(tab.id, {url: url});
            }
            else
                alert('No more places to show.');
        }
    });
});