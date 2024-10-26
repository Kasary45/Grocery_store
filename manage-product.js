var productModal = $("#productModal");
    $(function () {

        //JSON data by API call
        $.get(productListApiUrl, function (response) {
            if(response) {
                var table = '';
                $.each(response, function(index, product) {
                    table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
                        '<td>'+ product.name +'</td>'+
                        '<td>'+ product.uom_name +'</td>'+
                        '<td>'+ product.price_per_unit +'</td>'+
                        '<td><span class="btn btn-xs btn-danger delete-product">Delete</span></td></tr>';
                });
                $("table").find('tbody').empty().html(table);
            }
        });
    });

    // Save Product
    // $("#saveProduct").on("click", function () {
    //     // If we found id value in form then update product detail
    //     var data = $("#productForm").serializeArray();
    //     var requestPayload = {
    //         product_name: null,
    //         uom_id: null,
    //         price_per_unit: null
    //     };
    //     for (var i=0;i<data.length;++i) {
    //         var element = data[i];
    //         switch(element.name) {
    //             case 'name':
    //                 requestPayload.product_name = element.value;
    //                 break;
    //             case 'uoms':
    //                 requestPayload.uom_id = element.value;
    //                 break;
    //             case 'price':
    //                 requestPayload.price_per_unit = element.value;
    //                 break;
    //         }
    //     }
    //     callApi("POST", productSaveApiUrl, {
    //         'data': JSON.stringify(requestPayload)
    //     });
    // });

// // Save Product
// $("#saveProduct").on("click", function () {
//     var data = $("#productForm").serializeArray();
//     var requestPayload = {
//         product_name: null,
//         uom_id: null,
//         price_per_unit: null
//     };
    
//     // Prepare requestPayload from form data
//     for (var i = 0; i < data.length; ++i) {
//         var element = data[i];
//         switch (element.name) {
//             case 'name':
//                 requestPayload.product_name = element.value; // Ensure 'name' matches the input field's name
//                 break;
//             case 'uoms':
//                 requestPayload.uom_id = element.value; // Ensure 'uoms' matches the select field's name
//                 break;
//             case 'price':
//                 requestPayload.price_per_unit = element.value; // Ensure 'price' matches the input field's name
//                 break;
//         }
//     }
    
//     console.log(requestPayload); // Debugging: Log the payload to ensure it’s correct

//     callApi("POST", productSaveApiUrl, requestPayload); // Call API for insertion
// });

// Save Product
$("#saveProduct").on("click", function () {
    // If we found id value in form then update product detail
    var data = $("#productForm").serializeArray();
    var requestPayload = {
        product_name: null,
        uom_id: null,
        price_per_unit: null
    };

    for (var i = 0; i < data.length; ++i) {
        var element = data[i];
        switch (element.name) {
            case 'name':
                requestPayload.product_name = element.value.trim(); // Trim whitespace
                break;
            case 'uoms':
                requestPayload.uom_id = element.value ? parseInt(element.value) : null; // Convert to integer or null
                break;
            case 'price':
                requestPayload.price_per_unit = element.value ? parseFloat(element.value) : null; // Convert to float or null
                break;
        }
    }

    // Check if required fields are valid
    if (!requestPayload.product_name || requestPayload.uom_id === null || requestPayload.price_per_unit === null) {
        alert("All fields are required and must be valid.");
        return; // Stop the API call if validation fails
    }

    console.log(requestPayload); // Log for debugging
    callApi("POST", productSaveApiUrl, requestPayload); // Send request without additional data wrapping
});


















































    $(document).on("click", ".delete-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            product_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
        if (isDelete) {
            callApi("POST", productDeleteApiUrl, data);
        }
    });

    productModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#name, #unit, #price").val('');
        productModal.find('.modal-title').text('Add New Product');
    });

    // productModal.on('show.bs.modal', function(){
    //     //JSON data by API call
    //     $.get(uomListApiUrl, function (response) {
    //         if(response) {
    //             var options = '<option value="">--Select--</option>';
    //             $.each(response, function(index, uom) {
    //                 options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
    //             });
    //             $("#uoms").empty().html(options);
    //         }
    //     });
    // });


    productModal.on('show.bs.modal', function() {
        // JSON data by API call
        $.get(uomListApiUrl, function(response) {
            if (response) {
                var options = '<option value="">--Select--</option>';
                $.each(response, function(index, uom) {
                    options += '<option value="' + uom.uom_id + '">' + uom.uom_name + '</option>';
                });
                $("#uoms").empty().html(options);
            }
        }).fail(function() {
            alert("Failed to load UOMs. Please try again.");
        });
    });