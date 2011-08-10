import codecs

seed = 1
f = codecs.open('realstatebulked.csv', "w", "utf-8")
suto =  'name,title,url,created_at,telephone_number,fax_number,updated_at,key,email\r\n'
f.write(suto.encode('utf-8'))
for n in range(10):
  seto = "Real State #%s, Real State name #%s ,http://www.realestate%s.com ,2011-06-14T20:55:54,011485792%s,011485892%s,2011-06-14T20:55:54, %s,info@realestate%s.com\r\n" % (seed,seed,seed,seed,seed,seed,seed)
  f.write(seto.encode('utf-8'))
  seed = seed+1 
f.close()
