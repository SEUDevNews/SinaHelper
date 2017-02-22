(function (accout, password, done) {
    var userId = document.getElementById('userId');
    userId.value = accout;
    var passwd = document.getElementById('passwd');
    passwd.value = password;
    document.getElementsByClassName('WB_btn_login')[0].click();
    done('login finished')
})(arguments[0],arguments[1],arguments[arguments.length -1])