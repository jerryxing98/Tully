$.ajax({data: "surname=Smith&cartTotal=12.34", dataType: "text", error: function(XMLHttpRequest, textStatus, errorThrown) {
        displayErrorMessage("An error has occurred: " + textStatus);
        }, success: function(data, textStatus, XMLHttpRequest) {
        try
            {
            updatePage(JSON.parse(data));
            }
        catch(error)
            {
            displayErrorMessage("There was an error updating your shopping cart. Please call customer service at 800-555-1212.");
            }
        },  type: "POST", url: "/update-user"};
