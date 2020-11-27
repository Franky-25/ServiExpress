var input_datejoined;
var fvSale;

var tblSearchReps;
var tblRepuests;
var tblEquips;
var tblSearchEquips;
var tblEmps;
var date_range = null;
var select_typeserv;
var date_current = new moment().format("YYYY-MM-DD");

function count_days() {
    var startdate = date_current;
    var enddate = date_current;

    if (date_range !== null) {
        startdate = date_range.startDate.format('YYYY-MM-DD');
        enddate = date_range.endDate.format('YYYY-MM-DD');
    }

    if (startdate !== '' && enddate !== '') {
        var d1 = startdate.split("-");
        var d2 = enddate.split("-");
        new Date(d2[0], d2[1], d2[2]);
        if (d1 <= d2) {
            var difference = Math.floor((Date.parse(startdate) - Date.parse(enddate)) / 86400000);
            difference = difference < 0 ? difference * -1 : difference;
            return difference + 1;
        }
    }
    return 0;
}

var sale = {
    details: {
        veh: '',
        type_serv: '',
        km_current: '',
        start_date: date_current,
        end_date: date_current,
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        repuests: [],
        equips: [],
        emps: [],
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var days = count_days();

        $.each(this.details.repuests, function (i, item) {
            item.pos = i;
            item.cant = parseInt(item.cant);
            item.subtotal = item.cant * parseFloat(item.cost);
            subtotal += item.subtotal;
        });

        $.each(this.details.equips, function (i, item) {
            item.pos = i;
            item.cant = days;
            item.subtotal = days * parseFloat(item.depreciation);
        });

        $.each(this.details.emps, function (i, item) {
            item.pos = i;
            item.subtotal = parseFloat(item.cost);
            // subtotal += parseFloat(item.subtotal);
        });

        var valor_typeserv = 0.00;
        var typeserv = select_typeserv.select2('data')[0];
        if (typeserv.id !== '') {
            valor_typeserv = parseFloat(typeserv.data.price);
        }

        sale.details.subtotal = subtotal + valor_typeserv;
        sale.details.iva = subtotal * iva;
        sale.details.total = subtotal + sale.details.iva;
        $('input[name="subtotal"]').val(sale.details.subtotal.toFixed(0));
        $('input[name="iva"]').val(sale.details.iva.toFixed(0));
        $('input[name="total"]').val(sale.details.total.toFixed(0));
    },
    get_repuests_ids: function () {
        var ids = [];
        $.each(this.details.repuests, function (i, item) {
            ids.push(item.id)
        });
        return ids;
    },
    list_repuests: function () {
        this.calculate_invoice();
        tblRepuests = $('#tblRepuests').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.repuests,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                { data: "id" },
                { data: "name" },
                { data: "type.name" },
                { data: "stock" },
                { data: "cant" },
                { data: "cost" },
                { data: "subtotal" },
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cost" value="' + row.cost + '">';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var frm = $(row).closest('tr');

                frm.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: data.stock,
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
                    });

                frm.find('input[name="cost"]')
                    .TouchSpin({
                        min: 1,
                        max: 100000000,
                        step: 1,
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
                    });

            },
            initComplete: function (settings, json) {

            },
        });
    },
    add_repuest: function (item) {
        this.details.repuests.push(item);
        this.list_repuests();
    },
    list_equips: function () {
        this.calculate_invoice();
        tblEquips = $('#tblEquips').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.equips,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                { data: "id" },
                { data: "prod.name" },
                { data: "serie" },
                { data: "guaranty" },
                { data: "price" },
                { data: "depreciation" },
                { data: "cant" },
                { data: "subtotal" },
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data > 1) {
                            return data + ' años';
                        } else if (data === 1) {
                            return data + ' año';
                        }
                        return 'Sin garantía';
                    }
                },
                {
                    targets: [-1, -3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {

            },
        });
    },
    get_equips_ids: function () {
        var ids = [];
        $.each(this.details.equips, function (i, item) {
            ids.push(item.id)
        });
        return ids;
    },
    add_equip: function (item) {
        this.details.equips.push(item);
        this.list_equips();
    },
    get_emps_ids: function () {
        var ids = [];
        $.each(this.details.emps, function (i, item) {
            ids.push(item.id)
        });
        return ids;
    },
    add_emp: function (item) {
        this.details.emps.push(item);
        this.list_emps();
    },
    list_emps: function () {
        this.calculate_invoice();
        tblEmps = $('#tblEmps').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.emps,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                { data: "id" },
                { data: "emp.user.first_name" },
                { data: "emp.user.last_name" },
                { data: "emp.user.run" },
                { data: "nro" },
                { data: "job.name" },
                { data: "cost" },
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cost" value="' + row.cost + '">';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var frm = $(row).closest('tr');

                frm.find('input[name="cost"]')
                    .TouchSpin({
                        min: 0,
                        max: 100000000,
                        step: 1,
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {

            },
        });
    },
}

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmSale');
    fvSale = FormValidation.formValidation(form, {
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
            date_range: {
                validators: {
                    notEmpty: {
                        message: 'La fecha es obligatoria'
                    },
                }
            },
            veh: {
                validators: {
                    notEmpty: {
                        message: 'Seleccione un vehículo'
                    },
                }
            },
            type_serv: {
                validators: {
                    notEmpty: {
                        message: 'Seleccione un tipo de servicio'
                    },
                }
            },
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
            const iconPlugin = fvSale.getPlugin('icon');
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
            if (date_range !== null) {
                sale.details.start_date = date_range.startDate.format('YYYY-MM-DD');
                sale.details.end_date = date_range.endDate.format('YYYY-MM-DD');
            }
            sale.details.type_serv = $('select[name="type_serv"]').val();
            sale.details.veh = $('select[name="veh"]').val();
            sale.details.km_current = $('input[name="km_current"]').val();

            if (sale.details.repuests.length === 0 && sale.details.emps.length === 0 && sale.details.equips.length === 0) {
                message_error('Debe tener al menos un item en su detalle');
                return false;
            }

            submit_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                {
                    'action': 'add',
                    'items': JSON.stringify(sale.details)
                },
                function () {
                    location.href = fvSale.form.getAttribute('data-url');
                },
            );
        });
});

