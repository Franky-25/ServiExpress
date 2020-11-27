var fv;

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
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="name"]').value,
                                    type: 'name',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de insumo'
                        },
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                cost: {
                    validators: {
                        numeric: {
                            notEmpty: {},
                            digits: {},
                        }
                    }
                },
                pvp: {
                    validators: {
                        numeric: {
                            notEmpty: {},
                            digits: {},
                        }
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
    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="type"]').on('change.select2', function () {
        fv.revalidateField('type');
    });

    $('input[name="cost"]')
        .TouchSpin({
            min: 1,
            max: 100000000,
            step: 1,
            verticalbuttons: true,
            prefix: '$'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            $('input[name="pvp"]').trigger("touchspin.updatesettings", {min: parseInt($(this).val())});
            fv.revalidateField('cost');
        })
        .keypress(function (e) {
            return validate_form_text('numbers', e, null);
        });

    $('input[name="pvp"]')
        .TouchSpin({
            min: 1,
            max: 100000000,
            step: 1,
            verticalbuttons: true,
            prefix: '$'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fv.revalidateField('pvp');
        })
        .keypress(function (e) {
           return validate_form_text('numbers', e, null);
        });
});
