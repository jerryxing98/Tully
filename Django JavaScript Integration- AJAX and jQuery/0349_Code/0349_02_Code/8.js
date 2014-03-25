closureExample = function()
    {
    var field = 0;
    return {
        get: function()
            {
            return field;
            },
         set: function(newValue)
            {
            var value = parseInt(newValue.toString());
            if (isNaN(value))
                {
                return false;
                }
            else
                {
                field = value;
                return true;
                }
            }
        }
    } ();
