function init()
    {
    if (detect_feature())
        {
        initialize_with_feature();
        }
    else
        {
        initialize_without_feature();
        }
    }
