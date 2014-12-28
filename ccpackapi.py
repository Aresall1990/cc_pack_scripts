from  Ccpack import Ccpack

def create_container_files_all (caa_dir, caa_label, caa_prod, cxa_label, cxa_prod, cxc_parameters, container_dir):
	caa = Ccpack(caa_label, caa_dir)
	caa.create_caa_container(caa_dir, caa_label, caa_prod, container_dir)
	cxa = Ccpack(cxa_label, caa_dir)
	cxa.create_cxa_container(caa_dir, cxa_label, cxa_prod, container_dir)
	cxc = Ccpack()
	cxc.create_cxc_containers(caa_dir, caa_label, cxc_parameters, container_dir)

def create_caa_cxa_containers (caa_dir, caa_label, caa_prod, cxa_label, cxa_prod, container_dir):
	caa = Ccpack(caa_label, caa_dir)
	caa.create_caa_container(caa_dir, caa_label, caa_prod, container_dir)
	cxa = Ccpack(cxa_label, caa_dir)
	cxa.create_cxa_container(caa_dir, cxa_label, cxa_prod, container_dir)

def create_cxa_container (cxa_dir, cxa_label, cxa_prod, container_dir):
	cxa = Ccpack(cxa_label, cxa_dir)
	cxa.create_cxa_container(cxa_dir, cxa_label, cxa_prod, container_dir)

def create_caa_cxc_containers (caa_dir, caa_label, caa_prod, cxc_parameters, container_dir):
	caa = Ccpack(caa_label, caa_dir)
	caa.create_caa_container(caa_dir, caa_label, caa_prod, container_dir)
	cxc = Ccpack()
	cxc.create_cxc_containers(caa_dir, caa_label, cxc_parameters, container_dir)