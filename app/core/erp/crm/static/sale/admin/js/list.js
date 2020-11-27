$(function () {
    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var td = table.cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data();
        var id = parseInt(rows[0]);
        $('#tblEmps').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_det_emps',
                    'id': id
                },
                dataSrc: ""
            },
            columns: [
                { data: "cont.emp.user.first_name" },
                { data: "cont.emp.user.last_name" },
                { data: "cont.emp.user.run" },
                { data: "cont.nro" },
                { data: "cont.job.name" },
                { data: "bonus" },
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
            ]
        });
        $('#tblEquips').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_det_equips',
                    'id': id
                },
                dataSrc: ""
            },
            columns: [
                { data: "rec.prod.name" },
                { data: "rec.serie" },
                { data: "rec.guaranty" },
                { data: "rec.price" },
                { data: "price" },
                { data: "cant" },
                { data: "total" },
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
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ]
        });
        $('#tblRepuests').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_det_repuests',
                    'id': id
                },
                dataSrc: ""
            },
            columns: [
                { data: "rec.prod.name" },
                { data: "cant" },
                { data: "price" },
                { data: "total" },
            ],
            columnDefs: [
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                }
            ]
        });
        $('#myModalDet').modal('show');
    });
});
