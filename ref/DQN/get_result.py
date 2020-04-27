import json


def LastNlines(fname, N): 
	output = {}
	with open(fname) as file: 
		for line in (file.readlines() [-N:]): 
			result = line.split(":")
			output[result[0]] = result[1].strip()
	json_object = json.dumps(output)
	with open("result.json", "w") as outfile: 
		outfile.write(json_object) 


# Driver Code:  
if __name__ == '__main__': 
	fname = 'log.txt'
	N = 5
	try: 
		LastNlines(fname, N) 
	except: 
		print(fname)
		print('File not found')