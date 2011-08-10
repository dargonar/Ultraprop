# -*- coding: utf-8 -*-
class Property():
  
  # AREA FIELDS
  area_indoor             = 350.0
    # 1	 # 0-40
    # 2	 # 40-50
    # 3	 # 50-60
    # 4	 # 60-70
    # 5	 # 60-100
    # 6	 # 100-200
    # 7	 # 200-300
    # 8	 # 300 o más
  area_outdoor            = 9.0
    # 1	  # 0-10
    # 2	  # 10-20
    # 3	  # 20-50
    # 4	  # 50-100
    # 5	  # 100 o más
  area_cells              = []

  rooms_count	            = 4 
    # 1 a 5 - P es >= 6
  bathrooms               = 5
    # 1 a 3 - P es >= 4
  bedrooms                = 6
    # 1 a 4 -	P es >= 5
  xrooms_cells            = []
    # = (x, y, z) => ( rooms_count, bathrooms, bedrooms)
    # alphabet x='012345P'
    # alphabet y='0123P'
    # alphabet z='01234P'
  
  # PRICES FIELDS
  price                   = 10000.0
  fee                     = 100.0
  
  # AMENITIES FIELDS GROUP 1
  appurtenance            = 1
  balcony                 = 0
  doorman                 = 1
  elevator                = 0
  fireplace               = 1
  furnished               = 0
  garage                  = 1
  
  xamenities_cells_g1     = []
  
  # AMENITIES FIELDS GROUP 2
  garden                  = 1
  grillroom               = 0
  gym                     = 1
  live_work               = 0
  luxury                  = 1
  pool                    = 0
  terrace                 = 1
  
  prop_type_id            = 9


  xamenities_cells_g2     = []
    # (t, u, v, w, x, y, z) =>(garden, grillroom, gym, live_work, luxury, pool, terrace)
    # alphbet='01' ¥
  
  # AMENITIES FIELDS GROUP 3 & YEAR BUILT
  washer_dryer            = 0
  sum	                    = 1
	
  year_built	            = 2005
  
  xamenities_cells_g3_and_year      = []
  prop_type_xbiz_cells              = []  
  # ==================== #
  # PRIVATE ============ #
  alphabet = '0123456789abcdef'
  config_dict_arrays = {
    'area_cells' : [
        {'propiedad':'area_indoor', 'rangos':[0.0, 40.0, 50.0, 60.0, 70.0, 100.0, 200.0, 300.0, 9999999999.0]}
        ,{'propiedad':'area_outdoor', 'rangos':[0.0, 10.0, 20.0, 50.0, 100.0, 9999999999.0]}
      ]
    , 'xamenities_cells_g1':
      [
        {'propiedad':'appurtenance', 'rangos':[0, 1]}
        , {'propiedad':'balcony', 'rangos':[0, 1]}
        , {'propiedad':'doorman', 'rangos':[0, 1]}
      ]
    , 'xamenities_cells_g3_and_year':
      [
        {'propiedad':'washer_dryer', 'rangos':[0, 1]}
        , {'propiedad':'sum', 'rangos':[0, 1]}
        , {'propiedad':'year_built', 'rangos':[ 1961, 1991, 2001, 2006, 2010, 9999999999]}
      ]
    , 'prop_type_xbiz_cells':
      [
            {'propiedad':'prop_type_id', 'rangos':[0, 5], 'is_binary':True}
          , {'propiedad':'prop_type_id', 'rangos':[0, 9], 'is_binary':True}
          , {'propiedad':'prop_type_id', 'rangos':[0, 'a'], 'is_binary':True}
          , {'propiedad':'prop_type_id', 'rangos':[0, 'b'], 'is_binary':True}
      ]
  }
  # Esta funcion retorna un par con (alphabet[x], alphabet[0:y])
  #   x = el indice del primer item mayor que value, si no se encuentra este item, retorna la longitud del array.
  #   y = len(array) + sum_plus. (sum_plus indica que la propiedad es de tipo rango y el máximo valor es "o más").
  def get_index_alphabet(self, value, array, is_binary=False):
    #return (self.alphabet[array.index( min(filter(lambda x:x<=value,array)) if value<array[-1:][0] else len(array))]
    if is_binary:
      this_alphabet = map(lambda x:str(x),array)
      return ( self.alphabet[array.index(value) if value in array else 0], this_alphabet)
    
    filtered = filter(lambda x:x>=value,array)
    return (self.alphabet[array.index( min(filtered))]
              , self.alphabet[0:len(array)] )
  
# Producto cartesiano de un array de listas.  
  def product(self, *args):
    if not args:
        return iter(((),)) # yield tuple()
    return (items + (item,) 
            for items in self.product(*args[:-1]) for item in args[-1])
  
  # Itera sobre las listas y llama a product .... 
  def build_list(self, cells):
    todos = []
    for i,v in enumerate(cells):
      items = []
      for j in range(0, len(cells)):
        items.append( [cells[j][0]] if j == i else cells[j][1] )
      todos += self.product( *items )
    return todos

  def check_options(self):
    for key in self.config_dict_arrays.keys():
      pair_array = []
      for prop in self.config_dict_arrays[key]:
        is_binary = False 
        if 'is_binary' in prop:
          is_binary = True
        pair = self.get_index_alphabet(getattr(self, prop['propiedad']), prop['rangos'], is_binary)
        pair_array.append(pair)
      setattr(self, key, self.build_list(pair_array))
      
  
o = Property()
o.check_options()
print ' area_cells'
print o.area_cells

# print ' xamenities_cells_g1'
# print o.xamenities_cells_g1

# print ' xamenities_cells_g2'
# print o.xamenities_cells_g2

# print ' xamenities_cells_g3_and_year'
# print o.xamenities_cells_g3_and_year

print ' prop_type_xbiz_cells'
print o.prop_type_xbiz_cells

