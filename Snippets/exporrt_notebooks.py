
import os,pathlib

dirREPO      = pathlib.Path( __file__ ).parent.parent


def export_ipynb_as_html_embed(fpathIPYNB):
	cmd          = f'jupyter nbconvert --template classic --to html_embed {fpathIPYNB}'
	os.system( cmd )


# # export single notebook:
# fpathIPYNB   = os.path.join(dirREPO, 'Lessons', 'Lesson01', '1-IntroductionToJupyter', 'IntroductionToJupyter.ipynb')
# export_ipynb_as_html_embed( fpathIPYNB )


# export all notebooks for one lesson:
lesson       = 8
dirLESSON    = os.path.join( dirREPO, 'Lessons', f'Lesson{lesson:02}')
for root,dname,fnames in os.walk(dirLESSON):
	for f in fnames:
		if f.endswith('.ipynb') and not ('checkpoint' in f):
			fpathIPYNB = os.path.join(root, f)
			export_ipynb_as_html_embed( fpathIPYNB )




