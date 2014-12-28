import argparse
import sys
import ccpackapi

def create_argument_parser():

	parser = argparse.ArgumentParser(prog='ccpack',
                                     description='Create container files',
                                     epilog='2014, Ostap Kravchuk')

	parser = argparse.ArgumentParser()

	parser.add_argument('-vob',  action='store', required=True, dest='directory', 
                   		 help='Store a CAA directory')

	parser.add_argument('-caa_label', action='store', dest='caa_label', default='not_given',
                  		  help='Store a CAA label')

	parser.add_argument('-cxa_label', action='store', dest='cxa_label', default='not_given',
                   		 help='Set a CXA label')

	parser.add_argument('-caa_prod', action='store', dest='caa_prod', default='not_given', 
                  		  help='Set a CAA product number')

	parser.add_argument('-cxa_prod', action='store', dest='cxa_prod', default='not_given',
                   		 help='Set a CXA product number')

	parser.add_argument('-cxc_parameters', action='store', dest='cxc_parameters', default='not_given', nargs='+', 
                   		 help='Set the CXC parameter values')

	parser.add_argument('-container_dir', action='store', dest='container_dir', required=True,
                   		 help='Directory where conatainer files will be stored')

	parser.add_argument('--version', action='version', version='%(prog)s 1.0')

	return parser

def main():
	parser = create_argument_parser() 
	args = parser.parse_args()

	if args.caa_label == 'not_given' and args.caa_prod == 'not_given' and args.cxc_parameters == 'not_given':

		ccpackapi.create_cxa_container (args.directory, args.cxa_label, args.cxa_prod, args.container_dir)

	if args.cxa_label == 'not_given' and args.cxa_prod == 'not_given':

		ccpackapi.create_caa_cxc_containers (args.directory, args.caa_label, args.caa_prod, args.cxc_parameters, args.container_dir)

	elif args.cxc_parameters == 'not_given':

		ccpackapi.create_caa_cxa_containers(args.directory, args.caa_label, args.caa_prod, args.cxa_label, args.cxa_prod, args.container_dir)
	else:
		ccpackapi.create_container_files_all(args.directory, args.caa_label, args.caa_prod, args.cxa_label, args.cxa_prod, args.cxc_parameters, args.container_dir)
	
	return 0

if __name__ == '__main__':
    sys.exit(main())
