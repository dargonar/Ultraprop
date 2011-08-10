import codecs

f = codecs.open('imagefilebulker.csv', "w", "utf-8")
suto =  'key,title,created_at,filename,file,property\r\n'
f.write(suto.encode('utf-8'))

seed = 1001
blob_key = 'KFD1knA4mKyZjBSkqzn-bw=='
for n in range(1):
  seto =  "%s,%s %s,2011-06-14T20:55:54,Filename,google.appengine.ext.blobstore.BlobKey('%s'),%s\r\n" % (seed,'Image nro', seed,blob_key,seed)
  f.write(seto.encode('utf-8'))
  seed = seed+1 
f.close()
