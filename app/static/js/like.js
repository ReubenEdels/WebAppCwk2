$(document).ready(function() {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });


    $('.like-button').click(function() {
        var reviewId = $(this).data('review-id');
        
        $.ajax({
            url: '/like/' + reviewId,
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                var likes = response.likes;
                var likeCount = likes.length;
                var displayText = ''
                var  buttonText = ''

                var action = response.action;
                if (action == 'like') {
                    buttonText = 'Unlike';
                } else if (action == 'unlike') {
                    buttonText = 'Like';
                }

                if (likeCount == 0) {
                    displayText = 'No likes yet.';
                } else if (likeCount == 1) {
                    displayText = 'Liked by ' + likes[0];
                } else if (likeCount == 2) {
                    displayText = 'Liked by ' + likes[0] + ' & ' + likes[1];
                } else {
                    displayText = 'Liked by ' + likes[0] + ', ' + likes[1] + ' & ' + (likeCount - 2) + ' more';
                }

                $('#like-button-' + reviewId).html(buttonText);
                $('#likes-' + reviewId).html(displayText);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});