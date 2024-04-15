# Final model
def print_parameters(myDict):
	myGroup = {}
	myGroup['Prime Editing'] = ['genome_fasta','scaffold','n_jobs','debug','PE2_model','PE3_model','extend_length']
	myGroup['PBS searching'] = ['min_PBS_length','max_PBS_length']
	myGroup['RTT searching'] = ['min_RTT_length','max_RTT_length','min_distance_RTT5','max_max_RTT_length']
	myGroup['sgRNA searching'] = ['gRNA_search_space','sgRNA_length','offset','PAM','max_target_to_sgRNA','max_max_target_to_sgRNA']
	myGroup['ngRNA searching'] = ['max_ngRNA_distance']
	for k in myGroup:
		print_group(myDict,myGroup[k],k)


def print_group(myDict,myList,group_title):
	print ("-------- Parameter Group: %s --------"%(group_title))
	for l in myList:
		print ("%s: %s"%(l,myDict[l]))


#تعریف پارامترهای پیش فرض
def get_parameters(config):
	p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
	# return dict
	parameters = {}
	# default parameters
	pre_defined_list = {}
	#------------ Prime Editing related-----------
	#این ورودی را باید برای برنامه فراهم کنم
	pre_defined_list["genome_fasta"] = "/home/yli11/Data/Human/hg19/fasta/hg19.fa"
	pre_defined_list["n_jobs"] = -1
	pre_defined_list["scaffold"] = "GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC"
	pre_defined_list["debug"] = 0
	pre_defined_list["extend_length"] = 1000 # extracting +- 1000bp center at target pos from the genome, in 99.9% cases, you don't need to change this. If change to less than 500, will trigger fasta input mode, may cause error.
	#   مدل های از پیش آموزش دیده را اینجا معرفی می کنم.
	# می تونی DEEPPRIME بزاری
	pre_defined_list["PE2_model"] = p_dir+"../model/PE2_model_final.py"
	pre_defined_list["PE3_model"] = p_dir+"../model/PE3_model_final.py"

	#------------ PBS -----------
	pre_defined_list["min_PBS_length"] = 10
	pre_defined_list["max_PBS_length"] = 15

	#------------ RTT -----------
	pre_defined_list["min_RTT_length"] = 10
	pre_defined_list["max_RTT_length"] = 20 # if no candidate is found, this value will be increased by 5, max to max_max_RTT_length
	pre_defined_list["max_max_RTT_length"] = 50
	pre_defined_list["min_distance_RTT5"] = 5

	#------------ sgRNA -----------
	pre_defined_list["gRNA_search_space"] = 200
	pre_defined_list["sgRNA_length"] = 20
	pre_defined_list["offset"] = -3
	pre_defined_list["PAM"] = "NGG"
	pre_defined_list["max_target_to_sgRNA"] = 10 # if no candidate is found, this value will be increased by 5, max to max_max_target_to_sgRNA
	pre_defined_list["max_max_target_to_sgRNA"] = 30

	#------------ ngRNA ------------
	pre_defined_list["max_ngRNA_distance"] = 100 # if no candidate is found, this value will be increased by 20, max to max_max_ngRNA_distance
	pre_defined_list["max_max_ngRNA_distance"] = 200
	pre_defined_list["search_iteration"] = 1 # not affect anything

	try:
		with open(config, 'r') as f:
			manifest_data = yaml.load(f,Loader=yaml.FullLoader)
	except:
		print ("Config data is not provided or not parsed successfully, Default parameters were used.")

	for p in pre_defined_list:
		try:
			parameters[p] = manifest_data[p]
		except:
			parameters[p] = pre_defined_list[p]
	return parameters


import warnings
warnings.filterwarnings("ignore")
import sys
import argparse
import datetime
import getpass
import os

#Output: The output folder will contain:
#1. all pegRNA + ngRNA combination for the input vcf file
#2. top1 pegRNA + ngRNA combination for each variant
#3. visualization of the top1s [TODO]
#4. a summary file of each variant

