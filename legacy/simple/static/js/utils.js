function delete_customer(url) {
    var deleteCustomer = $.ajax({method: "DELETE",
                             url: url});
    deleteCustomer.done(function(data) {
        $("#detail").empty().append(data);
        console.log("delete_customer done");
    });
    deleteCustomer.fail(function(data) {
        console.log("delete_customer fail");
    });
}

function modify_customer(url) {
        var modifyCustomer = $.ajax({method: "GET",
                             url: url});
    modifyCustomer.done(function(data) {
        $("#detail").empty().append(data);
        console.log("modify_customer done");
    });
    modifyCustomer.fail(function(data) {
        console.log("modify_customer fail");
    });
}
