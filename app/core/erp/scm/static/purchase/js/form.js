var tblRepuests, tblSearchRepuests;
var prov = null;
var tblEquips, tblSearchEquips, equip;
var fvComp;
var fvProvider;
var input_datejoined;
var input_endate;
var pnlEndDate;
var defaultDate;

var tblSeries;
var fvSerie;
var input_serie;

var items = {
    details: {
        prov: '',
        date_joined: '',
        end_date: '',
        subtotal: 0.00,
        iva: 0.00,
        dscto: 0.00,
        total: 0.00,
        payment: 0,
        repuests: [],
        equips: [],
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.details.repuests, function (i, item) {
            item.pos = i;
            item.cant = parseInt(item.cant);
            item.subtotal = item.cant * parseFloat(item.cost);
            subtotal += item.subtotal;
        });

        $.each(this.details.equips, function (i, item) {
            item.pos = i;
            item.cant = parseInt(item.cant);
            item.subtotal = item.cant * parseFloat(item.cost);
            subtotal += item.subtotal;
        });
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
                {data: "id"},
                {data: "name"},
                {data: "cant"},
                {data: "cost"},
                {data: "subtotal"},
            ],
            columnDefs: [
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
                        max: 1000000000,
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
    get_repuests_ids: function () {
        var ids = [];
        $.each(this.details.repuests, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
    add_repuest: function (item) {
        this.details.repuests.push(item);
        this.list_repuests();
    },
    get_series: function () {
        var data = [];
        $.each(this.details.equips, function (key, value) {
            if (value.series.length > 0) {
                $.each(value.series, function (i, item) {
                    data.push(item);
                });
            }
        });
        return data;
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
                {data: "id"},
                {data: "name"},
                {data: "cant"},
                {data: "guaranty"},
                {data: "cost"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var html = '<div class="input-group input-group-sm">';
                        html += '<input type="text" class="form-control text-center" disabled value="' + row.series.length + '">';
                        html += '<span class="input-group-append">';
                        html += '<a class="btn btn-primary btn-xs btn-flat" rel="serie"><i class="fas fa-barcode"></i></a>';
                        html += '</span>';
                        html += '</div>';
                        return html;
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
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="guaranty" value="' + row.guaranty + '">';
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

                frm.find('input[name="guaranty"]')
                    .TouchSpin({
                        min: 1,
                        max: 1000000000,
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
    get_equips_ids: function () {
        var ids = [];
        $.each(this.details.equips, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
    add_equip: function (item) {
        this.details.equips.push(item);
        this.list_equips();
    },
    list_series: function (pos) {
        var series = [];
        $.each(this.details.equips[pos].series, function (key, value) {
            series.push({
                'pos': key, 'serie': value
            })
        });

        tblSeries = $('#tblSeries').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: series,
            columns: [
                {data: "pos"},
                {data: "serie"},
            ],
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columnDefs: [
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
    }
};


document.addEventListener('DOMContentLoaded', function (e) {
    const frmIngress = document.getElementById('frmComp');
    fvComp = FormValidation.formValidation(frmIngress, {
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
                payment: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una forma de pago'
                        },
                    }
                },
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
                end_date: {
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
            const iconPlugin = fvComp.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmIngress.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var url_refresh = frmIngress.getAttribute('data-url');

            if (prov === null) {
                message_error('Debe tener un proveedor seleccionado');
                $('input[name="search_prov"]').focus().select();
                return false;
            }

            items.details.prov = prov.id;
            items.details.date_joined = $('input[name="date_joined"]').val();
            items.details.end_date = $('input[name="end_date"]').val();
            items.details.payment = $('select[name="payment"]').val();

            if (items.details.equips.length === 0 && items.details.repuests.length === 0) {
                message_error('Debe tener al menos un item de repuesto o equipo en el detalle de la compra');
                return false;
            }

            submit_with_ajax('Notificación',
                '¿Estas seguro de guardar la siguiente compra?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'items': JSON.stringify(items.details)
                },
                function () {
                    location.href = url_refresh;
                },
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    const frmProvider = document.getElementById('frmProvider');
    fvProvider = FormValidation.formValidation(frmProvider, {
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
                                    obj: frmProvider.querySelector('[name="name"]').value,
                                    id: 0,
                                    type: 'name',
                                    action: 'validate_prov'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                rut: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 13
                        },
                        digits: {},
                        // callback: {
                        //     message: 'Introduce un número de rut es inválido',
                        //     callback: function (input) {
                        //         return validate_dni_ruc(input.value);
                        //     }
                        // },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmProvider.querySelector('[name="rut"]').value,
                                    id: 0,
                                    type: 'rut',
                                    action: 'validate_prov'
                                };
                            },
                            message: 'El número de rut ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                mobile: {
                    validators: {
                        // notEmpty: {},
                        // stringLength: {
                        //     min: 10
                        // },
                        digits: {},
                    }
                },
                email: {
                    validators: {
                        // notEmpty: {},
                        // stringLength: {
                        //     min: 5
                        // },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El email no es correcto'
                        },
                    }
                },
                address: {
                    validators: {
                        // stringLength: {
                        //     min: 4,
                        // }
                    }
                }
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
            const iconPlugin = fvProvider.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmProvider.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            submit_with_ajax('Notificación', '¿Estas seguro de guardar el siguiente proveedor?', pathname,
                {
                    name: $('#id_name').val(),
                    mobile: $('#id_mobile').val(),
                    address: $('#id_address').val(),
                    email: $('#id_email').val(),
                    rut: $('#id_ruc').val(),
                    action: 'create_prov'
                },
                function () {
                    $('#myModalAddProv').modal('hide');
                }
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmSeries');
    fvSerie = FormValidation.formValidation(form, {
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
                serie: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    pk: form.querySelector('[name="serie"]').value,
                                    series: JSON.stringify(items.get_series()),
                                    action: 'validate_serie'
                                };
                            },
                            message: 'La serie ya se encuentra registrada',
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
            const iconPlugin = fvSerie.getPlugin('icon');
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
            var serie = input_serie.val();
            var pos = parseInt(equip.pos);
            items.details.equips[pos].series.push(serie);
            fvSerie.resetForm(true);
            input_serie.val('').focus();
            items.list_series(pos);
        });
});

$(function () {

    pnlEndDate = $('#pnl_end_date');
    defaultDate = new moment().format("YYYY-MM-DD");
    input_datejoined = $('input[name="date_joined"]');
    input_endate = $('input[name="end_date"]');
    input_serie = $('input[name="serie"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('select[name="payment"]')
        .on('change.select2', function () {
            fvComp.revalidateField('payment');
            var id = $(this).val();
            var start_date = input_datejoined.val();
            input_endate.datetimepicker('minDate', start_date);
            input_endate.datetimepicker('date', start_date);
            pnlEndDate.hide();
            if (id === 'credito') {
                pnlEndDate.show();
            }
        });

    $('input[name="search_prov"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    action: 'search_prov',
                    term: request.term,
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
            $(this).val(ui.item.name);
            $(this).blur();
            prov = ui.item;
            $('#pruc').val(ui.item.rut);
        }
    });

    $('.btnClearProv').on('click', function () {
        prov = null;
        $('#pruc').val('');
        $('input[name="search_prov"]').val('').focus();
    });

    $('.btnAddProv').on('click', function () {
        $('#myModalAddProv').modal('show');
    });

    $('#myModalAddProv').on('hidden.bs.modal', function () {
        fvProvider.resetForm(true);
    });

    $('input[name="rut"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    input_datejoined.on('change.datetimepicker', function (e) {
        fvComp.revalidateField('date_joined');
        input_endate.datetimepicker('minDate', e.date);
        input_endate.datetimepicker('date', e.date);
    });

    input_endate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: defaultDate
    });

    input_endate.datetimepicker('date', input_endate.val());

    input_endate.on('change.datetimepicker', function (e) {
        fvComp.revalidateField('end_date');
    });

    pnlEndDate.hide();

    /* Repuestos */

    $('.btnRemoveAllRep').on('click', function () {
        if (items.details.repuests.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los repuestos de tu detalle?', function () {
            items.details.repuests = [];
            items.list_repuests();
        });
    });

    $('input[name="searchrep"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_repuests',
                    'term': request.term,
                    'ids': JSON.stringify(items.get_repuests_ids()),
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
            items.add_repuest(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearRep').on('click', function () {
        $('input[name="searchrep"]').val('').focus();
    });

    $('#tblRepuests tbody')
        .on('change', 'input[name="cant"]', function () {
            var td = tblRepuests.cell($(this).closest('td, li')).index();
            var row = tblRepuests.row(td.row).data();
            items.details.repuests[row.pos].cant = parseInt($(this).val());
            items.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = items.details.repuests[row.pos].subtotal.toFixed(0);
            $('td:eq(4)', tr).html('$' + subtotal);
        })
        .on('change', 'input[name="cost"]', function () {
            var td = tblRepuests.cell($(this).closest('td, li')).index();
            var row = tblRepuests.row(td.row).data();
            items.details.repuests[row.pos].cost = parseFloat($(this).val()).toFixed(0);
            items.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = items.details.repuests[row.pos].subtotal.toFixed(0);
            $('td:eq(4)', tr).html('$' + subtotal);
        })
        .on('click', 'a[rel="remove"]', function () {
            var td = tblRepuests.cell($(this).closest('td, li')).index();
            var row = tblRepuests.row(td.row).data();
            items.details.repuests.splice(row.pos, 1);
            items.list_repuests();
        });

    $('.btnSearchRep').on('click', function () {
        tblSearchRepuests = $('#tblSearchRepuests').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_repuests',
                    'term': $('input[name="searchrep"]').val(),
                    'ids': JSON.stringify(items.get_repuests_ids()),
                },
                dataSrc: ""
            },
            //paging: false,
            //ordering: false,
            //info: false,
            columns: [
                {data: "name"},
                {data: "cost"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
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
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
        });
        $('#myModalSearchRepuests').modal('show');
    });

    $('#tblSearchRepuests tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchRepuests.row($(this).parents('tr')).data();
        row.cant = 1;
        items.add_repuest(row);
        tblSearchRepuests.row($(this).parents('tr')).remove().draw();
    });

    /* Equips */

    $('.btnRemoveAllEquip').on('click', function () {
        if (items.details.equips.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los equipos de tu detalle?', function () {
            items.details.equips = [];
            items.list_equips();
        });
    });

    $('.btnClearEquip').on('click', function () {
        $('input[name="searchequip"]').val('').focus();
    });

    $('.btnSearchEquip').on('click', function () {
        tblSearchEquips = $('#tblSearchEquips').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_equips',
                    'term': $('input[name="searchequip"]').val(),
                    'ids': JSON.stringify(items.get_equips_ids()),
                },
                dataSrc: ""
            },
            //paging: false,
            //ordering: false,
            //info: false,
            columns: [
                {data: "name"},
                {data: "cost"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
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
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
        });
        $('#myModalSearchEquips').modal('show');
    });

    $('input[name="searchequip"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_equips',
                    'term': request.term,
                    'ids': JSON.stringify(items.get_equips_ids()),
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
            ui.item.guaranty = 0;
            ui.item.series = [];
            items.add_equip(ui.item);
            $(this).val('').focus();
        }
    });

    $('#tblEquips tbody')
        .on('click', 'a[rel="serie"]', function () {
            var td = tblEquips.cell($(this).closest('td, li')).index();
            equip = tblEquips.row(td.row).data();
            items.list_series(parseInt(equip.pos));
            fvSerie.resetForm(true);
            $('#myModalSeries').modal('show');
        })
        .on('change', 'input[name="guaranty"]', function () {
            var td = tblEquips.cell($(this).closest('td, li')).index();
            var row = tblEquips.row(td.row).data();
            items.details.equips[row.pos].guaranty = parseInt($(this).val());
        })
        .on('change', 'input[name="cost"]', function () {
            var td = tblEquips.cell($(this).closest('td, li')).index();
            var row = tblEquips.row(td.row).data();
            items.details.equips[row.pos].cost = parseFloat($(this).val());
            items.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = items.details.equips[row.pos].subtotal.toFixed(0);
            $('td:eq(5)', tr).html('$' + subtotal);
        })
        .on('click', 'a[rel="remove"]', function () {
            var td = tblEquips.cell($(this).closest('td, li')).index();
            var row = tblEquips.row(td.row).data();
            items.details.equips.splice(row.pos, 1);
            items.list_equips();
        });

    $('#tblSeries tbody').on('click', 'a[rel="remove"]', function () {
        var td = tblSeries.cell($(this).closest('td, li')).index();
        var row = tblSeries.row(td.row).data();
        var pos = parseInt(equip.pos);
        items.details.equips[pos].series.splice(row.pos, 1);
        items.list_series(pos)
    });

    $('#tblSearchEquips tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchEquips.row($(this).parents('tr')).data();
        row.cant = 1;
        row.guaranty = 0;
        row.series = [];
        items.add_equip(row);
        tblSearchEquips.row($(this).parents('tr')).remove().draw();
    });

    $('.btnRemoveAllSeries').on('click', function () {
        var pos = parseInt(equip.pos);
        items.details.equips[pos].series = [];
        items.list_series(pos)
    });

    $('.btnClearSerie').on('click', function () {
        fvSerie.resetForm(true);
        input_serie.val('').focus();
    });

    $('#myModalSeries').on('hidden.bs.modal', function () {
        items.list_equips();
    });

    $('.btnGenSerie').on('click', function () {
        $.ajax({
            url: pathname,
            data: {'action': 'generate_serie'},
            method: 'POST',
            dataType: 'json',
            beforeSend: function () {
                $('.tooltip').remove();
                fvSerie.resetForm(true);
                input_serie.val('');
            },
            success: function (request) {
                console.log(request);
                if (!request.hasOwnProperty('error')) {
                    input_serie.val(request.serie);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
    });
});