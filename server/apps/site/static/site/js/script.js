$(document).ready(function(){
        $('.tab-label').click(function(){
            $(this).next().slideToggle(150);
            $(this).next().next().slideToggle(150);
            $(this).find('i').toggleClass('bi bi-chevron-right').toggleClass('bi bi-chevron-down');

        })
    })
