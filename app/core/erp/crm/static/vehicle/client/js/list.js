var tblVehicle;
var fv;
var vehicle;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmKmCurrent');
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
                km_current: {
                    validators: {
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
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
            submit_with_ajax('Notificación',
                '¿Estas seguro de actualizar el km?',
                pathname,
                {
                    'action': 'set_km_current',
                    'id': vehicle.id,
                    'km_current': $('input[name="km_current"]').val(),
                },
                function () {
                    //tblVehicle.ajax.reload();
                    $('#myModalKmCurrent').modal('hide');
                    location.reload();
                }
            );
        });
});

$(function () {
    tblVehicle = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search_vehs',
            },
            dataSrc: ""
        },
        columns: [
            {data: "cli.user.full_name"},
            {data: "plaque"},
            {data: "year"},
            {data: "exemplar.name"},
            {data: "exemplar.brand.name"},
            {data: "km_current"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return row.km_current + ' KM';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a class="btn btn-success btn-xs btn-flat" rel="km_current"><i class="fas fa-tachometer-alt"></i></a>';
                }
            },
        ]
    });

    $('input[name="km_current"]').TouchSpin({
        min: 0.01,
        max: 100000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    }).on('change touchspin.on.min touchspin.on.max', function () {
        fv.revalidateField('km_current');
    }).keypress(function (e) {
        return validate_decimals($(this), e);
    });

    $('#data tbody').on('click', 'a[rel="km_current"]', function () {
        $('.tooltip').remove();
        var td = tblVehicle.cell($(this).closest('td, li')).index(),
            rows = tblVehicle.row(td.row).data();
        vehicle = rows;
        $('input[name="km_current"]').val(rows.km_current);
        $('#myModalKmCurrent').modal('show');
    });
});