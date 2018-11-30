from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pdb
import pickle
import numpy as np
import pandas as pd
from pathlib2 import Path
from datetime import datetime

class Janus2HDF(object):
	def __init__(self, load_path, fitter):
		self.set_path(load_path)
		self.set_fitter(fitter)
		self.load_dat()
		self.convert_dat2df()
		self.save_df()

	def __str__(self):
		return self.__class__.__name__

	@property
	def load_path(self):
		return self._load_path / self.fitter
	@property
	def fitter(self):
		return self._fitter
	@property
	def hdf_key(self):
		f = self.fitter
		if f == "mark":
			return "MJP"
		elif f == "ramiz":
			return "RAQ"
		else:
			msg = "Unrecognized fitter for building `hdf_key`: %s"
			raise ValueError(msg % f)
	@property
	def save_name(self):
		fname = "Feb2014_Janus_Event_Study_%s.h5" % datetime.now().strftime("%Y%m%d")
		return fname
	@property
	def fnames(self):
		fnames = sorted(list(self.load_path.glob("*.jns")))
		fnames = [x.parts[-1] for x in fnames]
		return fnames
	@property
	def dat(self):
		return self._dat
	@property
	def nspec(self):
		return self._nspec
	@property
	def df(self):
		return self._df

	@property
	def species_translator(self):
		return {"p1"  : 'p_c',
			"p2"  : 'p_b',
			"a1"  : 'a_c',
			"a2"  : 'a_b',
			"o6p1": 'o_c',
			"o6p2": 'o_b'
                       }

	def set_path(self, load_path):
		self._load_path = Path(load_path)
	def set_fitter(self, new):
		assert new in ("mark", "ramiz")
		self._fitter = new
	def load_dat(self):
		lp = self.load_path
		fnames = self.fnames

		dat = [0]*len(fnames)

		for j, fn in enumerate(fnames):
			file_path = lp / fn
			dat[j] = pickle.load( open(str(file_path),'rb') )

			print('Reading file {}'.format(fn))

		nspec = sum([d.n for d in dat])
		nspec_old = sum( [ len(dat[j]['b0'] ) for j in range ( len( fnames ) ) ] )
		assert nspec == nspec_old

		self._dat   = dat
		self._nspec = nspec

	def _get_dt_info(self):

		fnames = self.fnames
		dat = self.dat
		nspec = self.nspec
		year = np.full(nspec, 2014, dtype=np.int64)
		day  = np.full(nspec, 45,   dtype=np.int64)
		time = []

		for j in range( len( fnames ) ) :
			time += [ dat[j]['time'][i]  for i in range( len( dat[j]['time'] ) ) ]
		time = np.array(time)
		return year, day, time

	def _get_bfield(self):
		fnames = self.fnames
		dat = self.dat
		bx = []
		by = []
		bz = []


		for j in range( len( fnames ) ) :
			bx += dat[j]['b0_x']
			by += dat[j]['b0_y']
			bz += dat[j]['b0_z']


		bx = np.array(bx, dtype=np.float64)
		by = np.array(by, dtype=np.float64)
		bz = np.array(bz, dtype=np.float64)
		return bx, by, bz

	def _get_species(self, sB, sJ):
		dat = self.dat

		trans = {"n_": ("n", ""),
			 "w_per_": ("w", "per"),
			 "w_par_": ("w", "par"),
			 "w_": ("w", "scalar"),
			 }


		tc = {}
		for k in ("n_",
			  "w_per_", "w_par_", "w_"):

			kv = k + sJ
			ks = "sig_" + kv

			v = [d[kv] for d in dat]
			v = np.concatenate(v).astype(np.float64)
			s = [d[ks] for d in dat]
			s = np.concatenate(s).astype(np.float64)

			kB = trans[k] + (sB,)
			tc[kB] = v

			c = k.split("_")[1]
			if not c and k[0] == "w":
				c = "scalar"

			kBs = (k[0] + "_err", c, sB)
			tc[kBs] = s


		if sJ == "p_c":
			for c in ("x", "y", "z"):
				kv = "v0_%s_" % c + sJ
				ks = "sig_" + kv

				v = [d[kv] for d in dat]
				v = np.concatenate(v).astype(np.float64)
				s = [d[ks] for d in dat]
				s = np.concatenate(s).astype(np.float64)

				tc[("v", c, "p1")]     = v
				tc[("v_err", c, "p1")] = s

		else:
			kv = "dv_" + sJ
			ks = "sig_" + kv

			v = np.concatenate([d[kv] for d in dat]).astype(np.float64)
			s = np.concatenate([d[kv] for d in dat]).astype(np.float64)

			tc[("dv", "par", sB)]     = v
			tc[("dv_err", "par", sB)] = s

		return tc



	def convert_dat2df(self):
		year, doy, time = self._get_dt_info()
		bx, by, bz = self._get_bfield()

		tc = {("year", "", ""): year,
		      ("doy",  "", ""): doy,
		      ("time", "", ""): time,
		      ("b", "x",   ""): bx,
		      ("b", "y",   ""): by,
		      ("b", "z",   ""): bz}

		species_translator = self.species_translator
		for sB, sJ in species_translator.items():
			species_data = self._get_species(sB, sJ)
			tc.update(species_data)

		df = pd.DataFrame.from_dict(tc, orient="columns")
		self._df = df

	def save_df(self):
		fitter = self.fitter
		keys = {"ramiz": "RAQ", "mark": "MJP"}
		key = keys[fitter]

		sname = self.save_name
		df = self.df
		df.to_hdf(sname, key=key)

def run(fitter):
	load_path = Path("/home/ahmadr/Desktop/GIT/Personal/Janus/results/save/")
	j2h = Janus2HDF(load_path, fitter)

	return j2h 

if __name__ == "__main__":
	run()
