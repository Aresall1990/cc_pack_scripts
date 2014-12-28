import os
import subprocess
import re
import getpass
import time
import tarfile

BASE_TARGET_NUMBER = '19003'
BASE_CONTAINER_NUMBER = '19090'
BASE_INDEX_NUMBER = '19089'
CLASS_NUMBER = "190 89"
id_num = {'CAA': [ 'CAA', '204'], 'CXA': ['CXA', '109'], 'CXC': ['CXC', '146']};

#container_dir = "/home/eostkra/I_am_CM_now/ccpack_scripts/python_version/python_containers/"
#RAD_HOME = "/proj/bscrp/radrp/"

class Ccpack:

	os.environ["RAD_HOME"] = "/proj/bscrp/radrp/"   

	def __init__(self, label = None, directory = None):

		if directory != None and label != None:
			self.check_directory(directory)
			self.check_label(label, directory)
		else:
			pass

	def check_directory (self, directory):

		if os.path.exists(directory):
			pass
		else:
			print ("Directory " + directory +  " doesn't exists")
			exit(0)


	def check_label (self, label, directory):
		'''
		Check for label existence 
		'''
		# cmd = ' '.join(['/usr/atria/bin/cleartool', 'lstype', '-kind', 'lbtype', '-short' , '-invob', directory])
		# vob_labels = self.run_command(cmd).decode('utf-8')
		#(vob_labels) = vob_labels.split('\n')
		#print (vob_labels)
		vob_labels = [ 'CAA_1640_1100_R1A01', 'CAA_1685_2000_R1A01', 'CAA_1675_2000_R1A01', 'CXA_1640_1100_R1A01', 'CAA_1608_1000_R1A02', 'CAA_1607_1300_R1B01', 'CXA_1607_1300_R1B01', 'CXA_1608_1000_R1A02', 'CXA_1611_1000_R1A01', 'CAA_1611_1000_R1A01', 'R12_DROP_12.0_BL', 'CXA_1640_1100_R1A01']
		if label in vob_labels:
			print ("Warning! Label " + label + " exists, but not locked")
		elif label + ' (locked)' in vob_labels:  
			print ("Label " + label + " exists, and it is locked")
		else:
			print ("Label " + label + " doesn't exist")
			exit(0)

	def get_files(self, directory, subdir, label):
		'''
		Method for getting files basing on lable
		'''
		files = ''
		if subdir == "":
			cmd = ' '.join(['/usr/atria/bin/cleartool', 'find', ' ' + directory, '-type', 'f', '-ver', "\"lbtype(" + label, ")\"", '-print']) 
			files += self.run_command(cmd).decode('utf-8')
		else:	
			cmd = ' '.join(['/usr/atria/bin/cleartool', 'find', ' ' + directory + "/" + subdir, '-type', 'f', '-ver', "\"lbtype(" + label, ")\"", '-print']) 
			files += self.run_command(cmd).decode('utf-8')   
			cmd = ' '.join(['/usr/atria/bin/cleartool', 'find', ' ' + directory + "/" + subdir, '-type', 'l', '-print'])
			files += self.run_command(cmd).decode('utf-8') 
		files_for_tar = '\n'.join (self.mysplit (files))
		files_for_index = ''.join(self.mysplit( files, directory + '/' ))
		files_for_index = '\n'.join(self.mysplit( files_for_index))

		return files_for_index, files_for_tar

	def get_unit_name (self, directory):
		'''
		Method for getting unit name
		'''
		match = re.compile(r'([A-Z]+)')
		name = match.search(directory).group(0)
		return name

	def get_appl_RFPGAF (self, directory):

		match = re.compile (r'([A-Z]+_)([A-Z]+)')
		appl = match.search(directory).group(2)
		return appl

	def get_number (self, directory):     # there is no need to have it now...
		match = re.compile(r'([0-9]+)')
		number = match.search(directory).group(0)
		#number += str(caa_prod)
		return number

	def make_index_file (self, index_file, tar_file, product_label, files, id_num, prefix, prod_num, container_dir):
		'''
		Method for creating software record file
		'''
		user = getpass.getuser()
		date = time.strftime("%c")
		path_to_store = container_dir + index_file # for now its my local directory... SHOULD be changed of course
		fo = open(path_to_store, "wt")
		fo.write ("#-------------------------------------------------\n")
		fo.write ("# Software record for file " + tar_file + "\n")

		if product_label != "no label":
			fo.write ("# Versions selected by " + product_label + "\n")

		fo.write ("# Created by " + user + "\n" )
		fo.write ("# Date " + date + "\n" )
		fo.write ("# " + "\n" )
		fo.write ("# CLASS " + CLASS_NUMBER + "\n" )

		if prefix == "":
			fo.write ("# NUMBER " + id_num[0] + " " + id_num[1] + " " + str(prod_num) + "\n" )
		else:
			#num_prefix = prefix.rsplit('_', 1)[0]
			fo.write ("# NUMBER " + prefix + "/" + id_num[0] + " " + id_num[1] + " " + str(prod_num) + "\n" ) # 7/CXC 146 1640
		fo.write ("# REVISION				A" + "\n" )
		fo.write ("#-------------------------------------------------\n")
		fo.write ("# " + "\n" )
		for f in files:

			fo.write (f )
		print ("Index file is created for " + id_num[0] + " product")
		fo.close()

	def make_tar_file (self, files, tar_file, id_num, container_dir, index_file, vob_dir, unit_dir): 	
		'''
		Method for creating container file
		'''	
		files_list = ""
		(files) = files.split('\n')
		tar = tarfile.open(container_dir + tar_file, "w")

		for f in files:
			if id_num[0] == "CAA":

				if "CP_RP" in f or "_COMMON" in f:
					if f != '':
						tar.add (f,  '../' +''.join(self.mysplit( f, vob_dir + '/' )).rsplit('@@', 1)[0])
				else:
					if f != '':
						tar.add (f, ''.join(self.mysplit( f, unit_dir + '/' )).rsplit('@@', 1)[0])
			else:
				if f != '':
					tar.add (f, './' + ''.join(self.mysplit( f, unit_dir + '/' )).rsplit('@@', 1)[0])
		tar.add (container_dir + index_file, index_file) 
		tar.close()
		print ("Tar file is created for " + id_num[0] + " product")

	def run_command (self, command):
		'''
		Method for running commands
		'''
		result = subprocess.Popen(command,
								stdout = subprocess.PIPE, \
								stdin=subprocess.PIPE, \
								stderr=subprocess.STDOUT,
								shell=True).communicate()[0]

		return result

	def get_suffix_revision (self, caa_label):
		suffix = caa_label.rsplit('_', 2) [1]
		revision = caa_label.rsplit('_', 2) [2].lower()
		return suffix, revision

	def get_cxc_prefix_product (self, parameter):
		product = parameter.rsplit('_', 1) [1]
		prefix = parameter.rsplit('_', 1) [0]
		return prefix, product

	def get_rpc_file (self, cxc_directory):
		cmd = ' '.join(['find', cxc_directory + '/*', '-name', '\'*.rp*\'', '-print'])
		rpc_file = self.run_command(cmd)
		return rpc_file.decode('utf-8')

	def  make_index_target_file_name(self, prod_num, id_name, prefix, caa_label ): 
		if id_name[0] == 'CAA' or id_name[0] == 'CXA' :
			index_file_name = ''.join ([ BASE_INDEX_NUMBER, '-', id_name[0], id_name[1], str(prod_num), self.get_doc_revision(caa_label),'.txt' ])
			target_file_name = ''.join ([ BASE_CONTAINER_NUMBER, '-', id_name[0], id_name[1], str(prod_num), self.get_doc_revision(caa_label), '.tar' ])
		elif id_name[0] == 'CXC':
			index_file_name = ''.join([ BASE_INDEX_NUMBER, '-', prefix, '_', id_name[0], id_name[1], str(prod_num), self.get_doc_revision(caa_label),'.txt' ])
			target_file_name = ''.join([ BASE_CONTAINER_NUMBER, '-', prefix, '_', id_name[0], id_name[1], str(prod_num), self.get_doc_revision(caa_label), '.tar' ])
		return index_file_name, target_file_name

	def make_target_file (self, target_file_name, index_file_name, label, container_dir, rpc_files, prefix, unit_name, prod_no, id_name, unit_dir):
		#rpc_files = "/home/eostkra/I_am_CM_now/test/RGMACR/8_CXC1461640_1100/r1a01/test1.txt\n /home/eostkra/I_am_CM_now/test/RGMACR/8_CXC1461640_1100/r1a01/test2.txt\n"
		i = 1
		files_for_tar = ''.join (self.mysplit( rpc_files, '\n'))
		files_for_index = ''.join (self.mysplit( rpc_files, '\n')).split(unit_dir)[1]
		rpc_amount = len(self.mysplit (rpc_files))
		if rpc_amount >= 2:
			for f in files_for_tar:
				if i <= rpc_amount:
					target_file = ''.join ([container_dir, str(i), '_', target_file_name])
					tar = tarfile.open(target_file, "w")
					test = ''.join (f.split(unit_dir)[1])
					tar.add (f, ''.join (f.split(unit_dir)[1]) )
					self.make_index_file(index_file_name, str(i) + '_' + target_file_name, 'no label', files_for_index, id_name, prefix, prod_no, container_dir )
					i += 1
		else:
			target_file = ''.join ([container_dir, target_file_name])
			tar = tarfile.open(target_file, "w")
			test = rpc_files  + './' + rpc_files.split()[0]
			tar.add (files_for_tar, ''.join (self.mysplit( rpc_files, '\n')).split(unit_dir)[1] )
			self.make_index_file(index_file_name, target_file_name, 'no label', files_for_index,  id_num['CXC'], prefix, prod_no, container_dir )

	def get_doc_revision (self, caa_label):
		dict_num = dict (zip (range(1,21), self.letter_range('A', 'Z', [ 'O', 'P', 'Q', 'R', 'W'])))
		dict_letter = {'a': ""}
		dict_letters = dict (zip (self.letter_range('b', 'z', [ 'o', 'p', 'q', 'r', 'w']), range(1,21)))
		dict_letters.update (dict_letter)
		revision = caa_label.rsplit('_', 2)[2]
		regexp = re.compile (r'([A-Z])([0-9])([A-Z])([0-9])([0-9])')
		if regexp.match (revision):
			rev_letter = regexp.match (revision).group(3).lower()
			rev_number = int(regexp.match (revision).group(2))		
			doc_revision = ''.join(["_", dict_num[rev_number] + str(dict_letters[rev_letter])])
		else:
			doc_revision = ''		
		return doc_revision

	def mysplit(self, s, delim = None):
		return [l for l in s.split(delim) if l]

	def letter_range(self, start, stop, exeptions):
		letter_list = []
		for c in range(ord(start), ord(stop)):
			if chr(c) not in exeptions:
				letter_list.append(chr(c))
		return letter_list

	def compress (self, tar_file):

		cmd = ' '.join(['compress', '-f', tar_file])
		self.run_command(cmd)
		#`compress -f $file`;

	def create_caa_container (self, caa_dir, caa_label, caa_prod, container_dir):

		print ("Creating CAA container...")	
		print ("Working directory is " + caa_dir)

		index_files = ""
		target_files = ""
		vob_dir = caa_dir.rsplit('/', 1) [0]
		for subdir in ['doc/', 'man/', 'subunits/']:
			if os.path.exists( caa_dir + '/' + subdir):
				(files_for_index, files_for_tar) = self.get_files(caa_dir, subdir, caa_label)
				if files_for_index != "":
					index_files += files_for_index + "\n"
					target_files += files_for_tar + "\n"
		sub_cp_rp_dir = self.get_unit_name(caa_dir) + "_CP_RP/"
		sub_common_dir = self.get_unit_name(caa_dir) + '_COMMON_CAA252'
		
		if os.path.exists(vob_dir + '/' + sub_cp_rp_dir):
			(cp_rp_files_for_index, cp_rp_files_for_tar) = self.get_files(vob_dir, sub_cp_rp_dir, caa_label)
			for cp_rp_file in cp_rp_files_for_index.split('\n'):		
				index_files += "../" + cp_rp_file + '\n'
			target_files += cp_rp_files_for_tar
		elif 'RFPGAF' in caa_dir and os.path.exists(vob_dir + '/' + sub_common_dir):
			(common_files_for_index, common_files_for_tar) = self.get_files(vob_dir, sub_common_dir, caa_label)
			for common_file in common_files_for_index.split('\n'):		
				index_files += "../" + common_file + '\n'
			target_files += common_files_for_tar
		if self.get_number(caa_dir) != '204':	
			id_num['CAA'][1] = self.get_number(caa_dir) # now there will be 252 not 204

		(index_file_name, tar_file_name) = self.make_index_target_file_name (caa_prod, id_num['CAA'], '', caa_label)
		self.make_index_file (index_file_name, tar_file_name, caa_label, index_files, id_num['CAA'], "", caa_prod, container_dir )
		self.make_tar_file (target_files, tar_file_name, id_num['CAA'], container_dir, index_file_name, vob_dir, caa_dir )
		self.compress (container_dir + tar_file_name)

	def create_cxa_container (self, directory, cxa_label, cxa_prod, container_dir):

		vob_dir = directory.rsplit('/', 1) [0]

		if self.get_unit_name(directory) + "_" + self.get_appl_RFPGAF(directory) + "_CAA" in directory and 'RFPGAF' in directory:
			cxa_dir = vob_dir + "/" + self.get_unit_name(directory) + "_" + self.get_appl_RFPGAF(directory) + "_" + "CXA"
		elif self.get_unit_name(directory) + "_CAA" in directory and 'RFPGAF' not in directory:
			cxa_dir = vob_dir + "/" + self.get_unit_name(directory) + "_" + "CXA"
		elif self.get_unit_name(directory) + "_CXA" in directory:
			cxa_dir = directory 

		print ("Creating CXA container...")
		print ("Working directory is " + cxa_dir) 

		index_files = ""
		target_files = ""
		# vob_dir = caa_dir.rsplit('/', 1) [0]
		# cxa_dir = vob_dir + "/" + self.get_unit_name(caa_dir) + "_" + "CXA"
		(files_for_index, files_for_tar) = self.get_files(cxa_dir, "", cxa_label)
		
		if files_for_index != "":
			(index_file_name, tar_file_name) = self.make_index_target_file_name (cxa_prod, id_num['CXA'], '', cxa_label)
			self.make_index_file (index_file_name, tar_file_name, cxa_label, files_for_index, id_num['CXA'], "", cxa_prod, container_dir )
			self.make_tar_file (files_for_tar, tar_file_name, id_num['CXA'], container_dir, index_file_name, '', cxa_dir)
			self.compress (container_dir + tar_file_name)
		else:
			print ("CXA directory is empty for the label " + cxa_label + "container file will not be created")

	def create_cxc_containers (self, caa_dir, caa_label, cxc_parameters, container_dir):

		(suffix, revision) = self.get_suffix_revision (caa_label)
		for parameter in cxc_parameters:
			(prefix, product) = self.get_cxc_prefix_product(parameter)
			CXC_dir = ''.join([prefix, '_', id_num['CXC'][0] + id_num['CXC'][1] + product, '_' + suffix])

			print ("Creating CXC container for prefix " + prefix)
			print ("Working directory is " + CXC_dir)

			CXC_path = ''.join([os.environ['RAD_HOME'], self.get_unit_name(caa_dir), '/', CXC_dir])
			CXC_unit_dir = ''.join([os.environ['RAD_HOME'], self.get_unit_name(caa_dir), '/'])
			unit_name = self.get_unit_name(caa_dir)
			#print (CXC_path)
			(index_file_name, target_file_name) = self.make_index_target_file_name(product, id_num['CXC'], prefix, caa_label )
			if os.path.exists(CXC_path + "/" + revision):
				#os.chdir (CXC_path + "/" + revision)
				rpc_files = self.get_rpc_file (CXC_path + "/" + revision)
				if rpc_files != "":
					self.make_target_file (target_file_name, index_file_name, caa_label, container_dir, rpc_files, prefix, unit_name, product, id_num['CXC'],CXC_unit_dir)	
					self.compress (container_dir + target_file_name)
					print ("Tar file is created for CXC")

			else:
				print ("ERROR: Directory " + CXC_path + "/" + revision + " not found under" + os.environ['RAD_HOME']/self.get_unit_name(caa_dir)) # do this with printf	


	# def create_caa_container (self, caa_dir, caa_label, caa_prod):
	# 	print ("Creating CAA container...")			
	# 	files = ""
	# 	vob_dir = caa_dir.rsplit('/', 1) [0]
	# 	sub_cp_rp_dir = caa.get_unit_name(caa_dir) + "_CP_RP/"
	# 	for subdir in ['doc/', 'man/', 'subunits/']:
	# 		files += caa.get_files(caa_dir, subdir, caa_label) + '\n'

