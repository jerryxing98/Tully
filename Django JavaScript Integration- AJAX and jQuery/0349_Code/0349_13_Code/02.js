function init()
    {
    if (detect_feature())
        {
        console.log("init 1");
        initialize_with_feature();
        }
    else
        {
        console.log("init 2");
        initialize_without_feature();
        }
    }
