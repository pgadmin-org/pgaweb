// eslint-disable-next-line no-undef
jQuery(document).ready(function ($) {
  $('#pga-illustration').hover(
    function () {
      $(this).addClass('expand');
    },
    function () {
      $(this).removeClass('expand');
    },
  );
});
