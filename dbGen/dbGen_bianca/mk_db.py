#!/usr/bin/env python
#mk_db

import os
import subprocess
import dbGen_stripe

subprocess.check_call(['rm' ,  '/home/bianca/Documents/github/locustVR/dbGen/stripe_flyVRExperiments.db'])
subprocess.check_call(['rm', '/home/bianca/Documents/github/locustVR/dbGen/stripe_flyVRProjects.db'])
dbGen_stripe.FirstGen()







#subprocess.call(["python dbGen_stripe.py"])


#os.system("/home/bianca/Documents/github/locustVR/dbGen/dbGen_stripe.py")
#subprocess.check_call(["python2.7", "/home/bianca/Documents/github/locustVR/dbGen/dbGen_stripe.py"])
subprocess.call(["python2.7" , "/home/bianca/Documents/github/locustVR/dbGen/dbGen_stripe.py"])
subprocess.call(["sqlitebrowser" , "/home/bianca/Documents/github/locustVR/dbGen/stripe_flyVRProjects.db"])




quit()