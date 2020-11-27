var btnRemoveAssist;
var input_daterange = null;

function getAssists() {
    var parameters = { 'action': 'load' };
    if (input_daterange !== null) {
        parameters['start_date'] = input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD');
        parameters['end_date'] = input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD');
    }
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columns: [
            { data: "date_joined" },
            { data: "cont.emp.user.full_name" },
            { data: "cont.emp.user.run" },
            { data: "cont.job.name" },
            { data: "state" },
            { data: "motive_perm" },
            { data: "dscto" },
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
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (!$.isEmptyObject(row.motive_perm)) {
                        return row.motive_perm;
                    }
                    return 'Sin novedad';
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
                    if (row.state) {
                        return '<span class="badge badge-success">Si</span>';
                    }
                    return '<span class="badge badge-danger">No</span>';
                }
            },
        ],
        initComplete: function (settings, json) {
            btnRemoveAssist.prop('disabled', $.isEmptyObject(json));
        }
    });
}

$(function () {

    input_daterange = $('input[name="date_range"]');
    btnRemoveAssist = $('.btnRemoveAssist');

    btnRemoveAssist.prop('disabled', true);

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        }).on('change', function (ev, picker) {
        });

    $('.applyBtn').hide();

    $('.btnSearchAssist').on('click', function () {
        getAssists();
    });

    btnRemoveAssist.on('click', function () {
        location.href = pathname + 'delete/' + input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD') + '/' + input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD') + '/';
    });

    getAssists();
});
