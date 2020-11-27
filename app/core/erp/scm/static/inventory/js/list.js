var tblInventory;
var input_datejoined;

function search() {
    tblInventory = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search',
                'purchase': $('select[name="purchase"]').val(),
                'product': $('select[name="product"]').val(),
            },
            dataSrc: ""
        },
        columns: [
            {data: "purch.nro"},
            {data: "purch.date_joined"},
            {data: "prod.name"},
            {data: "prod.type.name"},
            {data: "cant"},
            {data: "saldo"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    console.log(row);
                    if (row.serie !== null) {
                        return '<span class="badge badge-secondary">' + row.serie + '</span>';
                    }
                    return '<span class="badge badge-secondary">' + data + '</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    if (data > 0) {
                        return '<span class="badge badge-success">' + data + '</span>'
                    }
                    return '<span class="badge badge-danger">' + data + '</span>'
                }
            },
        ],
    });
}

$(function () {

    input_datejoined = $('input[name="date_joined"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    }).on('change.select2', function () {
        search();
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    input_datejoined.on('change.datetimepicker', function (e) {
        search();
    });

    search();
});