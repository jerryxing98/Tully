            /* if element is empty add something clickable (if requested) */
            if (!$.trim($(this).html())) {
                $(this).html(settings.placeholder);
            }

            $(this).bind(settings.event, function(e) {

                $("div").removeAttr("onmouseover");
                if (!PHOTO_DIRECTORY.check_login())
                    {
                    PHOTO_DIRECTORY.offer_login();
                    }
                /* abort if disabled for this element */
                if (true === $(this).data('disabled.editable')) {
                    return;
                }
