function form_remove_errors(form) {
    form.find('span.error').remove()
    form.find('div.invalid').removeClass('invalid')
}

function form_success(form, msg) {
    form.find('input, textarea').val("")
    form_remove_errors(form)

    form.prepend('<div class="success">' + msg + '</div>')
}

function form_clear(form) {
    form.find('.success').remove()
    form_remove_errors(form)
}

$(document).ready(function () {
    $('#feedback_form')
        .on('submit', function (e) {
            e.preventDefault();
            form_clear($(this))

            var form = $(this)

            var url = $(this).attr('action');
            var method = $(this).attr('method');

            var dataArray = $(this).serializeArray();

            var dataObj = {};
            $(dataArray).each(function (i, field) {
                dataObj[field.name] = field.value;
            });

            var jsonData = JSON.stringify(dataObj);

            $.ajax({
                url: url,
                method: method,
                contentType: 'application/json',
                data: jsonData,
                success: function (response) {
                    form_success(form, response["message"])
                },
                error: function (xhr, status, error) {
                    $.each(xhr.responseJSON, function (field_name, errors) {
                        var field = form.find("[name='" + field_name + "']")
                        field.closest('div').addClass('invalid')

                        $.each(errors, function (i, error_msg) {
                            field.after('<span class="error">' + error_msg + '</span>')
                        })
                    })
                }
            });
        });
});