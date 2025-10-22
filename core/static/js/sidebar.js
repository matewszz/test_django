$(".menu-btn").click(function () {
    $(".sidebar").toggleClass("active");
    updateFocusedContentStyle();
  });
  
  $(".menu > ul > li").click(function (e) {
    // remove active from already active
    $(this).siblings().removeClass("active");
    // add active to clicked
    $(this).toggleClass("active");
    // if has sub menu open it
    $(this).find("ul").slideToggle();
    // close other sub menu if any open
    $(this).siblings().find("ul").slideUp();
    // remove active class of sub menu items
    $(this).siblings().find("ul").find("li").removeClass("active");
  
    updateFocusedContentStyle();
  });
  
  $(".menu > ul > li.has-submenu > a").click(function (e) {
    // prevent event from bubbling up to parent li
    e.stopPropagation();
    // remove active from already active
    $(this).parent().siblings().removeClass("active");
    // add active to clicked
    $(this).parent().toggleClass("active");
    // if has sub menu open it
    $(this).parent().find("ul").slideToggle();
    // close other sub menu if any open
    $(this).parent().siblings().find("ul").slideUp();
    // remove active class of sub menu items
    $(this).parent().siblings().find("ul").find("li").removeClass("active");
  
    updateFocusedContentStyle();
  });
  
  function updateFocusedContentStyle() {
    var sidebar = $(".sidebar");
    var focusedContent = $(".focused_content");
    var headername = $(".header_name");
    var headerback = $(".header_back");
    var contenthome = $(".content_home");
    var protocol_options = $(".protocol_options");
    var protocol_options_2 = $(".protocol_options_2");
    var txt_service = $(".txt_service");
  
  
    if (sidebar.hasClass("active")) {
      // Se a barra lateral estiver ativa, define margin-left como 8rem
      focusedContent.css("margin-left", "6rem");
      headername.css("margin-left", "7rem");
      headerback.css("margin-left", "5.75rem");
      contenthome.css("margin-left", "0rem");
      protocol_options.css("width", "21.3rem");
      protocol_options_2.css("margin-left", "11.5rem");
      txt_service.css("background-color", "#f6f6f6");
  
  
    } else {
      // Se a barra lateral não estiver ativa, define margin-left como 16rem
      focusedContent.css("margin-left", "16rem");
      headername.css("margin-left", "17rem");
      headerback.css("margin-left", "16rem");
      contenthome.css("margin-left", "16rem");
      protocol_options.css("width", "19rem");
      protocol_options_2.css("margin-left", "9rem");
      txt_service.css("background-color", "transparent");
  
    }
  }
  
  // JS dashboard
  function updateDisplayStyle() {
    $(".sub-menu-0").click(function () {
        $(".sub-menu-1").toggle();
    });
  
    $(".sub-menu-1").click(function (e) {
        e.stopPropagation();
        $(".sub-menu-1").not(this).next(".sub-menu-2").hide();
        $(this).next(".sub-menu-2").toggle();
        updateArrowsVisibility();
    });
  
    $(".sub-menu-2").click(function (e) {
        e.stopPropagation();
        var allDash = $(this).find(".all_dash");
        $(".all_dash").not(allDash).hide(); // Esconde todos os painéis exceto o relacionado ao serviço clicado
        allDash.toggle(); // Alterna a visibilidade do painel relacionado ao serviço clicado
        updateArrowsVisibility();
    });
  }

  function updateArrowsVisibility() {
      $(".sub-menu-2").each(function () {
          var isVisible = $(this).is(":visible");
          var arrow1 = $(this).prev(".sub-menu-1").find("#arrow_1");
  
          if (isVisible) {
              arrow1.addClass("rotate-180");
          } else {
              arrow1.removeClass("rotate-180");
          }
      });
  }
  
  updateDisplayStyle();