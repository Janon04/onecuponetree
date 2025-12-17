/**
 * One Cup Initiative Admin JavaScript Enhancements
 */

(function($) {
    'use strict';
    
    $(document).ready(function() {
        
        // Add loading animation to forms
        $('form').on('submit', function() {
            var submitBtn = $(this).find('input[type="submit"], button[type="submit"]');
            if (submitBtn.length) {
                submitBtn.addClass('admin-loading');
                submitBtn.prop('disabled', true);
                
                setTimeout(function() {
                    submitBtn.removeClass('admin-loading');
                    submitBtn.prop('disabled', false);
                }, 3000);
            }
        });
        
        // Enhanced table row hover effects
        $('.results tbody tr').hover(
            function() {
                $(this).css('transform', 'scale(1.01)');
                $(this).css('transition', 'all 0.2s ease');
            },
            function() {
                $(this).css('transform', 'scale(1)');
            }
        );
        
        // Auto-resize textareas
        $('textarea').each(function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        $('textarea').on('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Add confirmation dialogs for dangerous actions
        $('.deletelink').on('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
                return false;
            }
        });
        
        // Enhanced search functionality
        var searchTimeout;
        $('#searchbar').on('input', function() {
            var $this = $(this);
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(function() {
                if ($this.val().length >= 3) {
                    $this.css('border-color', '#28a745');
                } else if ($this.val().length > 0) {
                    $this.css('border-color', '#ffc107');
                } else {
                    $this.css('border-color', '#d0d0d0');
                }
            }, 300);
        });
        
        // Quick stats display
        function updateQuickStats() {
            $('.admin-quick-stat').each(function() {
                var $stat = $(this);
                var value = parseInt($stat.data('value')) || 0;
                var animationDuration = 1000;
                var increment = value / (animationDuration / 16);
                var current = 0;
                
                var timer = setInterval(function() {
                    current += increment;
                    if (current >= value) {
                        current = value;
                        clearInterval(timer);
                    }
                    $stat.text(Math.floor(current).toLocaleString());
                }, 16);
            });
        }
        
        updateQuickStats();
        
        // Image preview enhancement
        $('input[type="file"]').on('change', function() {
            var input = this;
            var $preview = $(input).siblings('.image-preview');
            
            if (!$preview.length) {
                $preview = $('<div class="image-preview" style="margin-top: 10px;"></div>');
                $(input).after($preview);
            }
            
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    $preview.html(
                        '<img src="' + e.target.result + '" style="max-width: 200px; max-height: 150px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />'
                    );
                };
                reader.readAsDataURL(input.files[0]);
            } else {
                $preview.empty();
            }
        });
        
        // Auto-save draft functionality for rich text editors
        var autoSaveTimeout;
        $('.cke_editable, textarea[name*="content"], textarea[name*="description"]').on('input', function() {
            var $field = $(this);
            clearTimeout(autoSaveTimeout);
            
            autoSaveTimeout = setTimeout(function() {
                // Add auto-save indicator
                var $indicator = $field.siblings('.auto-save-indicator');
                if (!$indicator.length) {
                    $indicator = $('<div class="auto-save-indicator" style="font-size: 12px; color: #666; margin-top: 5px;"></div>');
                    $field.after($indicator);
                }
                
                $indicator.html('<i class="fas fa-save"></i> Draft saved at ' + new Date().toLocaleTimeString());
                
                setTimeout(function() {
                    $indicator.fadeOut();
                }, 3000);
            }, 2000);
        });
        
        // Enhanced filter sidebar
        $('#changelist-filter h3').on('click', function() {
            $(this).next('ul').slideToggle(200);
            $(this).toggleClass('collapsed');
        });
        
        // Responsive table enhancements
        function makeTablesResponsive() {
            $('.results table').each(function() {
                if (!$(this).parent().hasClass('table-responsive')) {
                    $(this).wrap('<div class="table-responsive"></div>');
                }
            });
        }
        
        makeTablesResponsive();
        
        // Add tooltips to action buttons
        $('.button, .addlink, .changelink, .deletelink').each(function() {
            var $btn = $(this);
            var title = $btn.attr('title') || $btn.text().trim();
            
            if (title) {
                $btn.attr('data-toggle', 'tooltip');
                $btn.attr('data-placement', 'top');
                $btn.attr('title', title);
            }
        });
        
        // Initialize tooltips if Bootstrap is available
        if (typeof $().tooltip === 'function') {
            $('[data-toggle="tooltip"]').tooltip();
        }
        
        // Keyboard shortcuts
        $(document).on('keydown', function(e) {
            // Ctrl+S to save
            if (e.ctrlKey && e.keyCode === 83) {
                e.preventDefault();
                $('input[type="submit"][name="_save"]').first().click();
                return false;
            }
            
            // Ctrl+Shift+S to save and continue editing
            if (e.ctrlKey && e.shiftKey && e.keyCode === 83) {
                e.preventDefault();
                $('input[type="submit"][name="_continue"]').first().click();
                return false;
            }
            
            // Escape to cancel/go back
            if (e.keyCode === 27) {
                var $cancel = $('.cancel-link, .deletelink').first();
                if ($cancel.length) {
                    window.location.href = $cancel.attr('href');
                }
            }
        });
        
        // Add keyboard shortcut help
        var $helpBtn = $('<button type="button" class="help-button" style="position: fixed; bottom: 20px; right: 20px; background: #17a2b8; color: white; border: none; border-radius: 50%; width: 50px; height: 50px; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">' +
                         '<i class="fas fa-question"></i></button>');
        
        $helpBtn.on('click', function() {
            alert('Keyboard Shortcuts:\n\nCtrl+S: Save\nCtrl+Shift+S: Save and continue editing\nEsc: Cancel/Go back');
        });
        
        $('body').append($helpBtn);
        
        // Progress bars animation
        $('.progress-bar').each(function() {
            var $bar = $(this);
            var width = $bar.data('width') || $bar.css('width');
            
            $bar.css('width', '0%');
            setTimeout(function() {
                $bar.animate({width: width}, 1000);
            }, 500);
        });
        
        // Enhanced action selection
        $('#action-toggle').on('change', function() {
            var checked = $(this).is(':checked');
            $('.action-checkbox').prop('checked', checked);
            
            if (checked) {
                $('.actions').addClass('actions-selected');
            } else {
                $('.actions').removeClass('actions-selected');
            }
        });
        
        $('.action-checkbox').on('change', function() {
            var totalChecked = $('.action-checkbox:checked').length;
            var total = $('.action-checkbox').length;
            
            if (totalChecked > 0) {
                $('.actions').addClass('actions-selected');
                $('#action-toggle').prop('indeterminate', totalChecked < total);
                $('#action-toggle').prop('checked', totalChecked === total);
            } else {
                $('.actions').removeClass('actions-selected');
                $('#action-toggle').prop('indeterminate', false);
                $('#action-toggle').prop('checked', false);
            }
        });
        
    });
    
})(django.jQuery || jQuery);

