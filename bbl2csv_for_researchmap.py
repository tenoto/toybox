#!/usr/bin/env python

"""
Research Map
1. pip install pybtex-docutils 
2. at ADS : Search for the author full name (e.g., "Enoto, Teruaki") with selecting "Refereed Journal" below. 
3. Selecting "BibTex with abstracts", "Save to file", Sort by "date", and "Retrieve selected records"
4. Rename the downloaded bbl file, (e.g., "enoto_refereed_journal.bbl")

reference
- http://pybtex-docutils.readthedocs.io/en/latest/
"""

__file__    = 'bbl2csv_for_researchmap.py'
__author__  = 'Teru Enoto'
__date__    = '2018 August 17'
__version__ = '0.01'

import os 
import sys 
import argparse
import pandas as pd 
from pybtex.database.input import bibtex
import datetime

def strip_brackets(word):
	return word.replace('{','').replace('}','')

def get_formatted_name(person):
	try:
		last_name = strip_brackets(unicode(person.last()[0]))
		first_initial = unicode(person.first()[0][0])
		return '%s %s.' % (last_name,first_initial)
	except:
		last_name = strip_brackets(unicode(person.last()[0]))		
		return last_name

def month_string_to_number(string):
	m = {
		'jan': 1,
		'feb': 2,
		'mar': 3,
		'apr':4,
		'may':5,
		'jun':6,
		'jul':7,
		'aug':8,
		'sep':9,
		'oct':10,
		'nov':11,
		'dec':12
		}
	s = string.strip()[:3].lower()

	try:
		out = m[s]
		return out
	except:
		raise ValueError('Not a month')

def abbreviation_to_name(string):
	journal_dictionary = {
		'aj':'Astronomical Journal',
		'actaa':'Acta Astronomica',
		'araa':'Annual Review of Astron and Astrophys',
		'apj':'Astrophysical Journal',
		'apjl':'Astrophysical Journal Letters',
		'apjs':'Astrophysical Journal Supplement',
		'ao':'Applied Optics',
		'apss':'Astrophysics and Space Science',
		'aap':'Astronomy and Astrophysics',
		'aapr':'Astronomy and Astrophysics Reviews',
		'aaps':'Astronomy and Astrophysics Supplement',
		'azh':'Astronomicheskii Zhurnal',
		'baas':'Bulletin of the AAS',
		'caa':'Chinese Astronomy and Astrophysics',
		'cjaa':'Chinese Journal of Astronomy and Astrophysics',
		'icarus':'Icarus',
		'jcap':'Journal of Cosmology and Astroparticle Physics',
		'jrasc':'Journal of the RAS of Canada',
		'memras':'Memoirs of the RAS',
		'mnras':'Monthly Notices of the RAS',
		'na':'New Astronomy',
		'nar':'New Astronomy Review',
		'pra':'Physical Review A: General Physics',
		'prb':'Physical Review B: Solid State',
		'prc':'Physical Review C',
		'prd':'Physical Review D',
		'pre':'Physical Review E',
		'prl':'Physical Review Letters',
		'pasa':'Publications of the Astron. Soc. of Australia',
		'pasp':'Publications of the ASP',
		'pasj':'Publications of the Astronomical Society of Japan',
		'rmxaa':'Revista Mexicana de Astronomia y Astrofisica',
		'qjras':'Quarterly Journal of the RAS',
		'skytel':'Sky and Telescope',
		'solphys':'Solar Physics',
		'sovast':'Soviet Astronomy',
		'ssr':'Space Science Reviews',
		'zap':'Zeitschrift fuer Astrophysik',
		'nat':'Nature',
		'iaucirc':'IAU Cirulars',
		'aplett':'Astrophysics Letters',
		'apspr':'Astrophysics Space Physics Research',
		'bain':'Bulletin Astronomical Institute of the Netherlands',
		'fcp':'Fundamental Cosmic Physics',
		'gca':'Geochimica Cosmochimica Acta',
		'grl':'Geophysics Research Letters',
		'jcp':'Journal of Chemical Physics',
		'jgr':'Journal of Geophysics Research',
		'jqsrt':'Journal of Quantitiative Spectroscopy and Radiative Transfer',
		'memsai':'Mem. Societa Astronomica Italiana',
		'nphysa':'Nuclear Physics A',
		'physrep':'Physics Reports',
		'physscr':'Physica Scripta',
		'planss':'Planetary Space Science',
		'procspie':'Proceedings of the SPIE'
		}

	try:
		out = journal_dictionary[string.replace('\\','')]
		return out
	except:
		return string
		#raise ValueError('No corresponding jounarl.')


