var i = 0;
var id;
var pr = false;
var ne = false;

function galleryR() {
    //var i=Math.floor((Math.random() * 9) + 1);
    var t = 40;
    var k = 1500 / t;
    var p = 1 / k;
    var c;

    document.getElementById("gallery1").src = "/static/img/pizza1.png";
    document.getElementById("gallery1").style.opacity = 1;
    document.getElementById("gallery2").src = "/static/img/pizza2.png";
    document.getElementById("gallery2").style.opacity = 0;

    function timeout() {
        if ((pr) || (ne)) {
            c = k + 1;
        }
        if (c <= k) {
            document.getElementById("gallery1").style.opacity = parseFloat(document.getElementById("gallery1").style.opacity) - p;
            document.getElementById("gallery2").style.opacity = parseFloat(document.getElementById("gallery2").style.opacity) + p;
            c++;
        } else {
            clearInterval(id);
            if ((!pr) && (!ne)) {
                if (i == 0) {
                    i++;
                }
                if (i < 9) {
                    i++;
                } else
                if (i == 9) {
                    i = 1;
                }
                document.getElementById("gallery1").src = "/static/img/pizza" + i + ".png";
                document.getElementById("gallery1").style.opacity = 1;
                if (i < 9) {
                    document.getElementById("gallery2").src = "/static/img/pizza" + (i + 1) + ".png";
                    document.getElementById("gallery2").style.opacity = 0;
                } else {
                    document.getElementById("gallery2").src = "/static/img/pizza1.png";
                    document.getElementById("gallery2").style.opacity = 0;
                }
            }
            if (pr) {
                pr = false;
            } else
            if (ne) {
                ne = false;
            }
            c = 1;
            setTimeout(function() {
                id = setInterval(timeout, t);
            }, 2500);
        }
    }

    c = 1;
    setTimeout(function() {
        id = setInterval(timeout, t);
    }, 2500);
}

function prev() {
    pr = true;
    if (i == 0) {
        i = 9;
    } else
    if (i == 1) {
        i = 9;
    } else {
        i--;
    }
    document.getElementById("gallery1").src = "/static/img/pizza" + i + ".png";
    document.getElementById("gallery1").style.opacity = 1;
    if (i < 9) {
        document.getElementById("gallery2").src = "/static/img/pizza" + (i + 1) + ".png";
        document.getElementById("gallery2").style.opacity = 0;
    } else {
        document.getElementById("gallery2").src = "/static/img/pizza1.png";
        document.getElementById("gallery2").style.opacity = 0;
    }
}

function next() {
    ne = true;
    if (i == 0) {
        i = 2;
    } else
    if (i == 9) {
        i = 1;
    } else {
        i++;
    }
    document.getElementById("gallery1").src = "/static/img/pizza" + i + ".png";
    document.getElementById("gallery1").style.opacity = 1;
    if (i < 9) {
        document.getElementById("gallery2").src = "/static/img/pizza" + (i + 1) + ".png";
        document.getElementById("gallery2").style.opacity = 0;
    } else {
        document.getElementById("gallery2").src = "/static/img/pizza1.png";
        document.getElementById("gallery2").style.opacity = 0;
    }
}

window.onload = galleryR;

var myCenter = new google.maps.LatLng(45.253992, 9.989992);
var marker;

function initialize() {
    var mapProp = {
        center: new google.maps.LatLng(45.253992, 9.989992),
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROAD
    };
    var map = new google.maps.Map(document.getElementById("map"), mapProp);

    var marker = new google.maps.Marker({
        position: myCenter
    });

    marker.setMap(map);
}
google.maps.event.addDomListener(window, 'load', initialize);
