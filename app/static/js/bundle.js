$(function() {
  // Set the command-line prompt
  $('.prompt').html('tniah@shanks:~$');

  // Initialize a new terminal object
  var term = new Terminal('#container .banner', '#input-line .cmdline', '#container output');
  term.init();
});
