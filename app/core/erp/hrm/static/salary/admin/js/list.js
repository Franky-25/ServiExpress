var input_datejoined;
var current_date;
var tblSalary = null;


function search_salary() {
    $('.btnDeleteSalary').prop('disabled', true);

    tblSalary = $('#tblSalary').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search_salary',
                'date_joined': input_datejoined.val()
            },
            dataSrc: ""
        },
        columns: [
            {"data": "cont.emp.user.full_name"},
            {"data": "cont.job.name"},
            {"data": "week"},
            {"data": "cont.rmu"},
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
            $('.btnDeleteSalary').prop('disabled', json.length === 0);
        },
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
        search_salary();
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
                    'id': rows.cont.id,
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
                    'id': rows.cont.id,
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

    $('.btnDeleteSalary').on('click', function () {
        location.href = '/erp/hrm/salary/delete/' + input_datejoined.val() + '/';
    });
});
