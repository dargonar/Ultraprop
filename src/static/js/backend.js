// JavaScript Document
function toggle_text(id,id2,text1,text2)
{
	jQuery(id).toggle();

	if( jQuery(id2).html() == text1 )
		jQuery(id2).html(text2);
	else
		jQuery(id2).html(text1);
		
	return false;
}

var map;
var marker;
var geocoder;
var put_marker;

function map_initialize() {
  geocoder = new google.maps.Geocoder();
  var latlng;
  var zoom = 18;
  if( $('#location').val() != '')
  {
    var parts = $('#location').val().split(',');
    latlng = new google.maps.LatLng(parts[0], parts[1]);
  }
  else
  {
    // latlng = new google.maps.LatLng(-34.397, 150.644);
    // LatLong del hint (Aguirre 276...).
    latlng = new google.maps.LatLng(-34.59962,-58.433897);
    zoom = 15;
  }
  
  var myOptions = {
    zoom: zoom,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  
  //if( $('#location').val() != '')
  //{
  put_marker_at(latlng);
  //}
}
 
function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.google.com/maps/api/js?sensor=false&callback=map_initialize&language=es";
  document.body.appendChild(script);
}

function handle_result(result, status, latlong)
{
  $('#searchmap').val(result.formatted_address);
  
  //Limpiamos y actualizamos actualizamos campos del form
  $('form#registerform>dl.form.x2col').find('input').val('');

  if( latlong == null )
  {
    $('#location').val(result.geometry.location.lat() + ',' + result.geometry.location.lng());
  }
  else
  {
    $('#location').val(latlong.lat() + ',' + latlong.lng());
  }
            
  for(var r in result.address_components)
  {
    var x = result.address_components[r];
    if( x.types[0] == 'street_number' )
    {
      var parts = x.short_name.split('-');
      $('#street_number').val(parts[0]);
    }
    if( x.types[0] == 'route' )
      $('#street_name').val(x.long_name);
    if( x.types[0] == 'administrative_area_level_1' )
      $('#state').val(x.long_name);
    if( x.types[0] == 'locality' )
      $('#city').val(x.long_name);
    if( x.types[0] == 'country' )
      $('#country').val(x.long_name);
    if( x.types[0] == 'neighborhood' )
      $('#neighborhood').val(x.long_name);
  }
        
  if( put_marker )
  {
    map.setCenter(result.geometry.location);
    put_marker_at(result.geometry.location);
  }
}

function put_marker_at(position)
{
    if( marker ) 
      marker.setMap(null);
    
    marker = new google.maps.Marker({
        map: map, 
        position: position,
        draggable: true
    });

    google.maps.event.addListener(marker, 'dragend', function() {
      put_marker = false;
      geocoder.geocode({latLng:marker.getPosition()}, function(results, status) { 
        //alert('tengo geocode result:' + marker.getPosition() + ' - ' + results[0].geometry.location );
        handle_result(results[0], status, marker.getPosition() ); 
      });
    });
}

function is_from_country(item, country)
{
  //Solo direcciones de argentina
  for(var i=0; i<item.address_components.length; i++)
  {
    var acomp = item.address_components[i];
    if( acomp.types[0] == 'country' && acomp.long_name.toUpperCase() == country.toUpperCase())
      return true;
  }
  
  return false;
}

function init_new_property()
{
  //Cargamos maps api
  loadScript();
  
  //Lindez de los forms
  $('[jqtransform|=true]').jqTransform();

  //Pone estilo 'Selected' cuando marcan checkbox y limpia errores <p>
  $(".typebox>div>.ex-label>.jqTransformCheckboxWrapper>.jqTransformCheckbox").click( function() {

    var typebox = $(this).parents('.typebox:first');
    $(typebox).toggleClass('selected', $(this).hasClass('jqTransformChecked'));

    //recalculate operation
    var val=0;
    $(".typebox>div>.ex-label>.jqTransformCheckboxWrapper>.jqTransformCheckbox.jqTransformChecked+input").each( function(i, field) {
      var tmp = field.id.split('_');
      val |= parseInt( tmp[1] );
    });
    $("#prop_operation_id").val(val);
    
    var op = $(this).parents('dd.operation:first');
    op.removeClass('errorbox');
    op.find('p.error').remove();
  });
  
  $("#description").focus( function() {
    $(this).removeClass('errorbox');
  });
  
  //Boton localizador
  $('#btnSearch2').click( function() {
    var address = document.getElementById("searchmap").value;

    put_marker = true;
    geocoder.geocode({'address': address,'region' : 'ar'}, function(results, status){ 
    
      var handled = false;
      $.each(results, function(i, item) {
        if( is_from_country(item, 'Argentina') )
        {
          handle_result(item, status, null);
          handled = true;
          return false;
        }
      });
      
      if (status != google.maps.GeocoderStatus.OK || handled == false) 
      {
        alert("Imposible ubicar dirección, intente 'altura calle,ciudad'");
        return;
      }
      
    });
  });  

  //Autocomplete textbox
  $("#searchmap").autocomplete({
    source: function(request, response) {
      geocoder.geocode( {'address': request.term, 'region' : 'ar'}, function(results, status) {
        response($.map(results, function(item) {
                  
                  //Solo direcciones de argentina
                  if( !is_from_country(item,'Argentina') )
                    return null;

                  return {
                        label: item.formatted_address,
                        value: item.formatted_address,
                        result: item
                  };
        }));
      });
    },
    select: function(event, ui) {
      put_marker = true;
      handle_result(ui.item.result, google.maps.GeocoderStatus.OK, null);
    }
  });   

  //No submit cuando enter en el campo de busqueda
  $("#searchmap").keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
  
  $("#toimages").click( function(e) {
    $("input[name=goto]").val('go');
  });
  
  //$( "#mnuLeft" ).accordion({ autoHeight: false });
	//$( "#mnuLeft" ).accordion({ active: 1 });
  
}

function bytesToSize(bytes, precision)
{  
    var kilobyte = 1024;
    var megabyte = kilobyte * 1024;
    var gigabyte = megabyte * 1024;
    var terabyte = gigabyte * 1024;
   
    if ((bytes >= 0) && (bytes < kilobyte)) {
        return bytes + ' B';
 
    } else if ((bytes >= kilobyte) && (bytes < megabyte)) {
        return (bytes / kilobyte).toFixed(precision) + ' KB';
 
    } else if ((bytes >= megabyte) && (bytes < gigabyte)) {
        return (bytes / megabyte).toFixed(precision) + ' MB';
 
    } else if ((bytes >= gigabyte) && (bytes < terabyte)) {
        return (bytes / gigabyte).toFixed(precision) + ' GB';
 
    } else if (bytes >= terabyte) {
        return (bytes / terabyte).toFixed(precision) + ' TB';
 
    } else {
        return bytes + ' B';
    }
}