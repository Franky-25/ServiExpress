var fv;
var input_year;
var date_current;
var dateYear;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
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
                plaque: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="plaque"]').value,
                                    type: 'plaque',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                cli: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cliente'
                        },
                    }
                },
                exemplar: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un modelo/marca'
                        },
                    }
                },
                year: {
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
            submit_formdata_with_ajax_form(fv);
        });
});

$(function () {

    input_year = $('input[name="year"]');
    dateYear = document.getElementById('year').value;

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    date_current = new moment();

    input_year.datetimepicker({
        format: 'YYYY',
        locale: 'es',
        keepOpen: false,
        viewMode: 'years',
        date: date_current,
    });

    input_year.on('change.datetimepicker', function (e) {
        fv.revalidateField('year');
    });

    input_year.keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    if (dateYear !== '') {
        input_year.datetimepicker('date', new Date(dateYear, 1));
    }

    $('select[name="cli"]').on('change.select2', function () {
        fv.revalidateField('cli');
    });

    $('select[name="exemplar"]').on('change.select2', function () {
        fv.revalidateField('exemplar');
    });
});