// Additional utility functions
window.OneCupAdmin = {
    showNotification: function(message, type) {
        type = type || 'info';
        var colors = {
            'success': '#28a745',
            'error': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8'
        };
        
        var $notification = $('<div class="admin-notification" style="position: fixed; top: 20px; right: 20px; background: ' + 
                             (colors[type] || colors.info) + '; color: white; padding: 15px 20px; border-radius: 6px; z-index: 9999; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">' +
                             '<i class="fas fa-info-circle"></i> ' + message + '</div>');
        
        $('body').append($notification);
        
        setTimeout(function() {
            $notification.fadeOut(function() {
                $(this).remove();
            });
        }, 4000);
    },
    
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    
    exportTableAsCSV: function(tableSelector, filename) {
        var csv = [];
        var rows = $(tableSelector + " tr");
        
        for (var i = 0; i < rows.length; i++) {
            var row = [], cols = rows[i].querySelectorAll("td, th");
            
            for (var j = 0; j < cols.length; j++) {
                row.push('"' + cols[j].innerText.replace(/"/g, '""') + '"');
            }
            
            csv.push(row.join(","));
        }
        
        var csvString = csv.join("\n");
        var blob = new Blob([csvString], { type: 'text/csv' });
        var url = window.URL.createObjectURL(blob);
        
        var a = document.createElement('a');
        a.href = url;
        a.download = filename || 'export.csv';
        a.click();
        
        window.URL.revokeObjectURL(url);
    }
};