# گرفتن ورودی ها به شکل فایل
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="pegRNA design")
	username = getpass.getuser()

	mainParser.add_argument('-f','--input_file',  help="vcf or fasta",required=True)
	mainParser.add_argument('-c','--config',  help="A YAML file specifying parameters",default=None)

	mainParser.add_argument('-o','--output',  help="output dir",default="easy_prime_%s_%s_result_dir"%(username,str(datetime.date.today())))

	#add parameters above
	args = mainParser.parse_args()
	return args


# دو گامی که در سکشن بالا تعریف کرده ام را اینجا فراخوانی می کنم.
def run_steps(t,**kwargs):
	t.init(**kwargs)
	t.search(**kwargs)
	t.predict(**kwargs)
	return [t.topX,t.rawX,t.X_p,t.found_PE3b,t.found_PE3,t.found_dPAM,t.found_PE2,t.N_sgRNA_found]





def main():

	#پارامترها را به صورت فایل میگیرم
  #برای هر تارگت کلاس بالا را فراخوانی می کنم
	args = my_args()
	# ------------------------- get parameters ----------------------------------------------

	parameters = get_parameters(args.config)
	print_parameters(parameters)

	try:
		vcf = pd.read_csv(args.input_file,comment="#",sep="\t",header=None)
		vcf[1] = vcf[1].astype(int)
		vcf =vcf.drop_duplicates(2) # remove duplicated names
		vcf[3] = [x.upper() for x in vcf[3]]
		vcf[4] = [x.upper() for x in vcf[4]]
		vcf[5] = vcf2fasta(vcf,**parameters)
		vcf = vcf[list(range(6))]

	except:
		try:
			print ("Reading fasta file: %s"%(args.input_file))
			vcf = fasta2vcf(args.input_file)
			print (vcf)
		except:
			print ("Can't read %s as vcf or fasta. Please check input. Exit..."%(args.input_file))
			exit()

	variant_list = vcf[2].tolist()


## for each target, create target mutation class
	my_targets = [target_mutation(*r) for i,r in vcf.iterrows()]



#find best pegRNAs
# backend can affect this parallization, if so, user show use n_jobs=1
	if parameters['n_jobs'] == 1:
		df_list = [run_steps(t,**parameters) for t in my_targets]
	else:
		from joblib import Parallel, delayed
		df_list = Parallel(n_jobs=parameters['n_jobs'],verbose=10)(delayed(run_steps)(t,**parameters) for t in my_targets)


#--------------------------------------------ضروری نیست می توانی این ها را حذف کنی-------------------------------------------------------------------------
	# save output
	#یا این کد ها و یا کدهای نوشته شده قبلی، فقط چاپ سطری در بالا
	import subprocess
	subprocess.call("mkdir -p %s"%(args.output),shell=True)
	summary = pd.DataFrame([x[3:8] for x in df_list]).astype(int)
	summary.columns = ['found_PE3b','found_PE3','found_dPAM','found_PE2',"N_sgRNA_found"]
	summary.index = variant_list
	summary.to_csv("%s/summary.csv"%(args.output),index=True)

	df_top = pd.concat([x[0] for x in df_list])
	if df_top.shape[0]==0:
		print ("no pegRNA were found for the input file: %s"%(args.input_file))
		sys.exit()
	df_top = df_top.sort_values("predicted_efficiency",ascending=False)
	df_top.to_csv("%s/topX_pegRNAs.csv"%(args.output),index=False)

	df_all = pd.concat([x[1] for x in df_list])
	df_all = df_all.sort_values("predicted_efficiency",ascending=False)
	df_all.to_csv("%s/rawX_pegRNAs.csv.gz"%(args.output),index=False,compression="gzip")

	X_p = pd.concat([x[2] for x in df_list])
	X_p = X_p.sort_values("predicted_efficiency",ascending=False)
	X_p.to_csv("%s/X_p_pegRNAs.csv.gz"%(args.output),index=True,compression="gzip")




if __name__ == "__main__":
	main()