$(function () {

    select_typeserv = $('select[name="type_serv"]');

    $('input[name="date_range"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        date_range = picker;
        fvSale.revalidateField('date_range');
        sale.list_equips();
    }).on('cancel.daterangepicker', function (ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_current);
        $(this).data('daterangepicker').setEndDate(date_current);
        date_range = picker;
    });

    $('select[name="veh"]').select2({
        theme: 'bootstrap4',
        language: "es"
    }).on('change.select2', function () {
        fvSale.revalidateField('veh');
    });

    select_typeserv.on('change.select2', function () {
        fvSale.revalidateField('type_serv');
        sale.calculate_invoice();
    });

    $('input[name="km_current"]')
        .TouchSpin({
            min: 0.01,
            max: 100000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
            prefix: 'KM'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fvSale.revalidateField('km_current');
        })
        .keypress(function (e) {
            return validate_decimals($(this), e);
        });

    /* Search repuests */

    $('.btnSearchRepuests').on('click', function () {
        tblSearchReps = $('#tblSearchReps').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_repuests',
                    'term': $('input[name="search_repuests"]').val(),
                    'ids': JSON.stringify(sale.get_repuests_ids()),
                },
                dataSrc: ""
            },
            //paging: false,
            //ordering: false,
            //info: false,
            columns: [
                { data: "name" },
                { data: "cost" },
                { data: "stock" },
                { data: "id" },
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        return '<span class="badge badge-warning">' + data + '</span>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<a rel="add" class="btn btn-secondary btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                        }
                        return 'No se puede agregar'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({ 'background': '#dc3345', 'color': 'white' });
                }
            },
        });
        $('#myModalSearchReps').modal('show');
    });

    $('#tblSearchReps tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchReps.row($(this).parents('tr')).data();
        row.cant = 1;
        sale.add_repuest(row);
        tblSearchReps.row($(this).parents('tr')).remove().draw();
    });

    $('input[name="search_repuests"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_repuests',
                    'term': request.term,
                    'ids': JSON.stringify(sale.get_repuests_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            if (ui.item.stock === 0) {
                message_error('El stock de este producto esta en 0');
                return false;
            }
            ui.item.cant = 1;
            sale.add_repuest(ui.item);
            $(this).val('').focus();
        }
    });

    $('#tblRepuests tbody')
        .on('change', 'input[name="cant"]', function () {
            var td = tblRepuests.cell($(this).closest('td, li')).index();
            var index = parseInt(td.row);
            sale.details.repuests[index].cant = parseInt($(this).val());
            sale.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = sale.details.repuests[index].subtotal.toFixed(0);
            $('td:eq(6)', tr).html('$' + subtotal);
        })
        .on('change', 'input[name="cost"]', function () {
            var td = tblRepuests.cell($(this).closest('td, li')).index();
            var index = parseInt(td.row);
            sale.details.repuests[index].cost = parseFloat($(this).val());
            sale.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = sale.details.repuests[index].subtotal.toFixed(0);
            $('td:eq(6)', tr).html('$' + subtotal);
        })
        .on('click', 'a[rel="remove"]', function () {
            var td = tblRepuests.cell($(this).closest('td, li')).index();
            var index = parseInt(td.row);
            sale.details.repuests.splice(index, 1);
            sale.list_repuests();
        });

    $('.btnClearRepuests').on('click', function () {
        $('input[name="search_repuests"]').val('').focus();
    });

    $('.btnRemoveAllRepuests').on('click', function () {
        if (items.details.repuests.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los repuestos/herramientas de tu detalle?', function () {
            items.details.repuests = [];
            items.list_repuests();
        });
    });

    /* Equips */

    $('.btnSearchEquips').on('click', function () {
        tblSearchEquips = $('#tblSearchEquips').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_equips',
                    'term': $('input[name="search_equips"]').val(),
                    'ids': JSON.stringify(sale.get_equips_ids()),
                },
                dataSrc: ""
            },
            //paging: false,
            //ordering: false,
            //info: false,
            columns: [
                { data: "prod.name" },
                { data: "price" },
                { data: "serie" },
                { data: "guaranty" },
                { data: "depreciation" },
                { data: "id" },
            ],
            columnDefs: [
                {
                    targets: [-5, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data > 1) {
                            return data + ' años';
                        } else if (data === 1) {
                            return data + ' año';
                        }
                        return 'Sin garantía';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-secondary btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
        });
        $('#myModalSearchEquips').modal('show');
    });

    $('#tblSearchEquips tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchEquips.row($(this).parents('tr')).data();
        row.cant = 1;
        sale.add_equip(row);
        tblSearchEquips.row($(this).parents('tr')).remove().draw();
    });

    $('input[name="search_equips"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_equips',
                    'term': request.term,
                    'ids': JSON.stringify(sale.get_equips_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.cant = 1;
            sale.add_equip(ui.item);
            $(this).val('').focus();
        }
    });

    $('#tblEquips tbody')
        .on('click', 'a[rel="remove"]', function () {
            var td = tblEquips.cell($(this).closest('td, li')).index();
            var index = parseInt(td.row);
            sale.details.equips.splice(index, 1);
            sale.list_equips();
        });

    $('.btnClearEquips').on('click', function () {
        $('input[name="search_equips"]').val('').focus();
    });

    $('.btnRemoveAllEquips').on('click', function () {
        if (sale.details.equips.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los equipos de tu detalle?', function () {
            sale.details.equips = [];
            sale.list_equips();
        });
    });

    /* Employee */

    $('.btnClearEmps').on('click', function () {
        $('input[name="search_emp"]').val('').focus();
    });

    $('input[name="search_emp"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_emps',
                    'term': request.term,
                    'ids': JSON.stringify(sale.get_emps_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            sale.add_emp(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnRemoveAllEmps').on('click', function () {
        if (sale.details.emps.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los empleados de tu detalle?', function () {
            sale.details.emps = [];
            sale.list_emps();
        });
    });

    $('#tblEmps tbody')
        .on('change', 'input[name="cost"]', function () {
            var td = tblEmps.cell($(this).closest('td, li')).index();
            var index = parseInt(td.row);
            sale.details.emps[index].cost = parseFloat($(this).val());
            sale.calculate_invoice();
        })
        .on('click', 'a[rel="remove"]', function () {
            var td = tblEmps.cell($(this).closest('td, li')).index();
            var index = parseInt(td.row);
            sale.details.emps.splice(index, 1);
            sale.list_emps();
        });
});