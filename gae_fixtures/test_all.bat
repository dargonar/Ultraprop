appcfg.py upload_data --email=admin --application=dev~viralizar --filename=realstatebulked.csv --config_file=bulkloader.yaml --url=http://localhost:8096/remote_api --kind=RealEstate ../src
appcfg.py upload_data --email=admin --application=dev~viralizar --filename=propertybulked.csv  --config_file=bulkloader_prop.yml --url=http://localhost:8096/remote_api --kind=Property ../src
