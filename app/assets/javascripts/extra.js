$("#solve").click(function(){
  var genome = $('textarea').val().toLowerCase();
  var applyChunks = function(el) {
    curChunks = _.first(_.rest(this.chunks, el), 4);
    $('#chunks-container').append('<div class="w-row bracket-row" id="row'+Math.floor(el/4)+'">');
    _.each(curChunks, _.bind(function() {
      var html = '<div class="w-col w-col-3"><div class="dna-bracket" data-ix="files-trigger">'+arguments[0]+'</div></div>';
      $('#row'+Math.floor(this.idx/4)).append(html);
    }, {idx: el}));
  };
  $.ajax(
    {
      type: 'post',
      url: 'http://162.243.29.17/service',
      data: {genome: genome},
      complete: function(resp) {
        var data = resp.responseJSON;
        var res = data.results;
        window.sequence = data.sequence;
        window.res = res;
        var chunks = _.keys(res);
        var boundApplyChunks = _.bind(applyChunks, {chunks: chunks});
        $('#chunks-container').empty();
        _.each(_.range(0, chunks.length, 4), boundApplyChunks);
        $('.dna-bracket').click(function(event) {
          var key = $(event.target).text();
          var files = window.res[key];
          var indices = key.slice(1,-1).split(',');
          $('#left-idx').text(indices[0]);
          $('#right-idx').text(indices[1]);
          $('#sequence').text(window.sequence.slice(parseInt(indices[0], 10), parseInt(indices[1], 10)).toUpperCase());
          $('#file-list').empty();
          $('#file-list').append('<div>This strand can be found in:</div>');
          _.each(files, function(item) {
            $('#file-list').append('<div class="file-name">'+item+'</div>');
          });
        });
      }
    });
});
$( document ).ajaxStop(function() {
  //$('#myModal').modal('hide');
  $('#email-form').show();
  $('.w-form-done.success-message').hide();
  $('#search').click();
  $('#files-container').click();
});
$( document ).ready(function() {
  setTimeout(function() {$('#search').click();}, 4000);
});
