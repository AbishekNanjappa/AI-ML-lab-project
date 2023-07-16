$(document).ready(function() {
    $('#prediction-form').on('submit', function(event) {
        event.preventDefault(); // Prevent form submission
        
        // Retrieve input values
        var age = parseFloat($('#age').val());
        var gender = parseInt($('#gender').val());
        var height = parseFloat($('#height').val());
        var weight = parseFloat($('#weight').val());
        var ap_hi = parseFloat($('#ap_hi').val());
        var ap_lo = parseFloat($('#ap_lo').val());
        var cholesterol = $('#cholesterol').val();
        var gluc = $('#gluc').val();
        var smoke = $('#smoke').val();
        var alco = $('#alco').val();
        var active = $('#active').val();
        var bmi = weight / Math.pow(height / 100, 2);
        
        // Create input data object
        var input_data = {
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'ap_hi': ap_hi,
            'ap_lo': ap_lo,
            'cholesterol': cholesterol,
            'gluc': gluc,
            'smoke': smoke,
            'alco': alco,
            'active': active,
            'bmi': bmi
        };
        
        // Perform prediction using AJAX
        $.ajax({
            url: 'http://127.0.0.1:5001/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(input_data),
            success: function(response) {
                var resultText = $('#result-text');
                if (response.prediction === 0) {
                    resultText.text("The patient is not likely to have cardiovascular disease.");
                } else {
                    resultText.text("The patient is likely to have cardiovascular disease.");
                }
                $('#prediction-result').show();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});