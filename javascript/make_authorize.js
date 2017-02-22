(function (done) {
    var event = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
    });
    var btn =  document.getElementsByClassName('WB_btn_link')[0];
    btn.dispatchEvent(event);
    done('authorize finished')
})(arguments[arguments.length -1])