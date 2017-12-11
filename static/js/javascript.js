$(document).ready(function() {
  $(".flagged").click(function () {
    console.log($(this).attr('song_id'))
    var song_id = $(this).attr('song_id');
    $.ajax({
      url: '/ajax/flag_song/',
      data: {
        'song_id': song_id
      },
      dataType: 'json',
      success: function (data) {
        if (data.exists == 1) {
          alert("test error ");
        }
      }

    })
  });



});
