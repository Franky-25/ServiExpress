var tblAssistance = null;
var items = {
    details: {
        date_joined: '',
        assistances: []
    }
};
var input_datejoined;
var fv;

function generate_assistance() {
    $.ajax({
        url: pathname,
        type: 'POST',
        dataType: "json",
        data: {
            'action': 'generate_assistance',
            'date_joined': input_datejoined.val()
        },
        success: function (request) {
            tblAssistance = $('#tblAssistance').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                data: request,
                ordering: false,
                lengthChange: false,
                paging: false,
                columns: [
                    { data: "nro" },
                    { data: "emp.user.full_name" },
                    { data: "emp.user.run" },
                    { data: "job.name" },
                    { data: "dscto" },
                    { data: "motive_perm" },
                    { data: "id" },
                ],
                columnDefs: [
                    {
                        targets: [0],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<input type="text" name="dscto" class="form-control form-control-sm" value="' + data + '" autocomplete="off">';
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<input type="text" name="motive_perm" style="width: 100%;" class="form-control form-control-sm" placeholder="Ingrese un motivo del descuento" value="' + data + '" autocomplete="off">';
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            var attr = row.state === 1 ? ' checked' : '';
                            return '<input type="checkbox" name="chkstate" class="check" ' + attr + '>';
                        }
                    },
                ],
                rowCallback: function (row, data, index) {
                    var tr = $(row).closest('tr');
                    var background = data.state === 0 ? '#fff' : '#fff0d7';
                    $(tr).css('background', background);
                    $('td:eq(0)', row).html(index + 1);

                    tr.find('input[name="dscto"]')
                        .TouchSpin({
                            min: 0.00,
                            max: 100000000,
                            step: 0.01,
                            decimals: 2,
                            boostat: 5,
                            maxboostedstep: 10,
                            verticalbuttons: true,
                        })
                        .keypress(function (e) {
                            return validate_decimals($(this), e);
                        });
                },
                initComplete: function (settings, json) {
                    $('[data-toggle="tooltip"]').tooltip();
                },

            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown + ' ' + textStatus);
        }
    });
}

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmAssistance');
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
                    },
                    remote: {
                        url: pathname,
                        data: function () {
                            return {
                                obj: form.querySelector('[name="date_joined"]').value,
                                action: 'validate_data'
                            };
                        },
                        message: 'La fecha de asistencia ya esta registrada',
                        method: 'POST'
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
            items.details.date_joined = input_datejoined.val();
            items.details.assistances = [];

            $.each(tblAssistance.rows().data(), function (i, item) {
                items.details.assistances.push({
                    'id': item.id,
                    'dscto': item.dscto,
                    'motive_perm': item.motive_perm,
                    'state': item.state
                });
            });

            if (items.details.assistances.length === 0) {
                message_error('Debe tener al menos un empleado en el listado de asistencias');
                return false;
            }

            submit_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                {
                    'action': $('#action').val(),
                    'items': JSON.stringify(items.details)
                },
                function () {
                    location.href = form.getAttribute('data-url');
                }
            );
        });
});

$(function () {

    $('#tblAssistance tbody')
        .on('change', 'input[name="chkstate"]', function () {
            var td = tblAssistance.cell($(this).closest('td, li')).index(),
                row = tblAssistance.row(td.row).data();
            row.state = this.checked ? 1 : 0;
            var tr = $(this).parents('tr')[0];
            var background = !this.checked ? '#fff' : '#fff0d7';
            $(tr).css('background', background);
        })
        .on('keyup', 'input[name="motive_perm"]', function () {
            var td = tblAssistance.cell($(this).closest('td, li')).index(),
                row = tblAssistance.row(td.row).data();
            row.motive_perm = $(this).val();
        })
        .on('change', 'input[name="dscto"]', function () {
            var td = tblAssistance.cell($(this).closest('td, li')).index(),
                row = tblAssistance.row(td.row).data();
            row.dscto = parseFloat($(this).val());
        });

    $('input[type="checkbox"][name="chkstateall"]').on('change', function () {
        var state = this.checked;
        if (tblAssistance !== null) {
            var cells = tblAssistance.cells().nodes();
            $(cells).find('input[type="checkbox"][name="chkstate"]').prop('checked', state).change();
        }
    });

    input_datejoined = $('input[name="date_joined"]');

    input_datejoined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        daysOfWeekDisabled: [0]
        //minDate: new moment().format("YYYY-MM-DD")
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    input_datejoined.on('change.datetimepicker', function (e) {
        fv.validateField('date_joined').then(function (status) {
            if (status === 'Valid') {
                generate_assistance();
            } else if (tblAssistance !== null) {
                tblAssistance.clear().draw();
            }
        });
    });

    input_datejoined.trigger('change');

    //generate_assistance();
});

