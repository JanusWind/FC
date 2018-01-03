################################################################################
##
## Janus -- GUI Software for Processing Thermal-Ion Measurements from the
##          Wind Spacecraft's Faraday Cups
##
## Copyright (C) 2016 Bennett A. Maruca (bmaruca@udel.edu)
##
## This program is free software: you can redistribute it and/or modify it under
## the terms of the GNU General Public License as published by the Free Software
## Foundation, either version 3 of the License, or (at your option) any later
## version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
## FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
## details.
##
## You should have received a copy of the GNU General Public License along with
## this program.  If not, see http://www.gnu.org/licenses/.
##
################################################################################


################################################################################
## LOAD THE NECESSARY MODULES.
################################################################################

# Import the modules need for signaling.

from PyQt4.QtCore import SIGNAL

# Import the modules needed for multithreading.

from threading import enumerate as ThreadList


################################################################################
## DEFINE THE FUNCTION FOR TESTING IF ANY OF THESE THREADS IS ALREADY RUNNING.
################################################################################

def n_thread( ) :

	n = 0

	for thr in ThreadList( ) :
		if ( ( thr._Thread__target is thread_load_spec        ) or
		     ( thr._Thread__target is thread_anls_mom         ) or
		     ( thr._Thread__target is thread_anls_nln         ) or
		     ( thr._Thread__target is thread_chng_dsp         ) or
		     ( thr._Thread__target is thread_chng_dyn         ) or
		     ( thr._Thread__target is thread_chng_opt         ) or
		     ( thr._Thread__target is thread_rstr_opt         ) or
		     ( thr._Thread__target is thread_auto_run         ) or
		     ( thr._Thread__target is thread_save_res         ) or
		     ( thr._Thread__target is thread_xprt_res         ) or
		     ( thr._Thread__target is thread_chng_mom_sel     ) or
                     ( thr._Thread__target is thread_auto_mom_sel     ) or
		     ( thr._Thread__target is thread_chng_nln_spc     ) or
		     ( thr._Thread__target is thread_chng_nln_pop     ) or
		     ( thr._Thread__target is thread_chng_nln_set     ) or
		     ( thr._Thread__target is thread_chng_nln_gss     ) or
		     ( thr._Thread__target is thread_chng_nln_sel     ) or
		     ( thr._Thread__target is thread_chng_mom_win_dir ) or
		     ( thr._Thread__target is thread_chng_mom_win_bin )   ) :
			n += 1

	return n


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.load_spec".
################################################################################

def thread_load_spec( core, time_req, get_prev=False, get_next=False ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.load_spec( time_req, get_prev, get_next )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.anls_mom" (WITH "chng_dsp").
################################################################################

def thread_anls_mom( core ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.anls_mom( )
	core.chng_dsp( 'mom' )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.anls_nln" (WITH "chng_dsp").
################################################################################

def thread_anls_nln( core ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.anls_nln( )
	core.chng_dsp( 'nln' )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_dsp".
################################################################################

def thread_chng_dsp( core, value ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_dsp( value )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_dyn".
################################################################################

def thread_chng_dyn( core, anal, value ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_dyn( anal, value )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_opt".
################################################################################

def thread_chng_opt( core, key, value ) :

        core.emit( SIGNAL('janus_busy_end') )
        core.emit( SIGNAL('janus_busy_beg') )

        core.chng_opt( key, value )

        core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.rstr_opt".
################################################################################

def thread_rstr_opt( core ) :

        core.emit( SIGNAL('janus_busy_end') )
        core.emit( SIGNAL('janus_busy_beg') )

        core.rstr_opt( )

        core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.auto_run".
################################################################################

def thread_auto_run( core, t_strt, t_stop,
                     get_next=None, err_halt=None, pause=None ) :

        core.emit( SIGNAL('janus_busy_end') )
        core.emit( SIGNAL('janus_busy_beg') )

        core.auto_run( t_strt, t_stop, get_next, err_halt, pause )

        core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.save_res".
################################################################################

def thread_save_res( core, nm_fl, exit=False ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.save_res( nm_fl, exit )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.xprt_res".
################################################################################

def thread_xprt_res( core, nm_fl, exit=False ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.xprt_res( nm_fl, exit )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_mom_sel".
################################################################################

def thread_chng_mom_sel( core, c, d, b ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_mom_sel( c, d, b )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.auto_mom_sel".
################################################################################

def thread_auto_mom_sel( core ) :

        core.emit( SIGNAL('janus_busy_end') )
        core.emit( SIGNAL('janus_busy_beg') )

        core.auto_mom_sel( )

        core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_nln_spc".
################################################################################

def thread_chng_nln_spc( core, s, param, val ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_nln_spc( s, param, val )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_nln_pop".
################################################################################

def thread_chng_nln_pop( core, i, param, val ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_nln_pop( i, param, val )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_nln_set".
################################################################################

def thread_chng_nln_set( core, i, param, val ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_nln_set( i, param, val )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_nln_gss".
################################################################################

def thread_chng_nln_gss( core, i, param, val ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_nln_gss( i, param, val )

	core.emit( SIGNAL('janus_busy_end') )
 

################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_nln_sel".
################################################################################

def thread_chng_nln_sel( core, c, d, b ) :

        core.emit( SIGNAL('janus_busy_end') )
        core.emit( SIGNAL('janus_busy_beg') )

        core.chng_nln_sel( c, d, b )

        core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_mom_win_dir".
################################################################################

def thread_chng_mom_win_dir( core, val ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_mom_win_dir( val )

	core.emit( SIGNAL('janus_busy_end') )


################################################################################
## DEFINE THE WRAPPER FOR THE FUNCTION "core.chng_mom_win_bin".
################################################################################

def thread_chng_mom_win_bin( core, val ) :

	core.emit( SIGNAL('janus_busy_end') )
	core.emit( SIGNAL('janus_busy_beg') )

	core.chng_mom_win_bin( val )

	core.emit( SIGNAL('janus_busy_end') )
