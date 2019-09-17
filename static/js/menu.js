function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let toggleNavStatus = false;
let signInStatus = false;
let regStatus = false;

let toggleNav = async function() {
    let getSidebar = document.querySelector(".nav-sidebar");
    let getSidebarUl = document.querySelector('.nav-sidebar ul');
    let getSignInDiv = document.querySelector(".login-div");
    let getRegDiv = document.querySelector(".registration-div");

    if (toggleNavStatus === false) {
        getSidebar.style.width = "160px";
        getSidebarUl.style.visibility = "visible";
        toggleNavStatus = true;
    }
    else if (toggleNavStatus === true){
        if (signInStatus === true || regStatus === true) {
            getSignInDiv.style.width = "0px";
            getRegDiv.style.width = "0px";
            await sleep(300);
        }
        getSidebar.style.width = "50px";
        getSidebarUl.style.visibility = "hidden";
        toggleNavStatus = false;
        signInStatus = false;
        regStatus = false;
    }
};

let signInNav = async function () {
    let getSignInDiv = document.querySelector(".login-div");
    let getRegDiv = document.querySelector(".registration-div");

    if (signInStatus === false) {
        if (regStatus === true) {
            getRegDiv.style.width = "0px";
            await sleep(300);
            regStatus = false;
        }
        getSignInDiv.style.width = "200px";
        signInStatus = true;
    }
    else if (signInStatus === true) {
        getSignInDiv.style.width = "0px";
        signInStatus = false;
    }
};

let regNav = async function() {
    let getRegDiv = document.querySelector(".registration-div");
    let getSignInDiv = document.querySelector(".login-div");

    if (regStatus === false) {
        if (signInStatus === true) {
            getSignInDiv.style.width = "0px";
            await sleep(300);
            signInStatus = false;
        }
        getRegDiv.style.width = "200px";
        regStatus = true;
    }
    else if (regStatus === true){
        getRegDiv.style.width = "0px";
        regStatus = false;
    }
};
