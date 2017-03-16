/**
 * Created by bzm on 05.02.17.
 */

/* Select item on click line */
$(function () {
    var ITEMS_CONTAINER = '#items';
    var ACTIONS_CONTAINER = '#items-actions';
    var DIALOG_MULTIEDIT = '#dialog-multiedit';
    var CSRF_TOKEN_NAME = 'csrfmiddlewaretoken';

    //  - helpers -
    function getSelected() {
        var data = [];
        $(ITEMS_CONTAINER + ' input:checked').each(function() {
          data.push($(this).prop('name'));
        });
        return data;
    }

    function getActionUrl() {
        return $('#items').prop('src-url');
    }

    function send(action, arguments) {
        arguments !== undefined || (arguments = {});

        var data = {
            'action': action,
            'arguments': arguments,
            'items': getSelected()
        };
        data[CSRF_TOKEN_NAME] = $('[name="'+CSRF_TOKEN_NAME+'"]')[0].value;
        console.log('data post = ', data);

        return $.ajax(getActionUrl(), {
            data: data,
            type: 'post',
            async: false,
            traditional: true
            
        });
    }
    //  - init -
    $(DIALOG_MULTIEDIT + ' [id$="_date"]:not([type="checkbox"])' ).datepicker().datepicker(
        "option", "dateFormat", "yy-mm-dd"
    );
    // console.log('date inputs:', $(DIALOG_MULTIEDIT + ' [id$="_date"]:not([type="checkbox"])' ));

    //  - events -
    // check checkbox on click row
    $(ITEMS_CONTAINER + ' tbody tr').click(function () {
        var checkbox = $(this).find('input');
        checkbox.prop('checked', !checkbox.prop('checked'));
        // $(this).toggleClass('selector-choosen');
    });
    $(ITEMS_CONTAINER + ' tbody [role="select"]').click(function () {
        this.preventDefault();
        this.stopPropagation();
        return false;
    });

    // select/deselect all items
    $(ACTIONS_CONTAINER + ' [behavior="btn-select-all"]').click(function () {
        if($(this).prop('checked')){
            $(ITEMS_CONTAINER + ' [role="select"]').prop('checked', false);
            $(this).removeClass('btn-info').addClass('btn-default').prop('checked', false);
        }else {
            $(ITEMS_CONTAINER + ' [role="select"]').prop('checked', true);
            $(this).removeClass('btn-default').addClass('btn-info').prop('checked', true);
        }
    });

    var dialog = $(DIALOG_MULTIEDIT).dialog({
        autoOpen: false,
        width: '55%',
        height: $(window).height() * 0.8,
        position: { my: "center", at: "center", on: window },
        modal: true,
        title: "Мультиредактирование",
        buttons: [
            {
                text: "Применить изменения",
                click: function () {
                    var to_update_names = [];
                    $(DIALOG_MULTIEDIT + ' input[name^="edit__"]:checked').each(function () {
                        var name = $(this).prop('name');
                        to_update_names.push(name.substr(6, name.length));
                    });
                    // console.log('to_update_names:', to_update_names);
                    var form_data = $(DIALOG_MULTIEDIT).serializeArray();
                    var form_data_filtered = jQuery.grep(form_data, function( field ) {
                        return $.inArray(field.name, to_update_names) >= 0;
                    });
                    var to_update_data = {}
                    $.each(form_data_filtered, function( index, field ) {
                        to_update_data[field.name] = field.value;
                    });
                    var serialized = JSON.stringify(to_update_data);
                    console.log('serialized:', serialized);
                    send('update', serialized)
                        .done(function () {
                            location.reload();  // dirty hack, instead sync post request
                        });
                },
                class:"ui-button-warning"
            },
            {
                text: "Отмена",
                click: function() {
                    $(this).dialog("close");
                }
            }
        ]
    });

    // select/deselect all items
    $(ACTIONS_CONTAINER + ' [behavior="btn-delete"]').click(function () {
        send('delete')
            .done(function () {
                location.reload();  // dirty hack, instead sync post request
            });
    });

    // select/deselect all items
    $(ACTIONS_CONTAINER + ' [behavior="btn-update"]').click(function () {
        $(DIALOG_MULTIEDIT).dialog('open');
    });

});