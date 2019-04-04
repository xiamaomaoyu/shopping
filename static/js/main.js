function adapt() {
    if (window.innerWidth < 1100) {
        elems = document.getElementsByClassName("specialContent2");
        var i;
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 176px";
        }
        elems = document.getElementsByClassName("specialContent3");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "200px 0 0 176px";
        }
        elems = document.getElementsByClassName("specialContent4");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 352px";
        }
        elems = document.getElementsByClassName("specialContent5");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 704px";
        }
        elems = document.getElementsByClassName("specialContent6");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "200px 0 0 704px";
        }
        elems = document.getElementsByClassName("specialTimeLimitLeftPosition2");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 352px";
        }
        elems = document.getElementsByClassName("specialTimeLimitLeftPosition4");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "200px 0 0 352px";
        }
        elems = document.getElementsByClassName("specialTimeLimitRight");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.marginLeft = "704px";
        }
    } else {
        elems = document.getElementsByClassName("specialContent2");
        var i;
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 16%";
        }
        elems = document.getElementsByClassName("specialContent3");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "200px 0 0 16%";
        }
        elems = document.getElementsByClassName("specialContent4");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 32%";
        }
        elems = document.getElementsByClassName("specialContent5");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 64%";
        }
        elems = document.getElementsByClassName("specialContent6");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "200px 0 0 64%";
        }
        elems = document.getElementsByClassName("specialTimeLimitLeftPosition2");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "0 0 0 32%";
        }
        elems = document.getElementsByClassName("specialTimeLimitLeftPosition4");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.margin = "200px 0 0 32%";
        }
        elems = document.getElementsByClassName("specialTimeLimitRight");
        for (i = 0; i < elems.length; i++) {
            elems[i].style.marginLeft = "64%";
        }
    }
}

window.addEventListener('resize', adapt);
window.addEventListener('load', adapt)

