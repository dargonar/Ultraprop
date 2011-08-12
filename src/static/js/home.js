var geocoder              = new google.maps.Geocoder();

jQuery(document).ready(function(){
  
  // jQuery('[jqtransform|=true]').jqTransform(); // en _base.html.
  
  jQuery("#price_slider").slider({
    orientation: 'horizontal', min: default_slider_min, max: default_slider_max, range: true, step: default_slider_step, values: [default_slider_min, default_slider_max], 
    slide: function(event, ui) { 
        formatRangePriceText('price_display'
                              , getPriceValue(ui.values[0])
                              , getPriceValue(ui.values[1])
                              , 'ars'
                              ,jQuery( "#price_slider" ).slider( "option", "max") );
      },
    change: function(event, ui) {
      formatRangePriceText('price_display'
                            , getPriceValue(ui.values[0])
                            , getPriceValue(ui.values[1])
                            , 'ars'
                            ,jQuery( "#price_slider" ).slider( "option", "max") );
    }
  });
  formatRangePriceText('price_display'
                      , getPriceValue(jQuery("#price_slider").slider( "option", "values" )[0])
                      , getPriceValue(jQuery("#price_slider").slider( "option", "values" )[1])
                      , 'ars'
                      ,jQuery( "#price_slider" ).slider( "option", "max") );
  
  jQuery("#searchmap").autocomplete({
    source: function(request, response) {
      geocoder.geocode( {'address': request.term, 'region' : 'ar'}, function(results, status) {
        response(jQuery.map(results, function(item) {
            //Solo direcciones de argentina
            if( !is_from_country(item,'Argentina') )
              return null;

            return {
                  label: item.formatted_address,
                  value: item.formatted_address,
                  result: item
            };
        }));
      })
    },
    select: function(event, ui) {
      jQuery('#center_lat').val(ui.item.result.geometry.location.lat());
      jQuery('#center_lon').val(ui.item.result.geometry.location.lng());
    }
  }); 
  
  $('#prop_operation_id_container input[type="radio"]').change(function(){
    if ($(this).attr('id') == 'prop_operation_id2' && $(this).is(':checked'))
    {
      $('#prop_operation_id').val(OPER_RENT);
      setPriceSliderOptions('price_slider', default_slider_max2, default_slider_step2, default_slider_min2, default_slider_max2);
    }
    else 
    if ($(this).attr('id') == 'prop_operation_id1' && $(this).is(':checked'))
    {
      $('#prop_operation_id').val(OPER_SELL);
      setPriceSliderOptions('price_slider', default_slider_max1, default_slider_step1, default_slider_min1, default_slider_max1);
    }
  });
  
  jQuery('input[placeholder]').addPlaceholder({ 'class': 'hint'}); //{dotextarea:false, class:hint}
  
});

function checkForm()
{
  var priceValues = getPriceValues();
  jQuery('#price_min').val(priceValues[0]);
  jQuery('#price_max').val(priceValues[1]);
  return true;
}