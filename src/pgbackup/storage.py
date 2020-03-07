import oci

def local(infile, outfile):
    outfile.write(infile.read())
    outfile.close()
    infile.close()

config = oci.config.from_file()
object_storage = oci.object_storage.ObjectStorageClient(config)
ostorage = oci.object_storage.ObjectStorageClient(config)
namespace = object_storage.get_namespace().data

def oci(namespace, bucket, infile,name):
    ostorage.put_object(namespace,bucket,infile.name,infile)
