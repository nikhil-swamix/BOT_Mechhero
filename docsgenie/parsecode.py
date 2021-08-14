import ast,os,re

def titlecase_text(istr):
	"""this function is unique idea by: Nikhil Swami the great"""
	result=re.sub(r'\w+',lambda m:m.group(0)[0].upper()+m.group(0)[1:],istr)
	# result=re.sub(r'\w*',lambda m:[m.group(0).capitalize(),print(m)][0],istr) #DEBUG
	return result

def generate_markdown(filepath,output='./'):
	modulename=os.path.basename(filepath)
	# print(modulename)
	file=open(filepath,'r').read()
	astmodule=ast.parse(file)
	moduleDocstring=titlecase_text(ast.get_docstring(astmodule,clean=1)).replace('\n',' ')
	print(f"# MODULE: {modulename} \n {moduleDocstring}")
	for x in astmodule.body:
		if type(x) in [ast.FunctionDef,ast.ClassDef,ast.Module]:#logic sugar
			docstring=ast.get_docstring(x,clean=1)
			dsmessage=''
			print(f"\n---")
			print(f'## Function: **{x.name}**({",".join("<ins>"+y.arg+"</ins>" for y in x.args.args)})')
			if not docstring:
				dsmessage+='Sorry, Developer Has not provided docstring for this function'
			else:
				dsmessage+="\n".join('- '+x for x in docstring.split('\n'))
			print(dsmessage)


if __name__ == '__main__':
	filepath='../NPCExplorer.py'
	generate_markdown(filepath)








UNITTESTS=0
if UNITTESTS:
	titlecase_text('which allows uninterrupted and smart execution of NPC tiles')