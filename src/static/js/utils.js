/* ========================================================================================== */
/* Utils  =================================================================================== */

function swithPropertyLocationMap(sender, img_id, img_map_src, map_type, map_type_selector_id){
  var new_src = img_map_src.replace('roadmap',map_type);
  jQuery('#'+img_id).attr('src', new_src); 
  jQuery('#'+map_type_selector_id+' span.selected').removeClass('selected'); 
  jQuery(sender).addClass('selected');
  return false;
}

var tmp_currency='$';

function getPriceValue(value){
  /*
  if(value<50)
    return Math.pow(value, 2)/100;
  return Math.pow((value-12), 2)/10;
  */
  return value;
}

function getPriceValues(){
  var values = jQuery("#price_slider").slider( "option", "values" );
  return [getPriceValue(values[0]), getPriceValue(values[1])];
}

function setPriceSliderOptions(price_slider, max, step, value0, value1)
{
  jQuery("#"+price_slider).slider( "option" , 'max' ,  max);
  jQuery("#"+price_slider).slider( "option" , 'step' , step);
  jQuery("#"+price_slider).slider( "option" , 'values' , [value0, value1] );
}
      
function formatRangePriceText(object_id, from, to, currency, max)
{
  tmp_currency = currency.toUpperCase();
  var max_limit = formatPriceText(to);
  if (to == max)
  {
    max_limit = '-sin límite-';
  }
  var str_html = '<small>'+tmp_currency+' </small><b>' + formatPriceText(from) + '</b>&nbsp;<font class="to">a</font>&nbsp;<b>' + max_limit + '</b>';
  jQuery('#'+object_id).html(str_html);
  
}

function formatPriceText(level) {
  
  var valor = level.toString();
  if(level>0)
    //valor = new Number(level*1000).numberFormat('#,#,#,#').replace(/,/g,'.').toString();
    valor = new Number(level).numberFormat('#,#,#,#').replace(/,/g,'.').toString();
  
  return valor;  
}

function formatPriceRange(level1, level2) {
  return 'US$ ' + level1.toString() + 'K a ' + level2.toString() + 'K';
}

function formatPrice(level) {
  if (level === null || typeof(level) == 'undefined')
    return '';
  
  if (level == -1) return '-';
  
  return 'US$ ' + formatCurrency(level);
}