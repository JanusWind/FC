from janus_spin_arcv import spin_arcv
a = spin_arcv()
b = spin_arcv()
a.load_spin('2007 1 12 12')
b.load_spin('2008 12 1 12')
a.cleanup_date()
a.cleanup_file()
