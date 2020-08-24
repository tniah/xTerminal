$(function() {
  // Sets the banner
  $('#container .banner').html(
  '<img align="left" src="static/logo.png" width="100" height="100" style="padding: 0px 10px 20px 0px">' +
  '<h2 style="letter-spacing: 4px">Web Terminal</h2><p>' + new Date() + '</p>' +
  '<p>Enter "help" for more information.</p>');

  // Sets the command-line prompt
  $('#input-line .prompt').html('tniah@shanks:~$');

  var cmdline_ = $('#input-line .cmdline');
  var output_ = $('#container output');

  var history_ = [];
  var historyPos_ = 0;
  var historyTemp_ = 0;

  $(window).on('click', function(e) {
    cmdline_.focus();
  });

  cmdline_.on('click', function() {
    this.value = this.value;
  });

  cmdline_.on('keydown', function(e) {
    if (history_.length) {
      if (e.keyCode == 38 || e.keyCode == 40) {
        if (history_[historyPos_]) {
          history_[historyPos_] = this.value;
        } else {
          historyTemp_ = this.value;
        }
      }

      if (e.keyCode == 38) {  // up
        historyPos_--;
        if (historyPos_ <0) {
          historyPos_ = 0;
        }
      } else if (e.keyCode == 40) { // down
        historyPos_++;
        if (historyPos_ > history_.length) {
          historyPos_ = history_.length;
        }
      }

      if (e.keyCode ==38 || e.keyCode == 40) {
        this.value = history_[historyPos_] ? history_[historyPos_] : historyTemp_;
        this.value = this.value;  // Sets cursor to end of input.
      }
    }
  });

  cmdline_.on('keydown', function(e) {
    if (e.keyCode == 9) { // tab
      e.preventDefault();
    } else if (e.keyCode == 13) { // enter
      // Save shell history
      if (this.value) {
        history_[history_.length] = this.value;
        historyPos_ = history_.length;
      }

      // Duplicate current input and append to output section.
      var line = $(this).parent().parent().clone();
      line.removeAttr('id');
      line.addClass('line');
      var input = line.find('input.cmdline');
      input.autofocus = false;
      input.readOnly = true;
      output_.append(line);

      if (this.value && this.value.trim()) {
        var args = this.value.split(' ').filter(function(val, i) {
          return val;
        });
        var cmd = args[0].toLowerCase();
        args = args.splice(1);  // Remove cmd from arg list.
      }

      switch(cmd) {
        case 'clear':
          output_.html('');
          this.value = '';
          return;
        default:
          if (cmd) {
            console.log(cmd);
          }
      }
      $(window).scrollTop(getDocHeight_());
      this.value = ''; // Setup line for next input.
    }
  });

  function getDocHeight_() {
    return Math.max(
        Math.max($('body')[0].scrollHeight, $('html')[0].scrollHeight),
        Math.max($('body')[0].offsetHeight, $('html')[0].offsetHeight),
        Math.max($('body')[0].clientHeight, $('html')[0].clientHeight)
    );
  }
});
