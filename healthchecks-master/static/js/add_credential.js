$(function() {
    var form = document.getElementById("add-credential-form");
    var optionsBytes = Uint8Array.from(atob(form.dataset.options), c => c.charCodeAt(0));
    // cbor.js expects ArrayBuffer as input when decoding
    var options = CBOR.decode(optionsBytes.buffer);

    function b64(arraybuffer) {
        return btoa(String.fromCharCode.apply(null, new Uint8Array(arraybuffer)));
    }

    function requestCredentials() {
        // Hide error & success messages, show the "waiting" message
        $("#name-next").addClass("hide");
        $("#waiting").removeClass("hide");
        $("#error").addClass("hide");
        $("#success").addClass("hide");

        navigator.credentials.create(options).then(function(attestation) {
            $("#attestation_object").val(b64(attestation.response.attestationObject));
            $("#client_data_json").val(b64(attestation.response.clientDataJSON));

            // Show the success message and save button
            $("#waiting").addClass("hide");
            $("#success").removeClass("hide");
        }).catch(function(err) {
            // Show the error message
            $("#waiting").addClass("hide");
            $("#error-text").text(err);
            $("#error").removeClass("hide");
        });
    }

    $("#name").on('keypress',function(e) {
        if (e.which == 13) {
            e.preventDefault();
            requestCredentials();
        }
    });

    $("#name-next").click(requestCredentials);
    $("#retry").click(requestCredentials);

});
