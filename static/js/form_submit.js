console.log('form_submit.js loaded');

$(document).ready(function() {
    console.log('DOM ready, binding submit event');

    const $modal = $('#successModal');
    const $okBtn = $('#modalOkBtn');
    const $form = $('form.ajax-submit');
    
    $modal.hide();

    $form.on('submit', function(e) {
        e.preventDefault();
        console.log('Form submit intercepted');

        var form = $(this);
        var url = form.attr('action');
        var formData = form.serialize();

        $.post(url, formData, function(response) {
            if (response.success) {
                $modal.show();

                form[0].reset();
                form.find('select').val(null).trigger('change');
            } else {
                form.find('.text-red-500').remove();
                if (response.errors) {
                    var errors = JSON.parse(response.errors);
                    for (var field in errors) {
                        var errorMessages = errors[field].map(function(e) { return e.message; }).join(', ');
                        var fieldElement = form.find('[name=' + field + ']');
                        if (fieldElement.length) {
                            fieldElement.after('<p class="text-red-500">' + errorMessages + '</p>');
                        }
                    }
                } else if (response.error) {
                    alert(response.error);
                }
            }
        });
    });

    $okBtn.on('click', function() {
        $modal.hide();
    });

    $modal.on('click', function(e) {
        if (e.target === this) {
            $modal.hide();
        }
    });
});