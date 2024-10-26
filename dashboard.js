// $(function () {
//     //Json data by api call for order table
//     $.get(orderListApiUrl, function (response) {
//         if(response) {
//             var table = '';
//             var totalCost = 0;
//             $.each(response, function(index, order) {
//                 totalCost += parseFloat(order.total);
//                 table += '<tr>' +
//                     '<td>'+ order.datetime +'</td>'+
//                     '<td>'+ order.order_id +'</td>'+
//                     '<td>'+ order.customer_name +'</td>'+
//                     '<td>'+ order.total.toFixed(2) +' Rs</td></tr>';
//             });
//             table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>'+ totalCost.toFixed(2) +' Rs</b></td></tr>';
//             $("table").find('tbody').empty().html(table);
//         }
//     });
// });


$(function () {
    // Json data by API call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                // Ensure 'total' is not undefined before processing
                var orderTotal = parseFloat(order.total_cost) || 0;
                totalCost += orderTotal;
                
                table += '<tr>' +
                    '<td>'+ order.datetime +'</td>'+
                    '<td>'+ order.order_id +'</td>'+
                    '<td>'+ order.customer_name +'</td>'+
                    '<td>'+ orderTotal.toFixed(2) +' Rs</td></tr>';
            });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>'+ totalCost.toFixed(2) +' Rs</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});