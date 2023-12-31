
$(document).ready(function () {
    const form = $("#chatRoomForm");
    const responseDiv = $("#responseDiv");

    form.on("submit", function (e) {
        e.preventDefault();

        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success: function (data) {
                if (data.success) {
                    // Handle a successful response
                    responseDiv.html(`<div class="alert alert-success">${data.message}</div>`);
                    // Redirect to the index page
                    window.location.href = "{% url 'index' %}";
                } else {
                    // Handle errors
                    responseDiv.html(`<div class="alert alert-danger">${data.message}</div>`);
                }
            },
            error: function (error) {
                console.error(error);
            },
        });
    });
});

