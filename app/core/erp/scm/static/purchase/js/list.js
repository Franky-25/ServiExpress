$(function () {
    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var td = table.cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data();
        var id = parseInt(rows[0]);
        $('#tblRepuests').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_repuests',
                    'id': id
                },
                dataSrc: ""
            },
            columns: [
                {data: "prod.name"},
                {data: "price"},
                {data: "cant"},
                {data: "total"},
            ],
            columnDefs: [
                {
                    targets: [-1, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                }
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
                    'action': 'search_equips',
                    'id': id
                },
                dataSrc: ""
            },
            columns: [
                {data: "prod.name"},
                {data: "serie"},
                {data: "guaranty"},
                {data: "price"},
                {data: "total"},
                {data: "state"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success">Activo</span>';
                        }
                        return '<span class="badge badge-danger">Inactivo</span>';
                    }
                },
                {
                    targets: [-2, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(0);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data > 0) {
                            return data + ' Años';
                        }
                        if (data === 1) {
                            return data + ' Año';
                        }
                        return 'Sin garantía';
                    }
                }
            ]
        });
        $('.nav-tabs a[href="#home"]').tab('show')
        $('#myModalDet').modal('show');
    });
});
