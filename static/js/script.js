/*
Author       : Dreamstechnologies
Template Name: Clockfie - Bootstrap Admin Template
*/

(function () {
    "use strict";

	// Variables declarations
	var $wrapper = $('.main-wrapper');
	var $slimScrolls = $('.slimscroll');
	var $pageWrapper = $('.page-wrapper');

	// Page Content Height Resize
	$(window).resize(function () {
		if ($('.page-wrapper').length > 0) {
			var height = $(window).height();
			$(".page-wrapper").css("min-height", height);
		}
	});

	// Mobile menu sidebar overlay
	$('body').append('<div class="sidebar-overlay"></div>');

	$(document).on('click', '#mobile_btn', function() {
		$wrapper.toggleClass('slide-nav');
		$('.sidebar-overlay').toggleClass('opened');
		$('html').addClass('menu-opened');
		$('#task_window').removeClass('opened');
		return false;
	});

	$(".sidebar-overlay").on("click", function () {
		$('html').removeClass('menu-opened');
		$(this).removeClass('opened');
		$wrapper.removeClass('slide-nav');
		$('.sidebar-overlay').removeClass('opened');
		$('#task_window').removeClass('opened');
	});

	// Logo Hide Btn

	$(document).on("click",".hideset",function () {
		$(this).parent().parent().parent().hide();
	});

	$(document).on("click",".delete-set",function () {
		$(this).parent().parent().hide();
	});

	// Datatable
	if($('.datatable').length > 0) {
		$('.datatable').DataTable({
			"bFilter": true,
			"sDom": 'fBtlpi',  
			"ordering": false,
			"language": {
				search: ' ',
				sLengthMenu: '_MENU_',
				searchPlaceholder: "Search",
				sLengthMenu: 'Row Per Page _MENU_ Entries',
				info: "_START_ - _END_ of _TOTAL_ items",
				paginate: {
					next: '<i class="ti ti-chevron-right"></i>',
					previous: '<i class="ti ti-chevron-left"></i> '
				},
			 },
			"scrollX": true,         // Enable horizontal scrolling
			"scrollCollapse": true,  // Adjust table size when the scroll is used
			"responsive": true,
			"autoWidth": false,
			initComplete: (settings, json)=>{
				$('.dataTables_filter').appendTo('#tableSearch');
				$('.dataTables_filter').appendTo('.search-input');
			},	
		});
	}	

  // Loader	
  $('#loader-wrapper').show();
  setTimeout(function () {
      $("#loader-wrapper").hide();
  }, 300);

	// Datetimepicker
	if($('.datetimepicker').length > 0 ){
		$('.datetimepicker').datetimepicker({
			format: 'DD MMM YYYY',
			icons: {
				up: "fas fa-angle-up",
				down: "fas fa-angle-down",
				next: 'fas fa-angle-right',
				previous: 'fas fa-angle-left'
			}
		});
	}
	
	// toggle-password
	if($('.toggle-password').length > 0) {
		$(document).on('click', '.toggle-password', function() {
			$(this).toggleClass("ti-eye ti-eye-off");
			var input = $(".pass-input");
			if (input.attr("type") == "password") {
				input.attr("type", "text");
			} else {
				input.attr("type", "password");
			}
		});
	}
	if($('.toggle-passwords').length > 0) {
		$(document).on('click', '.toggle-passwords', function() {
			$(this).toggleClass("ti-eye ti-eye-off");
			var input = $(".pass-inputs");
			if (input.attr("type") == "password") {
				input.attr("type", "text");
			} else {
				input.attr("type", "password");
			}
		});
	}
	if($('.toggle-passworda').length > 0) {
		$(document).on('click', '.toggle-passworda', function() {
			$(this).toggleClass("ti-eye ti-eye-off");
			var input = $(".pass-inputa");
			if (input.attr("type") == "password") {
				input.attr("type", "text");
			} else {setTimeout
				input.attr("type", "password");
			}
		});
	}

	// Select 2	
	if ($('.select2').length > 0) {
	 	$(".select2").select2();
	}
	
	if ($('.select').length > 0) {
		$('.select').select2({
			minimumResultsForSearch: -1,
			width: '100%'
		});
	}

	// Select Image

	if ($('.select-img').length > 0) {
		function formatState (state) {
		  if (!state.id) { return state.text; }
		  var $state = $(
			'<span><img src="' + $(state.element).attr('data-image') + '" class="img-flag" / " width="16px"> ' + state.text + '</span>'
		  );
		  return $state;
		};
		$('.select-img').select2({
			minimumResultsForSearch: Infinity,
			  templateResult: formatState,
			  templateSelection: formatState
		});
	}

	// Sidebar Slimscroll
	if($slimScrolls.length > 0) {
		$slimScrolls.slimScroll({
			height: 'auto',
			width: '100%',
			position: 'right',
			size: '7px',
			color: '#ccc',
			wheelStep: 10,
			touchScrollStep: 100
		});
		var wHeight = $(window).height() - 60;
		$slimScrolls.height(wHeight);
		$('.sidebar .slimScrollDiv').height(wHeight);
		$(window).resize(function() {
			var rHeight = $(window).height() - 60;
			$slimScrolls.height(rHeight);
			$('.sidebar .slimScrollDiv').height(rHeight);
		});
	}

	// Sidebar
	var Sidemenu = function() {
		this.$menuItem = $('.sidebar-menu a');
	};

	function init() {
		var $this = Sidemenu;
		$('.sidebar-menu a').on('click', function(e) {
			if($(this).parent().hasClass('submenu')) {
				e.preventDefault();
			}
			if(!$(this).hasClass('subdrop')) {
				$('ul', $(this).parents('ul:first')).slideUp(250);
				$('a', $(this).parents('ul:first')).removeClass('subdrop');
				$(this).next('ul').slideDown(350);
				$(this).addClass('subdrop');
			} else if($(this).hasClass('subdrop')) {
				$(this).removeClass('subdrop');
				$(this).next('ul').slideUp(350);
			}
		});
		$('.sidebar-menu ul li.submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
	}

	
	// Sidebar Initiate
	init();
	$(document).on('mouseover', function(e) {
        e.stopPropagation();
        if ($('body').hasClass('mini-sidebar') && $('#toggle_btn').is(':visible')) {
            var targ = $(e.target).closest('.sidebar, .header-left, #toggle_btn').length;
            if (targ) {
                $('body').addClass('expand-menu');
                $('.subdrop + ul').slideDown();
            } else {
                $('body').removeClass('expand-menu');
                $('.subdrop + ul').slideUp();
            }
            return false;
        }
    });

	// Sidebar
	var Colsidemenu = function() {
		this.$menuItems = $('.sidebar-right a');
	};

	function colinit() {
		var $this = Colsidemenu;
		$('.sidebar-right ul a').on('click', function(e) {
			if($(this).parent().hasClass('submenu')) {
				e.preventDefault();
			}
			if(!$(this).hasClass('subdrop')) {
				$('ul', $(this).parents('ul:first')).slideUp(250);
				$('a', $(this).parents('ul:first')).removeClass('subdrop');
				$(this).next('ul').slideDown(350);
				$(this).addClass('subdrop');
			} else if($(this).hasClass('subdrop')) {
				$(this).removeClass('subdrop');
				$(this).next('ul').slideUp(350);
			}
		});
		$('.sidebar-right ul li.submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
	}
	colinit();
	
	// Date Range Picker
	if($('#reportrange').length > 0) {
		var start = moment().subtract(29, "days"),
			end = moment();

		function report_range(start, end) {
			$("#reportrange span").html(start.format("D MMM YY") + " - " + end.format("D MMM YY"))
		}
		$("#reportrange").daterangepicker({
			startDate: start,
			endDate: end,
			ranges: {
				'Today': [moment(), moment()],
				'Yesterday': [moment().subtract(1, "days"), moment().subtract(1, "days")],
				"Last 7 Days": [moment().subtract(6, "days"), moment()],
				"Last 30 Days": [moment().subtract(29, "days"), moment()],
				"This Month": [moment().startOf("month"), moment().endOf("month")],
				"Last Month": [moment().subtract(1, "month").startOf("month"), moment().subtract(1, "month").endOf("month")]
			}
		}, report_range), report_range(end, end);
	}

	if($('.bookingrange').length > 0) {
		var start = moment().subtract(6, 'days');
		var end = moment();
		function booking_range(start, end) {
			$('.bookingrange span').html(start.format('D MMM YY') + ' - ' + end.format('D MMM YY'));
		}

		$('.bookingrange').daterangepicker({
			startDate: start,
			endDate: end,
			ranges: {
				'Today': [moment(), moment()],
				'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
				'Last 7 Days': [moment().subtract(6, 'days'), moment()],
				'Last 30 Days': [moment().subtract(29, 'days'), moment()],
				'This Year': [moment().startOf('year'), moment().endOf('year')],
				'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
			}
		}, booking_range);
		booking_range(start, end);
	}

	
	if($('.daterange').length > 0) {
		$('.daterange').daterangepicker({
			autoUpdateInput: false,  // Prevents immediate update of input field
			ranges: {
				'Today': [moment(), moment()],
				'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
				'Last 7 Days': [moment().subtract(6, 'days'), moment()],
				'Last 30 Days': [moment().subtract(29, 'days'), moment()],
				'This Year': [moment().startOf('year'), moment().endOf('year')],
				'Next Year': [moment().add(1, 'year').startOf('year'), moment().add(1, 'year').endOf('year')]
			},
			locale: {
				cancelLabel: 'Clear'
			}
		});
		$('#daterange').on('input', function() {
			var textLength = $(this).val().length;
			$(this).css('width', (textLength + 10) + 'px'); // 10ch adds space for padding
		});
	
		// Event when the user selects a date
		$('.daterange').on('apply.daterangepicker', function(ev, picker) {
			$(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
		});
	
		// Event for clearing the selected date
		$('.daterange').on('cancel.daterangepicker', function(ev, picker) {
			$(this).val('');  // Resets to placeholder
		});
	}

	//toggle_btn
	$(document).on('click', '#toggle_btn', function() {
		if ($('body').hasClass('mini-sidebar')) {
			$('body').removeClass('mini-sidebar');
			$(this).addClass('active');
			$('.subdrop + ul');
			localStorage.setItem('screenModeNightTokenState', 'night');
			setTimeout(function() {
				$("body").removeClass("mini-sidebar");
				$(".header-left").addClass("active");
			}, 100);
		} else {
			$('body').addClass('mini-sidebar');
			$(this).removeClass('active');
			$('.subdrop + ul');
			localStorage.removeItem('screenModeNightTokenState', 'night');
			setTimeout(function() {
				$("body").addClass("mini-sidebar");
				$(".header-left").removeClass("active");
			}, 100);
		}
		return false;
	});

	var myDiv = document.querySelector('.sticky-sidebar-one');	

	$('.themecolorset').on('click', function(){
		$('.themecolorset').removeClass('active');
		$(this).addClass('active');
	});

	$('.theme-layout').on('click', function(){
		$('.theme-layout').removeClass('active');
		$(this).addClass('active');
	});


	if($('.win-maximize').length > 0) {
		$('.win-maximize').on('click', function(e){
			if (!document.fullscreenElement) {
				document.documentElement.requestFullscreen();
			} else {
				if (document.exitFullscreen) {
					document.exitFullscreen();
				}
			}
		})
	}

		// Custom Country Code Selector

		if ($('#phone').length > 0) {
			var input = document.querySelector("#phone");
			window.intlTelInput(input, {
				utilsScript: "assets/plugins/intltelinput/js/utils.js",
			});
		}

		// Custom Country Code Selector

		if ($('#phone2').length > 0) {
			var input = document.querySelector("#phone2");
			window.intlTelInput(input, {
				utilsScript: "assets/plugins/intltelinput/js/utils.js",
			});
		}

		if ($('#phone3').length > 0) {
			var input = document.querySelector("#phone3");
			window.intlTelInput(input, {
				utilsScript: "assets/plugins/intltelinput/js/utils.js",
			});
		}	

	// select all 2
	$(document).on('click', '#check_all', function() {
		$('.checkmail').click();
		return false;
	});
	var selectAllItems = "#select-all2";
	var checkboxItem = ".form-check.form-check-md :checkbox";
	$(selectAllItems).on('click', function(){
		
		if (this.checked) {
		$(checkboxItem).each(function() {
			this.checked = true;
		});
		} else {
		$(checkboxItem).each(function() {
			this.checked = false;
		});
		}
		
	});

	// select all 3
	$(document).on('click', '#check_all', function() {
		$('.checkmail').click();
		return false;
	});
	var selectAllItems = "#select-all3";
	var checkboxItem = ".form-check.form-check-md :checkbox";
	$(selectAllItems).on('click', function(){
		
		if (this.checked) {
		$(checkboxItem).each(function() {
			this.checked = true;
		});
		} else {
		$(checkboxItem).each(function() {
			this.checked = false;
		});
		}
		
	});
		
	// Tooltip
	if($('[data-bs-toggle="tooltip"]').length > 0) {
		var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
		var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
			return new bootstrap.Tooltip(tooltipTriggerEl)
		})
	}
	
	if(window.location.hash == "#LightMode"){
		localStorage.setItem('theme', 'dark');
	}
	else {
		if(window.location.hash == "#DarkMode"){
			localStorage.setItem('theme', 'light');
		}
	}

	
	$('ul.tabs li').on('click', function(){
		var $this = $(this);
		var $theTab = $(this).attr('id');
		console.log($theTab);
		if($this.hasClass('active')){
		  // do nothing
		} else{
		  $this.closest('.tabs_wrapper').find('ul.tabs li, .tabs_container .tab_content').removeClass('active');
		  $('.tabs_container .tab_content[data-tab="'+$theTab+'"], ul.tabs li[id="'+$theTab+'"]').addClass('active');
		}
		
	});

	// Date Range Picker
	if ($('input[name="datetimes"]').length > 0) {
		$('input[name="datetimes"]').daterangepicker({
		timePicker: true,
		startDate: moment().startOf('hour'),
		endDate: moment().startOf('hour').add(32, 'hour'),
		locale: {
		format: 'M/DD hh:mm A'
		}
	});
	}

	if($('.custom-input').length > 0) {
		const inputRange = document.querySelector('.custom-input');

		inputRange.addEventListener('input', function () {
			const progress = (inputRange.value - inputRange.min) / (inputRange.max - inputRange.min) * 100;
			inputRange.style.background = `linear-gradient(to top, var(--md-sys-color-on-surface-variant) 0%, var(--md-sys-color-on-surface-variant) ${progress}%, var(--md-sys-color-surface-variant) ${progress}%, var(--md-sys-color-surface-variant) 100%)`;
		});
	}

	// Datetimepicker time

	if ($('.timepicker').length > 0) {
		$('.timepicker').datetimepicker({
			format: 'HH:mm A',
			icons: {
				up: "fas fa-angle-up",
				down: "fas fa-angle-down",
				next: 'fas fa-angle-right',
				previous: 'fas fa-angle-left'
			}
		});
	}

	// hide show
	if ($('.hours-rate-btn').length > 0) {
	$(".hours-rate-btn").on("click", function() {
		$(".hours-rate-main").addClass("hours-rate-main-show");
	});
	$(".hours-rate-btn").on("click", function() {
		$(".hours-rate-btn").addClass("hours-rate-btn-close");
	});
	$(".reset-promote").on("click", function() {
		$(".hours-rate-main").removeClass("hours-rate-main-show");
	});
    }

	// month picker
	if ($('.month-picker').length > 0) {
	document.getElementById('monthly').value = '2025-01';
	document.getElementById('monthly2').value = '2025-12';
	}
	
	// Collapse Header
	if($('.btnFullscreen').length > 0) {
		const btnFullscreenElements = document.getElementsByClassName('btnFullscreen');

		// Add an event listener to each element
		Array.from(btnFullscreenElements).forEach(element => {
			element.addEventListener('click', function() {
				toggleFullscreen();
			});
		});

		// Function to toggle fullscreen mode
		function toggleFullscreen() {
			if (!document.fullscreenElement) {
				document.documentElement.requestFullscreen();
			} else {
				if (document.exitFullscreen) {
					document.exitFullscreen();
				}
			}
		}
	} 

	if($('#collapse-header').length > 0) {
		document.getElementById('collapse-header').onclick = function() {
		    this.classList.toggle('active');
		    document.body.classList.toggle('header-collapse');
		}
	}

	if($('.kanban-drag-wrap').length > 0) {
        $(".kanban-drag-wrap").sortable({
            connectWith: ".kanban-drag-wrap",
            handle: ".kanban-card",
            placeholder: "drag-placeholder"
        });
    }

	// Increment Decrement

	$(".inc").on('click', function() {
	    updateValue(this, 1);
	});
	$(".dec").on('click', function() {
	    updateValue(this, -1);
	});
	function updateValue(obj, delta) {
	    var item = $(obj).parent().find("input");
	    var newValue = parseInt(item.val(), 10) + delta;
	    item.val(Math.max(newValue, 0));
	}

	// card with fullscreen 
	let DIV_CARD = ".card";
	let cardFullscreenBtn = document.querySelectorAll(
		'[data-bs-toggle="card-fullscreen"]'
	  );
	  cardFullscreenBtn.forEach((ele) => {
		ele.addEventListener("click", function (e) {
		  let $this = this;
		  let card = $this.closest(DIV_CARD);
		  card.classList.toggle("card-fullscreen");
		  card.classList.remove("card-collapsed");
		  e.preventDefault();
		  return false;
		});
	});	

	// card with close button 
	let DIV_CARD_CLOSE = ".card";
	let cardRemoveBtn = document.querySelectorAll(
		'[data-bs-toggle="card-remove"]'
	);
	cardRemoveBtn.forEach((ele) => {
		ele.addEventListener("click", function (e) {
		e.preventDefault();
		let $this = this;
		let card = $this.closest(DIV_CARD_CLOSE);
		card.remove();
		return false;
		});
	});

	setTimeout(function(){
		$(".rating-select").on('click', function() {
			$(this).find("i").toggleClass("ti-star ti-star-filled filled");
		});
	},100);

	// Datetimepicker

	if($('.yearpicker').length > 0 ){
		$('.yearpicker').datetimepicker({
			viewMode: 'years',
			format: 'YYYY',

			icons: {
				up: "fas fa-angle-up",
				down: "fas fa-angle-down",
				next: 'fas fa-angle-right',
				previous: 'fas fa-angle-left'
			}
		});
	}

	// Upload Image 

	$('.image-sign').on('change', function(){
		$(this).closest('.upload-pic').find(".frames").html('');
		for (var i = 0; i < $(this)[0].files.length; i++) {
			$(this).closest('.upload-pic').find(".frames").append('<img src="'+window.URL.createObjectURL(this.files[i])+'" width="100px" height="100px">');
		}
	});

	// Datetimepicker
	if($('.datepic').length > 0 ){
		$('.datepic').datetimepicker({
			format: 'DD-MM-YYYY',
			keepOpen: true,inline: true,
			icons: {
				up: "fas fa-angle-up",
				down: "fas fa-angle-down",
				next: 'fas fa-angle-right',
				previous: 'fas fa-angle-left'
			}
		});
	}

	if($('.stack-menu').length > 0) {
		var activeTab = null;
		$('.stack-menu .nav a').on('click', function(e) {
			e.preventDefault();
			var currentTab = $(this).attr('href');

			if (activeTab === currentTab) {
				if ($(currentTab).is(':visible')) {
					$(currentTab).hide(); 
					activeTab = null;
				} else {
					$(currentTab).show(); 
					activeTab = currentTab;
				}
			} else {
				$('#myTabContent .tab-pane').hide(); 
				$(currentTab).show(); 
				activeTab = currentTab;
			}
		});
	}

	var selectAllItems = "#select-all";
	var checkboxItem = ".form-check.form-check-md :checkbox";
	$(selectAllItems).on('click', function(){	
		if (this.checked) {
		$(checkboxItem).each(function() {
			this.checked = true;
		});
		} else {
		$(checkboxItem).each(function() {
			this.checked = false;
		});
		}
		
	});

	function toggleFullscreen(elem) {
		elem = elem || document.documentElement;
		if (!document.fullscreenElement && !document.mozFullScreenElement &&
		!document.webkitFullscreenElement && !document.msFullscreenElement) {
		if (elem.requestFullscreen) {
			elem.requestFullscreen();
		} else if (elem.msRequestFullscreen) {
			elem.msRequestFullscreen();
		} else if (elem.mozRequestFullScreen) {
			elem.mozRequestFullScreen();
		} else if (elem.webkitRequestFullscreen) {
			elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
		}
		} else {
		if (document.exitFullscreen) {
			document.exitFullscreen();
		} else if (document.msExitFullscreen) {
			document.msExitFullscreen();
		} else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		} else if (document.webkitExitFullscreen) {
			document.webkitExitFullscreen();
		}
		}
	}

	if($('.switch-coder').length > 0) {
		$(".switch-coder").on("change", function () {
			var $card = $(this).closest(".card");
			var $viewPreview = $card.find(".view-preview");
			var $viewCode = $card.find(".view-code");	
			if ($(this).prop("checked")) {
				$viewPreview.addClass("d-none");
				$viewCode.removeClass("d-none");
			} else {
				$viewPreview.removeClass("d-none");
				$viewCode.addClass("d-none");
			}
		});
	}

	// Play & Pause Icon

	if($('.play-icon').length > 0) {
		$(".play-icon").on("click", function () {
			$(this).toggleClass("pause"); 
			$(this).find("i").toggleClass("ti-player-play-filled ti-player-stop-filled");
		});
	}

	// fancy box
	if($('.screenshot-item').length > 0) {
		$( '[data-fancybox="gallery"]' ).fancybox({
			infobar : false,
			buttons: [
				"close"
			],
			caption : function( instance, item ) {
				var caption = $(this).data('caption') || '';
		
				return `
					${caption.length ? caption + '<br />' : ''}
						  <div class="screenshot-info-top">
				<div class="d-flex align-items-center justify-content-center">				
					<a href="employee-details.html" class="avatar avatar-sm me-2 flex-shrink-0 avatar-rounded">
						<img src="assets/img/users/user-04.jpg" class="img-fluid" alt="img">
					</a>
					<span class="text-white">Ashley Regan -  24 Jan 2025, 09:01:00 AM</span>							
				</div>
			 </div>
			<div class="screenshot-info-bottom text-center">
				<div class="d-flex align-items-center mb-3 gap-3 justify-content-center flex-wrap">
					<div>
						<span class="text-white">Doccure Team</span>
						<i class="ti ti-point-filled text-primary mx-2"></i>
						<i class="ti ti-activity-heartbeat text-success me-2"></i>
						<span class="text-white">73% of 03 Min</span>
						<i class="ti ti-point-filled text-primary mx-2"></i>
						<span class="text-white">Doccure V1.0</span>
					</div>
					<div class="download-delete-icon ms-2">
						<a href="javascript:void(0);" class="download-icon border bg-white roundeed-circle text-orange p-1 d-inline-flex justify-content-center align-items-center rounded-circle"><i class="ti ti-download fs-13"></i></a>
						<a href="javascript:void(0);" class="delete-icon bg-white border p-1 d-inline-flex justify-content-center align-items-center rounded-circle"><i class="ti ti-trash fs-13"></i></a>
					</div>
				</div>
			   <div class="row justify-content-center">
				<div class="col-md-6">
					<div class="row row-gap-3">
						<div class="col-sm-6">
							<div>
								<div class="d-flex justify-content-between mb-1 text-white">
									<div>
										<i class="ti ti-keyboard me-1"></i>
										<span>Keystroke / Min</span>
									</div>
									<span>69</span>
								</div>									
								<div class="progress-stacked progress-xs w-100">
									<div class="progress-bar bg-success" role="progressbar" style="width: 60%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
								</div>
							</div>
						</div>
						<div class="col-sm-6">
							<div>
								<div class="d-flex justify-content-between mb-1 text-white">
									<div>
										<i class="ti ti-mouse me-1"></i>
										<span>Mouse Moments / Min</span>
									</div>
									<span>169</span>
								</div>									
								<div class="progress-stacked progress-xs w-100">
									<div class="progress-bar bg-success" role="progressbar" style="width: 80%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
								</div>
							</div>
						</div>				
						</div>
				</div>
			   </div>
			 </div>
				`;
			}
		});
	}

	document.addEventListener("DOMContentLoaded", function () {
		if (document.querySelector('.filter-dropdown')) {
			const closeBtn = document.getElementById("close-filter");
			const filterDropdown = document.getElementById("filter-dropdown");
	
			if (closeBtn && filterDropdown) {
				closeBtn.addEventListener("click", function () {
					filterDropdown.classList.remove("show");
				});
			}
		}
	});	

	//Trial Item
	if($('.trial-item').length > 0) {
		$(".trial-item .close-icon").on("click", function () {
			$(this).closest(".trial-item").hide(); 
		});
	}
	
	// Aprrearence Settings 
	$('.theme-image').on('click', function(){
		$('.theme-image').removeClass('active');
		$(this).addClass('active');
	});

	// Add More rows 
	document.addEventListener('DOMContentLoaded', () => {
		const tableBody = document.querySelector('#item-table tbody');
		const addButton = document.getElementById('add-item-btn');

		if (tableBody && addButton) {
			// Add more rows
			addButton.addEventListener('click', () => {
				const newRow = `
				<tr>
					<td><input type="text" class="form-control"></td>
					<td><input type="number" class="form-control" placeholder="Qty"></td>
					<td><input type="text" class="form-control"></td>
					<td>
						<div class="input-group">
							<input type="text" class="form-control">
							<span class="input-group-text">
								<i class="ti ti-currency-dollar"></i>
							</span>
						</div>
					</td>
					<td>
						<div class="input-group">
							<input type="text" class="form-control">
							<span class="input-group-text">
								<i class="ti ti-percentage"></i>
							</span>
						</div>
					</td>
					<td><input type="text" class="form-control"></td>
					<td class="ps-0">
						<select class="form-select form-select-sm">
							<option value="1">%</option>
							<option value="2">$</option>
						</select>
					</td>
					<td class="text-gray-9 fw-14 fw-medium">$0.00</td>
					<td><a href="javascript:void(0);" class="delete-row link-danger"><i class="ti ti-trash"></i></a></td>
				</tr>`;

				tableBody.insertAdjacentHTML('beforeend', newRow);
			});

			// Remove row on trash icon click
			document.addEventListener('click', (e) => {
				if (e.target.closest('.delete-row')) {
					e.target.closest('tr').remove();
				}
			});
		}
	});

	// create project 
	document.addEventListener('DOMContentLoaded', () => {
		const intervalSelect = document.getElementById('interval-select');
		const monthlyFields = document.getElementById('monthly-fields');
		const weeklyFields = document.getElementById('weekly-fields');
	
		// Only run the script if the elements are present
		if (intervalSelect && monthlyFields && weeklyFields) {
			intervalSelect.addEventListener('change', function () {
				if (this.value === 'monthly') {
					monthlyFields.classList.remove('d-none');
					weeklyFields.classList.add('d-none');
				} else {
					monthlyFields.classList.add('d-none');
					weeklyFields.classList.remove('d-none');
				}
			});
		}
	});

	// Quill Editor

	if($('.quill-editor').length > 0) {
		document.querySelectorAll('.quill-editor').forEach((editor) => {
			new Quill(editor, {
			  theme: 'snow'
			});
		});
	}	
	
})();