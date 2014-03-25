function update_autocomplete(event, ui)
    {
    var split_value = ui.item.value.split(".");
    var field = split_value[0];
    var id = split_value[1];
    $.ajax({
        data:
            {
            id: "Entity_" + field + "_" + {{ entity.id }},
            value: id,
            },
        url: "/ajax/save", 
        });
    }
