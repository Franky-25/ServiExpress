var tblPays, table;

function getData() {
    table = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {action: 'load'},
            dataSrc: ""
        },
        columns: [
            {data: "purch.nro"},
            {data: "purch.prov.name"},
            {data: "date_joined"},
            {data: "end_date"},
            {data: "total"},
            {data: "saldo"},
            {data: "state"},
            {data: "state"},
        ],
        columnDefs: [
            {
                targets: [-1],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<a rel="pays" data-toggle="tooltip" title="Pagos" class="btn bg-blue btn-xs btn-flat"><i class="fas fa-dollar-sign"></i></a> ';
                    if (row.state) {
                        buttons += '<a rel="payment" data-toggle="tooltip" title="Abonar" class="btn btn-success btn-xs btn-flat"><i class="far fa-money-bill-alt"></i></a> ';
                    }
                    buttons += '<a href="/erp/frm/debts/pay/delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [2, 3],
                class: 'text-center',
            },
            {
                targets: [4, 5],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + data;
                }
            },
            {
                targets: [-2],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    if (data) {
                        return '<b class="text-danger">Debe dinero aun</span>';
                    }
                    return '<b class="text-success">Pagado</b></span>';
                }
            }
        ],
    });
}

$(function () {

    getData();

    table.on('draw', function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

    $('#data tbody')
        .on('click', 'a[rel="payment"]', function () {
            $('.tooltip').remove();
            var td = table.cell($(this).closest('td, li')).index(),
                rows = table.row(td.row).data();
            $('#cta').val(rows.id);
            $('input[name="valor"]').val('0.00').trigger("touchspin.updatesettings", {max: parseFloat(rows.saldo)});
            $('#debt').html('Valor: (Deuda: ' + rows.saldo + ')');
            input_datejoined.datetimepicker('date', new Date());
            $('#myModalPay').modal('show');
        })
        .on('click', 'a[rel="pays"]', function () {
            $('.tooltip').remove();
            var td = table.cell($(this).closest('td, li')).index(),
                rows = table.row(td.row).data();
            tblPays = $('#tblPays').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                searching: false,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: function (d) {
                        d.action = 'search_pays';
                        d.id = rows.id;
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "id"},
                    {data: "date_joined"},
                    {data: "valor"},
                    {data: "valor"},
                ],
                columnDefs: [
                    {
                        targets: [2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data;
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash fa-1x"></i></a>';
                        }
                    }
                ],
                rowCallback: function (row, data, index) {
                    var desc = "Abono N°" + (index + 1);
                    $('td:eq(0)', row).html(desc);
                },
            });
            tblPays.on('draw', function () {
                $('[data-toggle="tooltip"]').tooltip();
            });
            $('#myModalListPay').modal('show');
        });

    $('#tblPays tbody')
        .on('click', 'a[rel="delete"]', function () {
            $('.tooltip').remove();
            var td = tblPays.cell($(this).closest('td, li')).index(),
                rows = tblPays.row(td.row).data();
            dialog_delete_with_ajax('Notificación',
                '¿Estas seguro de eliminar el registro?',
                pathname,
                {
                    'id': rows.id,
                    'action': 'delete_pay'
                },
                function () {
                    table = table.ajax.reload();
                    tblPays.ajax.reload();
                }
            );
        });

    $('[data-toggle="tooltip"]').tooltip();
});
