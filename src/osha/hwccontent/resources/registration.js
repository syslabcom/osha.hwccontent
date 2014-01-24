
var optional_fields = [
    ['formfield-form-widgets-conferences_check', 'formfield-form-widgets-conferences_description'],
    ['formfield-form-widgets-training_check', 'formfield-form-widgets-training_description'],
    ['formfield-form-widgets-partnerships_check', 'formfield-form-widgets-partnerships_description'],
    ['formfield-form-widgets-promotion_check', 'formfield-form-widgets-promotion_description'],
    ['formfield-form-widgets-bestpractice_check', 'formfield-form-widgets-bestpractice_description'],
    ['formfield-form-widgets-otheractivities_check', 'formfield-form-widgets-otheractivities_description']
];

    function show_hide_widget(widget, hide, fade) {
        if (hide===true) {
            if (fade===true) {
                widget.fadeOut();
            }
            else {
                widget.hide();
            }
        } else {
            if (fade===true) { widget.fadeIn(); }
            else { widget.show(); }
        }
    }

jQuery(document).ready(function() {
    var cb_0 = jQuery('#' + optional_fields[0][0] + ' input');
    if (typeof(cb_0[0]) != "undefined") {
        var widget_0 = jQuery('#' + optional_fields[0][1]);
        cb_0.bind('change', function(e) {
                show_hide_widget(widget_0, !(e.target.checked), true)
        });
        show_hide_widget(widget_0, !(cb_0[0].checked), fade=false);
    }

    var cb_1 = jQuery('#' + optional_fields[1][0] + ' input');
    if (typeof(cb_1[0]) != "undefined") {
        var widget_1 = jQuery('#' + optional_fields[1][1]);
        cb_1.bind('change', function(e) {
                show_hide_widget(widget_1, !(e.target.checked), true)
        });
        show_hide_widget(widget_1, !(cb_1[0].checked), fade=false);
    }

    var cb_2 = jQuery('#' + optional_fields[2][0] + ' input');
    if (typeof(cb_2[0]) != "undefined") {
        var widget_2 = jQuery('#' + optional_fields[2][1]);
        cb_2.bind('change', function(e) {
                show_hide_widget(widget_2, !(e.target.checked), true)
        });
        show_hide_widget(widget_2, !(cb_2[0].checked), fade=false);
    }

    var cb_3 = jQuery('#' + optional_fields[3][0] + ' input');
    if (typeof(cb_3[0]) != "undefined") {
        var widget_3 = jQuery('#' + optional_fields[3][1]);
        cb_3.bind('change', function(e) {
                show_hide_widget(widget_3, !(e.target.checked), true)
        });
        show_hide_widget(widget_3, !(cb_3[0].checked), fade=false);
    }

    var cb_4 = jQuery('#' + optional_fields[4][0] + ' input');
    if (typeof(cb_4[0]) != "undefined") {
        var widget_4 = jQuery('#' + optional_fields[4][1]);
        cb_4.bind('change', function(e) {
                show_hide_widget(widget_4, !(e.target.checked), true)
        });
        show_hide_widget(widget_4, !(cb_4[0].checked), fade=false);
    }

    var cb_5 = jQuery('#' + optional_fields[5][0] + ' input');
    if (typeof(cb_5[0]) != "undefined") {
        var widget_5 = jQuery('#' + optional_fields[5][1]);
        cb_5.bind('change', function(e) {
                show_hide_widget(widget_5, !(e.target.checked), true)
        });
        show_hide_widget(widget_5, !(cb_5[0].checked), fade=false);
    }

    // add placehoder text for autocomplete / content browse inputs
    jQuery('.querySelectSearch input').attr('placeholder', "Enter text or click the browse button")


    jQuery('div#manage_organisation a#reject').click( function() {
        var answer = confirm("Really reject the application and delete the profile?");
        if (answer){
            return true;
        }
        return false;
        });
});