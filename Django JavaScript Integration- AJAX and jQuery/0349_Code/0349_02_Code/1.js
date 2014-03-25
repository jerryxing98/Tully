if (typeof XMLHttpRequest == "undefined")
    {
    XMLHttpRequest = function()
        {
        try
            {
            return new ActiveXObject("Msxml2.XMLHTTP.6.0");
            }
        catch(exception)
            {
            try
                {
                return new ActiveXObject("Msxml2.XMLHTTP.3.0");
                }
            catch(exception)
                {
                try
                    {
                    return new ActiveXObject("Msxml2.XMLHTTP");
                    }
                catch(exception)
                    {
                    throw new Error("Could not construct XMLHttpRequest");
                    }
                }
            }
        }
    }

var xhr = new XMLHttpRequest();
xhr.open("GET", "/project/server.cgi?text=world");
callback = function()
    {
    if (xhr.readyState == 4 && xhr.status >= 200 && xhr.status < 300)
        {
        document.getElementById("result").innerHTML = xhr.responseText;
        }
    }
xhr.onreadystatechange = callback;
xhr.send(null);
