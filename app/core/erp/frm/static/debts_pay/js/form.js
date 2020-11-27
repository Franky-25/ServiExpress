var fv;
var input_datejoined;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmPay');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                valor: {
                    validators: {
                        notEmpty: {},
                        digits: {},
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            submit_with_ajax('Notificación',
                '¿Estas seguro de registrar el siguiente abono?',
                pathname,
                {
                    'action': 'payment',
                    'id': $('#cta').val(),
                    'valor': $('input[name="valor"]').val(),
                    'date_joined': $('input[name="date_joined"]').val(),
                },
                function () {
                    table.ajax.reload();
                    $('#myModalPay').modal('hide');
                }
            );
        });
});

$(function () {

    input_datejoined = $('input[name="date_joined"]');

    $('input[name="valor"]').TouchSpin({
        min: 1,
        max: 100000000,
        step: 1,
        prefix: '$'
    }).on('change touchspin.on.min touchspin.on.max', function () {
        fv.revalidateField('valor');
    }).keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('#myModalPay').on('hidden.bs.modal', function () {
        fv.resetForm(true);
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: new moment().format("YYYY-MM-DD")
    });

    input_datejoined.on('change.datetimepicker', function () {
        fv.revalidateField('date_joined');
    });
});
