var fv;
var current_date;
var input_datejoined;
var tblSalary = null;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmRolPay');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
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
                                    date_joined: form.querySelector('[name="date_joined"]').value,
                                    action: 'validate_data'
                                };
                            },
                            message: 'El rol de pago ya esta generado en esta semana',
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
            if (tblSalary === null) {
                message_error('No ha datos en el rol de pago');
                return false;
            }

            var parameters = {
                'action': 'add',
                'date_joined': input_datejoined.val(),
            };

            submit_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = form.getAttribute('data-url');
                }
            );
        });
});

function generate_salary() {
    tblSalary = $('#tblSalary').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'generate_salary',
                'date_joined': input_datejoined.val(),
            },
            dataSrc: ""
        },
        columns: [
            {"data": "emp.user.full_name"},
            {"data": "job.name"},
            {"data": "week"},
            {"data": "rmu"},
            {"data": "days_work"},
            {"data": "dsctos"},
            {"data": "bonus"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4, -6],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(0);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a rel="det" class="btn btn-primary btn-xs"><i class="fas fa-dollar-sign"></i></a>';
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    current_date = new moment().format("YYYY-MM-DD");
    input_datejoined = $('input[name="date_joined"]');

    input_datejoined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        date: current_date,
        daysOfWeekDisabled: [1, 2, 3, 4, 5, 6]
    });

    input_datejoined.on("change.datetimepicker", ({date, oldDate}) => {
        if (tblSalary !== null) {
            tblSalary.clear().draw();
        }
        fv.revalidateField('date_joined')
            .then(function (status) {
                if (status === 'Valid') {
                    generate_salary();
                }
            });
    });

    $('#tblSalary tbody').on('click', 'a[rel="det"]', function () {
        $('.tooltip').remove();
        var td = tblSalary.cell($(this).closest('td, li')).index(),
            rows = tblSalary.row(td.row).data();
        $('#tblAssistance').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering: false,
            lengthChange: false,
            searching: false,
            paging: false,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_det_assistance',
                    'id': rows.id,
                    'date_joined': input_datejoined.val(),
                },
                dataSrc: ""
            },
            columns: [
                {"data": "date_joined"},
                {"data": "dscto"},
                {"data": "motive_perm"},
                {"data": "state"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success">Asistio</span>'
                        }
                        return '<span class="badge badge-danger">Falto</span>'
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
            ]
        });
        $('#tblBonus').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering: false,
            lengthChange: false,
            searching: false,
            paging: false,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_det_bonus',
                    'id': rows.id,
                    'date_joined': input_datejoined.val(),
                },
                dataSrc: ""
            },
            columns: [
                {"data": "sale.nro"},
                {"data": "sale.start_date"},
                {"data": "sale.end_date"},
                {"data": "sale.type_serv.name"},
                {"data": "bonus"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
            ]
        });
        $('.nav-tabs a[href="#home"]').tab('show');
        $('#myModalDetSal').modal('show');
    });
});
