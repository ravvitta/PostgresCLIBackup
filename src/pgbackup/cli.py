from argparse import Action, ArgumentParser

known_drivers = ['local', 'oci']

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error("Unknown driver. Available drivers are 'local' & 'oci'")
        namespace.driver = driver.lower()
        namespace.destination = destination

def create_parser():
    parser = ArgumentParser(description="""
    Back up PostgreSQL databases locally or to AWS OCI.
    """)
    parser.add_argument("url", help="URL of database to backup")
    parser.add_argument("--driver", "-d",
            help="how & where to store backup",
            nargs=2,
            metavar=("DRIVER", "DESTINATION"),
            action=DriverAction,
            required=True)
    return parser

def main():
    
    import oci
    import time
    from pgbackup import pgdump,storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)

    if args.driver == 'oci':
        config = oci.config.from_file()
        object_storage = oci.object_storage.ObjectStorageClient(config)
        ostorage = oci.object_storage.ObjectStorageClient(config)
        namespace = object_storage.get_namespace().data
        outfile = dump.communicate()[0]
        timestamp = time.strftime("%Y-%m-%dT%H:%M", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        ostorage.put_object(namespace,args.destination,file_name,outfile)
    else:
        outfile = open(args.destination,'wb')
        print(f"Backing database up locally to {outfile.name}")
        storage.local(dump.stdout,outfile)
