// search bar

(function($) {

    $.fn.searchBox = function(ev) {
        var $searchEl = $('.search-elem');
        var $placeHolder = $('.placeholder');
        var $sField = $('#search-field');
        var moveText = function() {
            $placeHolder.addClass('move-up').html('searching...');
        }

        $sField.keydown(moveText);
        $placeHolder.on('click', moveText);

        if (ev === "open") {
            $searchEl.addClass('search-open')
            $sField.focus();
        };

        if (ev === 'close-btn') {
            $searchEl.removeClass('search-open'),
                $placeHolder.removeClass('move-up').html('Type something...'),
                $sField.val('');
        };

        $('.submit').prop('disabled', true);
        $('#search-field').keyup(function() {
            if ($(this).val() != '') {
                $('.submit').prop('disabled', false);
            }
        });
    }

}(jQuery));

$('.search-btn').on('click', function(e) {
    $(this).searchBox('open');
    e.preventDefault();
});

$('.close-btn').on('click', function() {
    $(this).searchBox('close-btn');
});
// 
$(document).ready(function(e) {
    $('.select_menu_con').each(function() {
        var $dropdown = $(this);

        $dropdown.find('.select_value').click(function(e) {
            $dropdown.find('.select_menu').slideToggle('slow');
        });

        $dropdown.find('.select_menu li').click(function(e) {
            $dropdown.find('.select_value').html($(this).html());
            $dropdown.find('.select_menu').slideToggle('slow');
        });
    });
});

var swiperOptions = {
    loop: true,

    // autoplay: {
    //     delay: 1,
    //     disableOnInteraction: true
    // },
    autoplay: true,
    slidesPerView: 'auto',
    slidesPerView: 3,
    speed: 2000,
    // grabCursor: true,
    // mousewheel: {
    //     enabled: true,
    // },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    },
    breakpoints: {
        0: {
            slidesPerView: 1
        },
        576: {
            slidesPerView: 2
        },
        992: {
            slidesPerView: 3
        },
    },
};

var swiper = new Swiper('.swiper-container', swiperOptions);