class BiBLiographicReferenceFile():
	def __init__(self,bblfile,last_name):
		self.bblfile = bblfile
		if not os.path.exists(self.bblfile):
			sys.stderr.write('error: input bbl file does not exist.\n' % self.bblfile)
			exit()
		sys.stdout.write('input file: %s\n' % self.bblfile)

		self.last_name = last_name

		self.csvfile = self.bblfile.replace('.bbl','.csv')		

	def convert2csv_for_researchmap(self,max_number_of_author_list=5):
		rows = []

		parser = bibtex.Parser()
		bib_data = parser.parse_file(self.bblfile)
		print(len(bib_data.entries))
		for e in bib_data.entries:
			title = strip_brackets(unicode(bib_data.entries[e].fields['title']))
			print(title)

			author_list = ""
			num_of_authors = len(bib_data.entries[e].persons['author'])

			author_order = -1 
			for author in bib_data.entries[e].persons['author']:
				if self.last_name in author.last()[0]:			
					author_order = bib_data.entries[e].persons['author'].index(author) + 1 
					your_name = get_formatted_name(author)
					break

			if num_of_authors <= max_number_of_author_list:
				for i in range(num_of_authors-1):
					author_list += '%s, ' % get_formatted_name(bib_data.entries[e].persons['author'][i])
				author_list += 'and %s, ' % get_formatted_name(bib_data.entries[e].persons['author'][num_of_authors-1])					
			else:
				for i in range(max_number_of_author_list-1):
					author_list += '%s, ' % get_formatted_name(bib_data.entries[e].persons['author'][i])
				author_list += 'and %s ' % get_formatted_name(bib_data.entries[e].persons['author'][max_number_of_author_list-1])
				author_list += 'et al., '
			if author_order > max_number_of_author_list:
				author_list += '(%s as %d-th author out of %d authors),' % (your_name,author_order,num_of_authors)

			try:
				journal = abbreviation_to_name(strip_brackets(unicode(bib_data.entries[e].fields['journal'])))
			except:
				journal = ""
				raise ValueError('error: journal name')

			try:
				volume  = 'vol.%s' % strip_brackets(unicode(bib_data.entries[e].fields['volume']))
			except:
				volume = ""
				raise ValueError('error: volume')

			try:
				pages = strip_brackets(unicode(bib_data.entries[e].fields['pages']))
				if len(pages.split('-')) == 2:
					starting_page,ending_page = pages.split('-')
				elif len(pages.split('-')) == 1:
					starting_page = pages.split('-')[0]
					ending_page = ""
				else:
					starting_page = ""
					ending_page = ""
			except:
				starting_page = ""
				ending_page = ""
				print("error: pages")

			year = strip_brackets(unicode(bib_data.entries[e].fields['year']))
			try:
				month = strip_brackets(unicode(bib_data.entries[e].fields['month']))
				yyyymmdd = '%s%02d00' % (year,month_string_to_number(month))
			except:
				yyyymmdd = '%s1200' % (year)
				print("error: year and month")
				
			try:
				doi = strip_brackets(unicode(bib_data.entries[e].fields['doi']))
				permalink = 'https://doi.org/%s' % doi
			except:
				doi = ""
				permalink = ""
				print("error: doi and permalink")

			try:
				adsurl = strip_brackets(unicode(bib_data.entries[e].fields['adsurl']))
			except:
				adsurl = ""
				print('error: adsurl')

			rows.append([
				title,title,				# "Title(English)","Title(Japanese)",
				author_list,author_list,	# "Author(English)","Author(Japanese)",
				journal,journal,			# "Journal(English)","Journal(Japanese)",
				volume,"",starting_page,ending_page,yyyymmdd,		# "Volume","Number","Starting page","Ending page","Publication date",
				1,0,"",0,			# "Refereed paper","Invited paper","Language","Publishing type",
				"",						# "ISSN",
				doi,"","","",		# "ID:DOI","ID:JGlobalID","ID:NAID","ID:PMID",
				permalink,adsurl,					# "Permalink","URL",
				"",""					# "Description(English)","Description(Japanese)"				
				])

		columns = [
			"Title(English)","Title(Japanese)",
			"Author(English)","Author(Japanese)",
			"Journal(English)","Journal(Japanese)",
			"Volume","Number","Starting page","Ending page","Publication date",
			"Refereed paper","Invited paper","Language","Publishing type",
			"ISSN",
			"ID:DOI","ID:JGlobalID","ID:NAID","ID:PMID",
			"Permalink","URL",
			"Description(English)","Description(Japanese)"
			]
		df = pd.DataFrame(rows,columns=columns)
		df.to_csv(self.csvfile,index=False)

if __name__=="__main__":

	parser = argparse.ArgumentParser(
		prog=__file__,
		usage='%s bblfile last_name' % __file__,
		description='convert a bbl-format file to csv-format to be imported into Researchmap.',
		epilog='',
		add_help=True,
		)
	parser.add_argument(
		'bblfile',metavar='bblfile',type=str,
		help='Input BiBLiographic reference file downloaded from ADS.')
	parser.add_argument(
		'last_name',metavar='last_name',type=str,
		help='Last name')
	args = parser.parse_args()	

	bbl = BiBLiographicReferenceFile(args.bblfile,args.last_name)
	bbl.convert2csv_for_researchmap()
