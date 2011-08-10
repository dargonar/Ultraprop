//jQuery(document).ready(function()
function doKetchup(obj){
  var selector = 'form';
  if (obj!=null)
    selector = obj;
  jQuery(selector).append('<input type="text" name="inketchup" id="inketchup" value="" />');
  setTimeout(
    function() { 
        jQuery('#inketchup').val('2');
      }
    , 2000);
}