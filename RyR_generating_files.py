scrfile = "pascal/ryr/RyR_template.mdl"
modelfolder = "RP20V90"
modelname = modelfolder+"Dr"

vdcc_number = "90"

dst_range = [-50, 750, 50]

f = open(scrfile,'r')
filedata = f.read()
f.close

for i in range(dst_range[0], dst_range[1]+50, dst_range[2]):
	fname_replace = 'fname = "'+modelname+str("%03d" %i)+'"'
	newdata = filedata.replace('fname = "RSDr350_template"',fname_replace).replace("ryr_distance = 350","ryr_distance = "+str(i)).replace("VDCC_number_presynaptic = 80","VDCC_number_presynaptic = "+vdcc_number).replace('modelname = "RyR"','modelname = "'+modelfolder+'"').replace('output_folder = "/home/pascal/Documents/IISER_Internship/MCell/Nishants_model/output/"','output_folder = "/storage/subhadra/pascal/output/"')
	trgfile = "pascal/ryr/" + modelname + str(i) + ".mdl"
	f = open(trgfile,'w')
	f.write(newdata)
	f.close()

'''
rep = {"condition1": "","condition2": "text","": ""}

rep = dict((re.escape(k), v) for k, v in rep.iteritems())
pattern = re.compile("|".join(rep.keys()))
text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
print(rep)
'''

#newdata += filedata.replace("ip3r_distance = 150","ip3r_distance = 350")
#newdata += filedata.replace('output_folder = "/home/pascal/Documents/IISER_Internship/MCell/Nishants_model/output/IP3/"','output_folder = "/home/subhadra/pascal/output/IP3/"')
