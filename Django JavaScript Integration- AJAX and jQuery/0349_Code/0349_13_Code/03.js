function init()
    {
    console.log("init 3");
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
