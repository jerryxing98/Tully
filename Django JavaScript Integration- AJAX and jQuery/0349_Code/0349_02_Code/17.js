$("#messages").load("/sitewide-messages");
$("#messages").load("/user-messages", "username=jsmith");
$("#hidden").load("/user-customizations", "username=jsmith", function(responseText, textStatus, XMLHttpRequest) {
        performUserCustomizations(responseText);
        });
