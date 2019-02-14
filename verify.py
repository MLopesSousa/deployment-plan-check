import xmltodict
import os
import re
import sys

d = "deployment"

def get_files(d):
        files = []
        for f in os.listdir(d):
                if re.match('.*\.plan\.xml$',f):
                        files.append(f)

        return files

def check_plan(f):
        xml = open(f, "r").read()
        try:
                obj = xmltodict.parse(xml)
        except:
                print("ERROR parsing %s" % (f))
                sys.exit(1)


        defined_variables = obj['deployment-plan']['variable-definition']['variable']
        defined_assignment = 0

        for module_descriptor in obj['deployment-plan']['module-override']['module-descriptor']:
                if not module_descriptor.get('variable-assignment') == None:
                        defined_assignment+= len(module_descriptor['variable-assignment'])

        #print("Defined variables found in %s: %s" %(f, str(len(defined_variables))))
        #print("Assignment variables found in %s: %s" %(f, str(defined_assignment)))

        return str(len(defined_variables)) + ":" + str(defined_assignment)


for f in get_files(d):
        df = d + "/" + f
        cr = 0

        if 'last_file_check' not in locals():
                last_file_check = check_plan(df)
                last_file = df
        else:
                if last_file_check != check_plan(df):
                        print("Current file %s:%s diverges from last file %s:%s !!!" % (df, check_plan(df), last_file, last_file_check))
                        cr = 1

                last_file_check = check_plan(df)
                last_file = df

sys.exit(int(cr))
