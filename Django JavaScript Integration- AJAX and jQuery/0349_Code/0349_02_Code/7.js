$.ajax({success: function(data, textStatus, XMLHttpRequest)
        {
        alert(this.name + ", your email address is " + this.email + ".");
        processData(data, this.name, this.email);
        }, context:
        {
        name: prompt("What is your name?", ""),
        email: prompt("What is your email address?", "")
        }, …
    });
