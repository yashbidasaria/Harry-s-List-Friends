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
          alert("The song is already flagged");
        }
      }

    })
  });

  $(".rater").click(function () {
    console.log($(this).attr('song_id'))
    //console.log($(this).attr(''))
    var v = $(this).parent().children(0).val()//.attr('value')
    console.log(v)
    var song_id = $(this).attr('song_id');
    $.ajax({
      url: '/ajax/rate_song/',
      data: {
        'rating': v,
        'song_id': song_id
      },
      dataType: 'json',
      success: function (data) {
        if (data.exists == 1) {
            alert("You have already rated the song")
        }
      }

    })
  });

});
