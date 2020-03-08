$(document).ready(function () {
    // Create qi session
    QiSession(function (session) {
        console.log("Created a session and connected!");

        // Load the ALmemory service and raise an event that shows that the greeting page was loaded
        session.service("ALMemory").then(function (mem) {
            mem.raiseEvent("pageLoaded", "displayinfo");

        }, function(error) {
            console.log("An error occurred:", error);
        });
    }, function () {
        console.log("disconnected");
    });
})

function raiseEvent(name, value) {
    QiSession(function (session) {
        session.service("ALMemory").then(function (mem) {
            mem.raiseEvent(name, value);
        }, function (error) {
            console.log("An error occurred:", error);
        });
    });
}

function displayPageInformation() {
    //alert("Inside display: " + localStorage.getItem("pageHeading"));
    document.getElementById("pageHeading").innerHTML = localStorage.getItem("pageHeading");
    document.getElementById("pageText").innerHTML  = localStorage.getItem("pageText");
}

function getAndFillPage(pageName, topSec, midSec) {
    //alert("From index: pageName = " + pageName);
    
    localStorage.setItem("pageHeading", topSec);
    localStorage.setItem("pageText", midSec);
    
    pageName = pageName.toLowerCase();
    
    switch(pageName) {
        case "index":
            window.location = "../index.html";
            break;
        case "help":
            window.location = "help.html";
            break;
        case "displayinfo":
            window.location = "displayinfo.html";
            break;
        case "confirmation":
            window.location = "confirmation.html";
            break;
        default:
            window.location = "../index.html";
            return;
    }
}

function getPage(pageName) {
    pageName = pageName.toLowerCase();

    switch(pageName) {
        case "index":
            window.location = "../index.html";
            break;
        case "help":
            window.location = "help.html";
            break;
        case "displayinfo":
            window.location = "displayinfo.html";
            break;
        case "confirmation":
            window.location = "confirmation.html";
            break;
        default:
            window.location = "../index.html";
            return;
    }
}

function confirmationButtonListener(n) {
    raiseEvent(getButtonId(n), n);
    //raiseEvent("serviceType", getButtonId(n));
}

function getButtonId(n) {
    switch(parseInt(n)) {
        case 1:
            return "noAnswer";
        case 2:
            return "yesAnswer";
        default:
            return "yesAnswer";
    }
}