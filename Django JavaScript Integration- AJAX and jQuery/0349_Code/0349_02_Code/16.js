$.get("/resources/update");
$.post("/resources/update");
$.post("/resources/update", "user=jsmith&product_id=112");
$.post("/resources/update", {user: "jsmith", product_id: 112});
$.post("/resources/update", function(data) { ("#result").html(data) });
$.get("/resources/update", "user=jsmith&product_id=112", function(data, textStatus, XMLHttpRequest) {
        ("#result").html(data);
        logStatus(textStatus);
        });
$.post("/resources/update", "user=jsmith&product_id=112", function(data, textStatus, XMLHttpRequest) {
        ("#result").html(data);
        logStatus(textStatus);
        }, "text");
