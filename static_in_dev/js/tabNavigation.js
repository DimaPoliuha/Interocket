$('.tabgroup > div').hide();
$('.tabgroup > div:first-of-type').show();
$('.menu-navigation-container a').click(function(e){
  e.preventDefault();
    var $this = $(this),
        tabgroup = '#' + $this.parents('.menu-navigation-container').data('tabgroup'),
        others = $this.closest('li').siblings().children('a'),
        target = $this.attr('href');
    others.removeClass('active-tab');
    $this.addClass('active-tab');
    $(tabgroup).children('div').hide();
    $(target).show();
})