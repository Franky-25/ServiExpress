var fv;
var input_birthdate;
var date_current;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmLogin');
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
            first_name: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 2,
                    },
                    regexp: {
                        regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                        message: 'Debe ingresar sus dos nombres y solo utilizando caracteres alfabéticos'
                    },
                }
            },
            last_name: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 2,
                    },
                    regexp: {
                        regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                        message: 'Debe ingresar sus dos apellidos y solo utilizando caracteres alfabéticos'
                    },
                }
            },
            run: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 9,
                    },
                    digits: {},
                    remote: {
                        url: pathname,
                        // Send { username: 'its value', email: 'its value' } to the back-end
                        data: function () {
                            return {
                                obj: form.querySelector('[name="run"]').value,
                                type: 'run',
                                action: 'validate_data'
                            };
                        },
                        message: 'El número de cedula ya se encuentra registrado',
                        method: 'POST'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 5
                    },
                    regexp: {
                        regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                        message: 'El formato del email no es correcto'
                    }
                }
            },
            mobile: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 7
                    },
                    digits: {}
                }
            },
            address: {
                validators: {
                    // stringLength: {
                    //     min: 4,
                    // }
                }
            },
            birthdate: {
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
            var form = fv.form;
            var parameters = new FormData($(form)[0]);
            parameters.append('action', 'add');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de registrarse?', pathname, parameters, function () {
                alert_sweetalert('success', 'Alerta', 'Se ha registrado correctamente en nuestro sitio web. Se le ha enviado un correo donde estaran sus credenciales', function () {
                    location.href = fv.form.getAttribute('data-url');
                }, null, null)
            });
        });
});

$(function () {

    input_birthdate = $('input[name="birthdate"]');
    date_current = new moment().format("YYYY-MM-DD");

    input_birthdate.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: date_current,
        maxDate: date_current
    });

    input_birthdate.datetimepicker('date', input_birthdate.val());

    input_birthdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('birthdate');
    });

    $('input[name="run"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    
});