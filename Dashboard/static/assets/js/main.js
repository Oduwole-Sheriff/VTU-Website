/*=== Javascript function indexing hear===========

1.counterUp ----------(Its use for counting number)
2.stickyHeader -------(header class sticky)
3.wowActive ----------( Waw js plugins activation)
4.swiperJs -----------(All swiper in this website hear)
5.salActive ----------(Sal animation for card and all text)
6.textChanger --------(Text flip for banner section)
7.timeLine -----------(History Time line)
8.datePicker ---------(On click date calender)
9.timePicker ---------(On click time picker)
10.timeLineStory -----(History page time line)
11.vedioActivation----(Vedio activation)
12.searchOption ------(search open)
13.cartBarshow -------(Cart sode bar)
14.sideMenu ----------(Open side menu for desktop)
15.Back to top -------(back to top)
16.filterPrice -------(Price filtering)

==================================================*/

(function ($) {
    'use strict';
  
    var rtsJs = {
        m: function (e) {
            rtsJs.d();
            rtsJs.methods();
        },
        d: function (e) {
            this._window = $(window),
            this._document = $(document),
            this._body = $('body'),
            this._html = $('html')
        },
        methods: function (e) {
            rtsJs.sideCollups();
            rtsJs.niceSelect();
            rtsJs.newTab();
            rtsJs.darkLightSwitcher();
            rtsJs.stickySearch();
        },
        
        sideCollups: function () {
            // Toggle classes on button click
            $('#collups-left').on('click', function (e) {
              $('#collups-left').toggleClass('collapsed');
              $('.left-side-bar').toggleClass('collapsed');
              $('.main-center-content-m-left').toggleClass('collapsed');
            });
            // Popup Toggle
            $(".single_action__haeader svg, .avatar").click(function(e) {
                e.preventDefault();
                var $popup = $(this).siblings('.slide-down__click');
            
                $popup.slideToggle();
                $(".slide-down__click").not($popup).slideUp(0);
            });
            // Popup Toggle
            $(".single_action__haeader").click(function(e) {
                $(this).toggleClass('active');
            });

            $(".right-side-open-clouse").click(function(e) {
                $(this).parent().toggleClass('close-right');
                $('.main-center-content-m-left').toggleClass('close-right-sidebar');
            });



        },

        niceSelect: function(){
            $('.nice-select').each(function() {
  
                var select = $(this),
                    name = select.attr('name');
                
                select.hide();
                
                select.wrap('<div class="nice-select-wrap"></div>');
                
                var parent = select.parent('.nice-select-wrap');
                
                parent.append('<ul id=' + name + ' style="display:none"></ul>');
                
                select.find('option').each(function() {
              
                  var option = $(this),
                      value = option.attr('value'),
                      label = option.text();
                  
                  if (option.is(":first-child")) {
                    
                    $('<a href="#" class="drop">' + label + '</a>').insertBefore(parent.find('ul'));
                    
                  } else {
                    
                    parent.find('ul').append('<li><a href="#" id="' + value + '">' + label + '</a></li>');
                    
                  }
                  
                });
                
                parent.find('a').on('click', function(e) {
                  
                  parent.toggleClass('down').find('ul').slideToggle(300);
                  
                  e.preventDefault();
                
                });
                
                parent.find('ul a').on('click', function(e) {
                  
                  var niceOption = $(this),
                          value = niceOption.attr('id'),
                      text = niceOption.text();
                  
                  select.val(value);
                  
                  parent.find('.drop').text(text);
                  
                  e.preventDefault();
                
                });
                
            });
        },

        newTab: function(){
            $(document).ready(function(){
                $('.new-chat-option').on('click', function(){
                    $('.question_answer__wrapper__chatbot').hide(5);
                });
                $('.new-chat-option').on('click', function(){
                    $('.copyright-area-bottom').hide(5);
                });
                $('.chat-history-area-start .single-history').on('click', function(){
                    $('.question_answer__wrapper__chatbot').hide(5).show(5);
                });
                $('.chat-history-area-start .single-history').on('click', function(){
                    $('.copyright-area-bottom').show(5);
                });
            });
        },

        darkLightSwitcher: function(e){
            $(document).ready(function() {

                var toggle = document.getElementById("rts-data-toggle");
                    
                // Check if user has already set a theme preference
                var storedTheme = localStorage.getItem('intellactai');
        
                // If no preference is found, default to dark mode
                if (!storedTheme) {
                    storedTheme = "dark";
                    localStorage.setItem('intellactai', storedTheme);
                }
        
                document.documentElement.setAttribute('data-theme', storedTheme);
                
                toggle.onclick = function() {
                    var currentTheme = document.documentElement.getAttribute("data-theme");
                    var targetTheme = "light";
        
                    if (currentTheme === "light") {
                        targetTheme = "dark";
                    }
                    
                    document.documentElement.setAttribute('data-theme', targetTheme);
                    localStorage.setItem('intellactai', targetTheme);
                };
                
            });
        },

        stickySearch: function (e) {
            $(document).ready(function(){
                $(window).scroll(function(){
                    var distanceFromBottom = $(document).height() - $(window).height() - $(window).scrollTop();
        
                    var threshold = 200; // You can adjust this value according to your requirement
        
                    if(distanceFromBottom < threshold) {
                        $('.chatbot .search-form').addClass('active');
                    } else {
                        $('.chatbot .search-form').removeClass('active');
                    }
                });
            });
 
        },

        
    }

    rtsJs.m();
  })(jQuery, window) 


