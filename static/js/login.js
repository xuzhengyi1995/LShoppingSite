// JavaScript Document

function is_email(str)
{
    var reg = /^([.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
    return reg.test(str);
}

function shake(o)
{
    var length = 6;
    var selector = $('body').css('position', 'relative');
    for (var i = 1; i <= length; i++)
    {
        if (i % 2 == 0)
        {
            if (i == length)
            {
                selector.animate({'left': 0}, 50);
            } else
            {
                selector.animate({'left': 10}, 50);
            }
        } else
        {
            selector.animate({'left': -10}, 50);
        }
    }
}

function login_check_email()
{
    if (!is_email(document.getElementById("email").value))
    {
        $('#div_e').addClass('has-error');
        document.getElementById("e_error").removeAttribute("hidden");
    } else
    {
        document.getElementById("e_error").setAttribute("hidden", true);
        $('#div_e').removeClass('has-error');
    }
}

function login_check_pwd()
{
    $('#div_p').removeClass('has-error');
}

function login_on_login()
{
    if (!is_email(document.getElementById("email").value))
    {
        //alert('Please input the right email.');
        $('#div_e').addClass('has-error');
        shake("email");
        document.getElementById("email").focus();
        return false;
    }
    if (document.getElementById("pwd").value == '')
    {
        $('#div_p').addClass('has-error');
        shake("pwd");
        document.getElementById("pwd").focus();
        return false;
    }
    document.getElementById("pwd").value = sha512(document.getElementById("pwd").value);
    document.getElementById("pwd").setAttribute("readonly", true);
    document.getElementById("email").setAttribute("readonly", true);

    $("#_login_btn").button("loading").delay(1000).queue(function () {

        $.post("/login", $('#login_form_f').serialize(), function (result) {
            data = result;
            if (data.is_error)
            {
                document.getElementById("err_info").innerHTML = data.error_info;
                document.getElementById("error").removeAttribute("hidden");
            } else
            {
                alert('Welcome ' + data.username + '!');
                window.location.href = "/"
            }
        });
    });
}

function login_clear_error() {
    grecaptcha.reset();
    document.getElementById("pwd").value = '';
    document.getElementById("pwd").removeAttribute("readonly");
    document.getElementById("email").removeAttribute("readonly");
    document.getElementById("error").setAttribute("hidden", true);
    $("#_login_btn").button('reset');
    $("#_login_btn").dequeue();

}
