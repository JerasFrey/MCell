scrfile = "pascal/ip3/template_IGDr150.mdl"
modelname = "IST10HzDi"
modelfolder = "IP3_T10Hz"


vdcc_number = "80"

dst_range = [-50, 750, 50]

f = open(scrfile,'r')
filedata = f.read()
f.close

for i in range(dst_range[0], dst_range[1]+dst_range[2], dst_range[2]):
	fname_replace = 'fname = "'+modelname+str("%03d" %i)+'"'
	newdata = filedata.replace('fname = "IGDr150_template"',fname_replace).replace("ip3r_distance = 150","ip3r_distance = "+str(i)).replace("VDCC_number_presynaptic = 80","VDCC_number_presynaptic = "+vdcc_number).replace('modelname = "IP3"','modelname = "'+modelfolder+'"').replace('output_folder = "/home/pascal/Documents/IISER_Internship/MCell/Nishants_model/output/"','output_folder = "/storage/subhadra/pascal/output/"')
	trgfile = "pascal/ip3/" + modelname + str(i) + ".mdl"
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