// JavaScript to handle dynamic cable plan options based on selected network
document.querySelector('.cable_subscription').addEventListener('change', function() {
    var network = this.value;
    var cablePlanSelect = document.querySelector('.cable_plan');
    
    // Clear existing options in the Cable Plan dropdown
    cablePlanSelect.innerHTML = '<option value="" disabled selected>Cable Plan</option>';
    
    // Define the options for each network
    var plans = {
        "1": [ // GOTV
            "GOtv smallie 1 month  = N1575",
            "GOtv Smallie - Monthly  = N1575",
            "GOtv Jin ja Bouquet  = N3300",
            "GOtv Smallie - Quarterly  = N4175",
            "GOtv Jolli  = N4850",
            "GOtv Max  = N7200",
            "GOtv Supa  = N9600",
            "GOtv smallie 1 year  = N12300",
            "GOtv Super Plus  = N13900",
        ],
        "2": [ // DSTV
            "Padi  = N3600",
            "DStv Yanga Bouquet E36  = N5100",
            "DStv Confam Bouquet E36  = N9300",
            "Asian Bouqet  = N12400",
            "DStv Compact  = N15700",
            "DDStv Compact XtraView  + HDPVR/XtraView   = N20700",
            "DStv  Compact Plus  = N25000",
            "DStv Compact Plus XtraView  + HDPVR/XtraView   = N30000",
            "DStv Premium  = N37000",
            "DStv Premium Xtraview  + HDPVR/XtraView   = N42000",
        ],
        "3": [ // STARTIME
            "Nova - 600 Naira - 1 Week  = N600",
            "Basic - 1100 Naira - 1 Week  = N1100",
            "Smart - 1300 Naira - 1 Week  = N1300",
            "Classic - 1,500 Naira - 1 Week  = N1500",
            "Nova - 1,700 Naira - 1 Month  = N1700",
            "Super - 2700 Naira - 1 Week  = N2700",
            "Basic - 3300Naira - 1 Month  = N3300",
            "Smart - 3800 Naira - 1 Month  = N3800",
            "Classic - 5000Naira - 1 Month  = N5000",
            "Super - 8000 Naira - 1 Month  = N8000"
        ]
    };

    // Add new options based on the selected network
    if (plans[network]) {
        plans[network].forEach(function(plan) {
            var option = document.createElement('option');
            option.value = plan;
            option.textContent = plan;
            cablePlanSelect.appendChild(option);
        });
    }
});

