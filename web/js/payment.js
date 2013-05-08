(function($, Stripe) {
    var displayError = function(message, $element) {
        // Show an error somewhere on the form
        $element.html('<ul class="message-list"><li class="message-list__error icon-text"><i class="icon-close icon-text__icon"></i>' + message + '</li></ul>');
    };

    var stripeResponseHandler = function(status, response) {
        var $form = $('#payment-form');
        if (response.error) {
            displayErrors(response.error.message, $form);
            $form.find('button').prop('disabled', false).removeClass("btn--inactive");
        } else {
            // token contains id, last4, and card type
            var token = response.id;
            // Insert the token into the form so it gets submitted to the server
            $form.append($('<input type="hidden" name="stripe_token" />').val(token));
            // and submit
            $form.get(0).submit();
        }
    };

    $(function($) {
        var $form = $('#payment-form');

        var checkExpiryDate = function(e) {
            var month = $('input[data-stripe="exp-month"]').val();
            var year = $('input[data-stripe="exp-year"]').val();

            if (month !== '' && year !== '') {
                if (!Stripe.validateExpiry(month, year)) {
                    // If it's not, show a validation message
                    displayError("Sorry, that doesn't look like a valid expiry date", $('.expiry-errors'));
                }
                else {
                    $('.expiry-errors').html('');
                }
            }
        };

        $('#payment-form').submit(function(event) {
            // Disable the submit button to prevent repeated clicks
            $form.find('button').prop('disabled', true).addClass("btn--inactive");

            Stripe.createToken($form, stripeResponseHandler);

            // Prevent the form from submitting with the default action
            return false;
        });

        $('input[data-stripe="number"]').blur(function(e) {
            var cardNumber = $(this).val();
            // Check the card looks valid with Stripe's js validation
            if (cardNumber !== '') {
                if (Stripe.validateCardNumber(cardNumber)) {
                    // If it is valid, add a class to show the card type
                    $('.card-type').addClass(Stripe.cardType(cardNumber));
                    $('.card-number-errors').html('');
                }
                else {
                    displayError("Sorry, that doesn't look like a valid card number", $('.card-number-errors'));
                }
            }
        });

        $('input[data-stripe="cvc"]').blur(function(e) {
            var cvc = $(this).val();
            // Check the cvc looks valid with Stripe's js validation
            if (cvc !== '') {
                if (!Stripe.validateCVC(cvc)) {
                    displayError("Sorry, that doesn't look like a valid security code", $('.cvc-errors'));
                }
                else {
                    $('.cvc-errors').html('');
                }
            }
        });

        $('input[data-stripe="exp-month"]').blur(checkExpiryDate);
        $('input[data-stripe="exp-year"]').blur(checkExpiryDate);

    });
})(window.jQuery, window.Stripe);
