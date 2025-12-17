// Main JavaScript file for custom functionality

$(document).ready(function() {
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Initialize popovers
    $('[data-toggle="popover"]').popover();
    
    // Smooth scrolling for anchor links
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();
        
        $('html, body').animate(
            {
                scrollTop: $($(this).attr('href')).offset().top,
            },
            500,
            'linear'
        );
    });
    
    // Hero video play/pause on hover
    var heroVideo = document.getElementById('heroVideo');
    if (heroVideo) {
        $('.hero-section').hover(
            function() {
                heroVideo.play();
            },
            function() {
                heroVideo.pause();
            }
        );
    }
    
    // Form submission handling
    $('form').submit(function() {
        var submitButton = $(this).find('button[type="submit"]');
        submitButton.prop('disabled', true);
        submitButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...');
    });
});