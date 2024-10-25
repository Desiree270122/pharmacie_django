$("#contactForm").validator().on("submit", function (event) {
    if (event.isDefaultPrevented()) {
        // handle the invalid form...
        formError();
        submitMSG(false, "Did you fill in the form properly?");
    } else {
        // everything looks good!
        event.preventDefault();
        submitForm();
    }
});


function submitForm(){
    // Initiate Variables With Form Content
    var noms_complet = $(".noms_complet").val();
    var email = $(".email").val();
    var telephone = $(".telephone").val();
    var message = $(".message").val();

    $.ajax(
        {
            type:"POST",
            url: "message_contact",
            dataType:"json",
            data:{noms_complet:noms_complet, telephone:telephone, email:email,message:message, csrfmiddlewaretoken:"{{csrf_token}}"},
            success: function(response) 
            {
                if (response.status == 1){
                    formSuccess();
                } else {
                    formError();
                    submitMSG(false,text);
                }
            }
        });
}

function formSuccess(){
    $("#contactForm")[0].reset();
    submitMSG(true, "Message Submitted!")
}

function formError(){
    $("#contactForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
        $(this).removeClass();
    });
}

function submitMSG(valid, msg){
    if(valid){
        var msgClasses = "h3 text-center tada animated text-success";
    } else {
        var msgClasses = "h3 text-center text-danger";
    }
    $("#msgSubmit").removeClass().addClass(msgClasses).text(msg);
}