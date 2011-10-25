function init_contact()
{
  doKetchup(null);
}

function init_ficha()
{
  doKetchup(null);
}

function init_search()
{
  $('#prop_operation_id').change( function(e) {
    var hide = $('#prop_operation_id').val() != 0;
    $('#cosas').toggle(hide);
    
    if( !hide )
    {
      $('#price_min').val('');
      $('#price_max').val('');
    }
    
    $('form#filter').submit();
  });

  $('#prop_type, #currency, #rooms, #area_indoor').change( function(e) {
    $('form#filter').submit();
  });
  
  $('#fake_sort').change( function(e) {
    $('#sort').val( $('#fake_sort').val() );
    $('form#filter').submit();
  });
  
  $('#apply').click( function(e) {
    $('form#filter').submit();
  });
}